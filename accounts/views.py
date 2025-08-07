from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.utils import timezone

from .forms import CustomAuthenticationForm
from .models import LoginAttempt

User = get_user_model()

# Lista local de destinatarios (puedes moverla a settings si lo prefieres)
EMAIL_RECIPIENTS = [
    'kramosv@inacap.cl',
    'kassramosveg@gmail.com',
]

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html'

    def form_invalid(self, form):
        username = form.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                login_attempt, _ = LoginAttempt.objects.get_or_create(user=user)

                # Si ya está bloqueado, avisamos y salimos
                if login_attempt.is_locked():
                    messages.error(self.request, "Tu cuenta está bloqueada. Inténtalo de nuevo más tarde.")
                    return super().form_invalid(form)

                # Incrementamos contador
                login_attempt.increment_failed_attempts()

                # Al segundo fallo, enviamos correo
                if login_attempt.failed_attempts == 2:
                    print("🚀 ¡Llegué al segundo fallo! Enviando correo…")  
                    subject = f"[Alerta] 2 intentos fallidos de {username}"
                    body = (
                        f"Usuario: {username}\n"
                        f"IP: {self.request.META.get('REMOTE_ADDR')}\n"
                        f"Hora: {timezone.localtime().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                        "Se han registrado 2 intentos fallidos de inicio de sesión."
                    )
                    send_mail(
                        subject,
                        body,
                        settings.DEFAULT_FROM_EMAIL,
                        EMAIL_RECIPIENTS,      # **IMPORTANTE:** debe ser siempre una lista
                        fail_silently=False,
                    )
                    messages.warning(
                        self.request,
                        "Contraseña incorrecta. Se ha enviado un aviso al equipo de seguridad."
                    )

                # Al tercer fallo o si se bloquea, informamos de bloqueo
                if login_attempt.is_locked():
                    messages.error(
                        self.request,
                        "Demasiados intentos fallidos. Tu cuenta ha sido bloqueada por 5 minutos."
                    )
                elif login_attempt.failed_attempts == 1:
                    # Mensaje genérico en el primer fallo
                    messages.error(self.request, "Contraseña incorrecta.")

            except User.DoesNotExist:
                messages.error(self.request, "Usuario o contraseña incorrectos.")
            except Exception as e:
                # Aquí podrías loguear e incluso grabar e en sentry, etc.
                messages.error(self.request, "Ocurrió un error durante el inicio de sesión.")

        return super().form_invalid(form)

# # accounts/views.py
# from django.views.generic import ListView, UpdateView, DeleteView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.urls import reverse_lazy
# from django.contrib import messages
# from django.shortcuts import get_object_or_404, render, redirect
# from django.contrib.auth.models import User, Group
# from .models import User, Profile
# from .forms import UserUpdateForm, ProfileUpdateForm
# from django.db.models import F, Prefetch
# from accounts.models import Profile
# from .decorators import get_group_and_color
# from .funciones import plural_singular
# from django.db import transaction
# from django.http import HttpResponseRedirect



# class ProfileListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
#     model = User
#     template_name = 'profiles/profile_list.html'
#     context_object_name = 'profiles_with_singular_groups'
#     paginate_by = 10

#     def test_func(self):
#         """Solo ADR puede ver la lista"""
#         return self.request.user.groups.filter(name='ADR').exists()
    
#     def handle_no_permission(self):
#         messages.error(self.request, 'No tiene permisos para esta acción')
#         return redirect('error')

#     def get_queryset(self):
#         # Optimizar la consulta para incluir todos los datos necesarios
#         queryset = User.objects.all().select_related('profile').prefetch_related('groups')
#         profiles_with_groups = []
        
#         for user in queryset:
#             group_names = [group.name for group in user.groups.all()]
#             singular_groups = [name.replace('es ADR', ' ADR').replace('s ADR', ' ADR') 
#                              for name in group_names]
            
#             profiles_with_groups.append({
#                 'profile': user.profile,
#                 'singular_groups': singular_groups
#             })
        
#         return profiles_with_groups

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         # Mantener el grupo del usuario actual para permisos de visualización
#         if self.request.user.groups.exists():
#             group_name = self.request.user.groups.first().name
#             context['group_name_singular'] = group_name.replace('es ADR', ' ADR').replace('s ADR', ' ADR')
        
#         return context

# class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = User
#     template_name = 'profiles/profile_edit.html'
#     form_class = UserUpdateForm
#     success_url = reverse_lazy('profile_list')

#     def test_func(self):
#         return self.request.user.groups.filter(name='ADR').exists()
    
#     def handle_no_permission(self):
#         messages.error(self.request, 'No tiene permisos para esta acción')
#         return redirect('error')

#     def get_object(self):
#         return get_object_or_404(User, pk=self.kwargs['pk'])

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.get_object()
        
#         # Pasamos el formulario de perfil al contexto
#         if self.request.method == 'GET':
#             context['profile_form'] = ProfileUpdateForm(instance=user.profile)
#         else:
#             context['profile_form'] = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=user.profile)
        
#         return context

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()  # UserUpdateForm
#         profile_form = ProfileUpdateForm(self.request.POST, self.request.FILES, instance=self.object.profile)

#         # Validar y guardar ambos formularios en una transacción atómica
#         if form.is_valid() and profile_form.is_valid():
#             with transaction.atomic():
#                 form.save()
#                 profile_form.save()
#             messages.success(self.request, 'Perfil actualizado exitosamente')
#             return redirect(self.success_url)
#         else:
#             # Si hay errores, renderizamos la página con ambos formularios y los errores
#             return self.form_invalid(form)

#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         form = self.get_form()
#         profile_form = ProfileUpdateForm(
#             request.POST,
#             request.FILES,
#             instance=self.object.profile
#         )

#         if form.is_valid() and profile_form.is_valid():
#             return self.form_valid(form, profile_form)
#         return self.form_invalid(form)

#     def form_valid(self, form, profile_form):
#         # Guardar el usuario
#         user = form.save(commit=False)
#         profile_form.save()
        
#         # Actualizar grupo
#         new_group_id = self.request.POST.get('group')
#         if new_group_id:
#             user.groups.clear()
#             user.groups.add(new_group_id)
        
#         user.save()
#         messages.success(self.request, 'Usuario actualizado exitosamente')
        
#         # Asegurar que la página de lista se actualice correctamente
#         return redirect(self.get_success_url())

#     def get_success_url(self):
#         return reverse_lazy('profile_list')

#     def form_invalid(self, form):
#         messages.error(self.request, 'Por favor corrija los errores en el formulario.')
#         return super().form_invalid(form)
    
    
# class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = User
#     success_url = reverse_lazy('profile_list')
#     template_name = 'profiles/profile_confirm_delete.html'  # Puedes omitir esto si no quieres una página de confirmación
   
#     def test_func(self):
#         """Solo ADR puede eliminar perfiles"""
#         return self.request.user.groups.filter(name='ADR').exists()
   
#     def handle_no_permission(self):
#         messages.error(self.request, 'No tiene permisos para esta acción')
#         return redirect('error')
   
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.user.groups.exists():
#             group_name = self.request.user.groups.first().name
#             context['group_name_singular'] = group_name.replace('es ADR', ' ADR').replace('s ADR', ' ADR')
#         return context
   
#     def delete(self, request, *args, **kwargs):
#         try:
#             self.object = self.get_object()
#             nombre_usuario = self.object.username
#             success_url = self.get_success_url()
            
#             # Eliminar el usuario
#             self.object.delete()
            
#             messages.success(self.request, f'Usuario {nombre_usuario} eliminado exitosamente')
#             return HttpResponseRedirect(success_url)
            
#         except Exception as e:
#             messages.error(self.request, f'Error al eliminar usuario: {str(e)}')
#             return redirect('profile_list')
    
#     def post(self, request, *args, **kwargs):
#         """
#         Sobreescribimos post para manejar las solicitudes AJAX si es necesario
#         """
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             try:
#                 self.object = self.get_object()
#                 nombre_usuario = self.object.username
#                 self.object.delete()
#                 messages.success(request, f'Usuario {nombre_usuario} eliminado exitosamente')
#                 return HttpResponseRedirect(self.success_url)
#             except Exception as e:
#                 messages.error(request, f'Error al eliminar usuario: {str(e)}')
#                 return HttpResponseRedirect(self.success_url)
#         return super().post(request, *args, **kwargs)