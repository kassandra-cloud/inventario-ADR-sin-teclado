from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import LoginAttempt
from django.core.exceptions import ValidationError

UserModel = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            try:
                user = UserModel._default_manager.get(username=username)
            except UserModel.DoesNotExist:
                # No revelar si el usuario existe o no directamente
                # Incrementar intento para un usuario 'fantasma' podría ser una opción,
                # pero por simplicidad, solo lanzamos el error estándar.
                raise ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

            login_attempt, created = LoginAttempt.objects.get_or_create(user=user)

            if login_attempt.is_locked():
                lockout_time_left = timezone.localtime(login_attempt.lockout_until) - timezone.localtime(timezone.now())
                minutes_left = int(lockout_time_left.total_seconds() // 60)
                seconds_left = int(lockout_time_left.total_seconds() % 60)
                
                raise ValidationError(
                    f"Su cuenta ha sido bloqueada temporalmente debido a múltiples intentos fallidos. "
                    f"Por favor, inténtelo de nuevo en {minutes_left} minutos y {seconds_left} segundos.",
                    code='account_locked',
                )

            if not self.user_cache.check_password(password):
                login_attempt.increment_failed_attempts()
                if login_attempt.is_locked():
                    # El bloqueo ocurrió en este intento
                    lockout_time_left = timezone.localtime(login_attempt.lockout_until) - timezone.localtime(timezone.now())
                    minutes_left = int(lockout_time_left.total_seconds() // 60)
                    seconds_left = int(lockout_time_left.total_seconds() % 60)
                    raise ValidationError(
                        f"Credenciales incorrectas. Su cuenta ha sido bloqueada temporalmente. "
                        f"Por favor, inténtelo de nuevo en {minutes_left} minutos y {seconds_left} segundos.",
                        code='account_locked_now',
                    )
                else:
                    # Aún no está bloqueado, pero el intento falló
                    remaining_attempts = 3 - login_attempt.failed_attempts
                    if remaining_attempts > 0:
                        raise ValidationError(
                            f"Credenciales incorrectas. Le quedan {remaining_attempts} intentos.",
                            code='invalid_login_attempts_left',
                        )
                    else: # Esto no debería ocurrir si is_locked() funciona bien arriba
                         raise ValidationError(
                            self.error_messages['invalid_login'],
                            code='invalid_login',
                            params={'username': self.username_field.verbose_name},
                        )
            else:
                # Inicio de sesión exitoso
                login_attempt.reset_attempts()
        
        return self.cleaned_data

# # # forms.py
#
# # from django import forms
# # from django.contrib.auth.models import User
# # from accounts.models import Profile
#
# # class UserForm(forms.ModelForm):
# #     """Formulario para actualización de datos básicos del usuario"""
# #     class Meta:
# #         model = User
# #         fields = ['username', 'first_name', 'last_name', 'email']
# #         widgets = {
# #             'username': forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-white', 'readonly': 'readonly'}),
# #             'first_name': forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-white'}),
# #             'last_name': forms.TextInput(attrs={'class': 'w-full p-2 rounded bg-white'}),
# #             'email': forms.EmailInput(attrs={'class': 'w-full p-2 rounded bg-white'}),
# #         }
#
# # class ProfileForm(forms.ModelForm):
# #     """Formulario para el perfil de usuario"""
# #     class Meta:
# #         model = Profile
# #         fields = ['image']
# #         widgets = {
# #             'image': forms.FileInput(attrs={'class': 'w-full p-2 rounded bg-white'}),
# #         }
