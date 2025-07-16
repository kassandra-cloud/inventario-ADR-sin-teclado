from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from django.contrib import messages # Import messages
from django.contrib.auth import get_user_model # Import get_user_model
from .models import LoginAttempt # Import LoginAttempt
from django.utils import timezone # Import timezone

User = get_user_model() # Get the User model

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'registration/login.html' # Asegúrate de que esta plantilla exista o ajústala

    def form_invalid(self, form):
        """Handle invalid login attempts."""
        username = form.cleaned_data.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
                login_attempt, created = LoginAttempt.objects.get_or_create(user=user)

                if login_attempt.is_locked():
                    messages.error(self.request, "Tu cuenta está bloqueada. Inténtalo de nuevo más tarde.")
                    return super().form_invalid(form) # Prevent further processing if locked

                login_attempt.increment_failed_attempts()

                if login_attempt.is_locked():
                    # Modificar el mensaje para que el JavaScript pueda parsear el tiempo de bloqueo
                    lockout_duration_minutes = 5 # Debe coincidir con el timedelta en models.py
                    messages.error(self.request, f"Demasiados intentos fallidos. Tu cuenta ha sido bloqueada. Por favor, inténtelo de nuevo en {lockout_duration_minutes} minutos y 0 segundos.")
                elif login_attempt.failed_attempts >= 2: # Warning before lockout (2 failed attempts + current failed = 3 total)
                     messages.warning(self.request, "Contraseña incorrecta. Tienes 1 intento restante antes de que tu cuenta sea bloqueada.")
                else:
                    messages.error(self.request, "Contraseña incorrecta.")

            except User.DoesNotExist:
                # Handle cases where the username doesn't exist (optional, could reveal valid usernames)
                messages.error(self.request, "Usuario o contraseña incorrectos.")
            except Exception as e:
                # Log the exception for debugging
                print(f"Error handling login attempt for {username}: {e}")
                messages.error(self.request, "Ocurrió un error durante el inicio de sesión.")

        return super().form_invalid(form)

    def form_valid(self, form):
        """Handle successful login attempts."""
        user = form.get_user()
        try:
            login_attempt = LoginAttempt.objects.get(user=user)
            login_attempt.reset_attempts()
        except LoginAttempt.DoesNotExist:
            # No login attempt record exists, which is fine for a successful login
            pass
        except Exception as e:
            # Log the exception for debugging
            print(f"Error resetting login attempt for {user.username}: {e}")

        return super().form_valid(form)
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