from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from .views import (
    LoginView, AddUserView, IndexView, ProfileListView, ProfileUpdateView, ProfileDeleteView, HomeView, CustomLoginView, HistorialCambiosView,
    ProfilePasswordChangeView,
    AllInOneView, Add_AllInOneView, Edit_AllInOneView,
    AllInOneAdminView, Add_AllInOneAdminView, Edit_AllInOneAdmView,
    NotebooksView, AddNotebooksView, Edit_NotebooksView,
    MiniPCView, AddMiniPCView, Edit_MiniPCView,
    ProyectoresView, AddProyectorView, Edit_ProyectorView,
    BodegaADRView, AddBodegaADRView, Edit_BodegaADRView,
    AzoteaView, AddAzoteaView, Edit_AzoteaView,
    ErrorView, DescargarExcelView,
    # Vistas para Monitor
    MonitorView, AddMonitorView, EditMonitorView, MonitorDetailView,
    # Vistas para Audio
    AudioView, AddAudioView, EditAudioView, AudioDetailView,
    # Vistas para Tablet
    TabletView, AddTabletView, EditTabletView, TabletDetailView,
    # Importación de las vistas de carga de Excel
    UploadExcelAllInOneView, UploadExcelNotebookView, UploadExcelProyectorView,
    UploadExcelMiniPCView, UploadExcelAllInOneAdmView, UploadExcelBodegaADRView,
    UploadExcelAzoteaView,
    ConfirmarRestauracionView, EliminadosListView, DeleteToEliminadosView, detalle_activo_busqueda
)
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import UserPasswordChangeView
from .forms import LoginForm


urlpatterns = [
    # Autenticación
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password_change/', login_required(ProfilePasswordChangeView.as_view()), name="profile_password_change"),
    
    # Gestión de Usuarios
    path('add_user/', login_required(AddUserView.as_view()), name="add_user"),
    path('profile_edit/<int:pk>/edit/', ProfileUpdateView.as_view(), name='profile_edit'),  # Edición de perfil
    path('profile_list/', login_required(ProfileListView.as_view()), name="profile_list"),
    path("mi-perfil/", views.my_profile, name="my_profile"),
    path('profile_delete/<int:pk>/', login_required(ProfileDeleteView.as_view()), name='profile_delete'),
     path("perfil/contraseña/cambiar/", UserPasswordChangeView.as_view(), name="password_change"),
    # Páginas Principales
    path('', IndexView.as_view(), name="index"),
        # Nueva ruta
    path('inicio/', login_required(HomeView.as_view()), name='inicio'),
     path(
        "login/",
        LoginView.as_view(
            authentication_form= LoginForm,
            template_name="registration/login.html",
        ),
        name="login",
    ),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
   
        # Redirección LEGACY con nombre 'home' (así reverse('home') sigue funcionando)
    path('home/', RedirectView.as_view(pattern_name='inicio', permanent=True), name='home'),
    path('all_in_one_selection/', login_required(views.AllInOneSelectionView.as_view()), name='all_in_one_selection'),
    path('buscar-global/', views.buscar_global, name='buscar_global'),      #  RUTA PARA BÚSQUEDA GLOBAL
    path('error/', ErrorView.as_view(), name="error"),
    
    # Gestión All In One
    path('all_in_one/', login_required(AllInOneView.as_view()), name="all_in_one"),
    path('add_all_in_one/', login_required(Add_AllInOneView.as_view()), name="add_all_in_one"),
    path('edit_all_in_one/<int:pk>/', login_required(Edit_AllInOneView.as_view()), name="edit_all_in_one"),
    path('delete_all_in_one/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_all_in_one'),
    path('eliminados/', login_required(EliminadosListView.as_view()), name='eliminados'),
    path('confirmar_restauracion_allinone/<int:pk>/', login_required(ConfirmarRestauracionView.as_view()), name='confirmar_restauracion_allinone'),
    
    # All In One Administradores
    path('all_in_one_adm/', login_required(AllInOneAdminView.as_view()), name="all_in_one_adm"),
    path('add_all_in_one_adm/', login_required(Add_AllInOneAdminView.as_view()), name="add_all_in_one_adm"),
    path('edit_all_in_one_adm/<int:pk>/', login_required(Edit_AllInOneAdmView.as_view()), name="edit_all_in_one_adm"),
    path('delete_all_in_one_adm/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_all_in_one_adm'),
    
    # Gestión de Notebooks
    path('notebooks/', login_required(NotebooksView.as_view()), name="notebooks"),
    path('add_notebook/', login_required(AddNotebooksView.as_view()), name="add_notebook"),
    path('edit_notebook/<int:pk>/', login_required(Edit_NotebooksView.as_view()), name="edit_notebook"),
    path('delete_notebook/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_notebook'),
    
    # Gestión de Mini PC
    path('mini_pc/', login_required(MiniPCView.as_view()), name="mini_pc"),
    path('add_mini_pc/', login_required(AddMiniPCView.as_view()), name="add_mini_pc"),
    path('edit_mini_pc/<int:pk>/', login_required(Edit_MiniPCView.as_view()), name="edit_mini_pc"),
    path('delete_mini_pc/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_mini_pc'),
    
    # Gestión de Proyectores
    path('proyectores/', login_required(ProyectoresView.as_view()), name="proyectores"),
    path('add_proyector/', login_required(AddProyectorView.as_view()), name="add_proyector"),
    path('edit_proyector/<int:pk>/', login_required(Edit_ProyectorView.as_view()), name="edit_proyector"),
    path('delete_proyector/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_proyector'),
    
    # Gestión de Bodega ADR
    path('bodega_adr/', login_required(BodegaADRView.as_view()), name="bodega_adr"),
    path('add_bodega_adr/', login_required(AddBodegaADRView.as_view()), name="add_bodega_adr"),
    path('edit_bodega_adr/<int:pk>/', login_required(Edit_BodegaADRView.as_view()), name="edit_bodega_adr"),
    path('delete_bodega_adr/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_bodega_adr'),
    
    # Gestión de Azotea
    path('azotea_adr/', login_required(AzoteaView.as_view()), name="azotea_adr"),
    path('add_azotea_adr/', login_required(AddAzoteaView.as_view()), name="add_azotea_adr"),
    path('edit_azotea_adr/<int:pk>/', login_required(Edit_AzoteaView.as_view()), name='edit_azotea_adr'),
    path('delete_azotea_adr/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_azotea_adr'),

    # Gestión de Monitores
    path('monitor_list/', login_required(MonitorView.as_view()), name="monitor_list"),
    path('add_monitor/', login_required(AddMonitorView.as_view()), name="add_monitor"),
    path('edit_monitor/<int:pk>/', login_required(EditMonitorView.as_view()), name="edit_monitor"),
    path('delete_monitor/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_monitor'),
    path('detalle_monitor/<int:pk>/', views.MonitorDetailView.as_view(), name='detalle_monitor'),

    # Gestión de Audio
    path('audio_list/', login_required(AudioView.as_view()), name="audio_list"),
    path('add_audio/', login_required(AddAudioView.as_view()), name="add_audio"),
    path('edit_audio/<int:pk>/', login_required(EditAudioView.as_view()), name="edit_audio"),
    path('delete_audio/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_audio'),
    path('detalle_audio/<int:pk>/', views.AudioDetailView.as_view(), name='detalle_audio'),

    # Gestión de Tablets
    path('tablet_list/', login_required(TabletView.as_view()), name="tablet_list"),
    path('add_tablet/', login_required(AddTabletView.as_view()), name="add_tablet"),
    path('edit_tablet/<int:pk>/', login_required(EditTabletView.as_view()), name="edit_tablet"),
    path('delete_tablet/<str:model_name>/<int:pk>/', login_required(DeleteToEliminadosView.as_view()), name='delete_tablet'),
    path('detalle_tablet/<int:pk>/', views.TabletDetailView.as_view(), name='detalle_tablet'),
    
    # Utilidades
    path('descargar_excel/excel/<str:model_name>/', login_required(DescargarExcelView.as_view()), name="descargar_excel"),
    path('upload_excel_allinone/', login_required(UploadExcelAllInOneView.as_view()), name='upload_excel_allinone'),
    path('upload_excel_notebook/', login_required(UploadExcelNotebookView.as_view()), name='upload_excel_notebook'),
    path('upload_excel_proyector/', login_required(UploadExcelProyectorView.as_view()), name='upload_excel_proyector'),
    path('upload_excel_minipc/', login_required(UploadExcelMiniPCView.as_view()), name='upload_excel_minipc'),
    path('upload_excel_allinoneadm/', login_required(UploadExcelAllInOneAdmView.as_view()), name='upload_excel_allinoneadm'),
    path('upload_excel_bodega_adr/', login_required(UploadExcelBodegaADRView.as_view()), name='upload_excel_bodega_adr'),
    path('upload_excel_azotea/', login_required(UploadExcelAzoteaView.as_view()), name='upload_excel_azotea'),

    path('upload_excel_monitor/', login_required(views.UploadExcelMonitorView.as_view()), name='upload_excel_monitor'),
    path('upload_excel_audio/', login_required(views.UploadExcelAudioView.as_view()), name='upload_excel_audio'),
    path('upload_excel_tablet/', login_required(views.UploadExcelTabletView.as_view()), name='upload_excel_tablet'),
    path('upload_success/', TemplateView.as_view(template_name="upload_success.html"), name='upload_success'),
    path('historial/', login_required(HistorialCambiosView.as_view()), name='historial'),
    path('historial/<str:model_name>/<int:object_id>/', login_required(HistorialCambiosView.as_view()), name='historial_objeto'),


# Rutas nuevas para las vistas de detalle
    path('detalle_allinone/<int:pk>/', views.AllInOneDetailView.as_view(), name='detalle_allinone'),
    path('detalle_allinone_admin/<int:pk>/', views.AllInOneAdminDetailView.as_view(), name='detalle_allinone_admin'),
    path('detalle_notebook/<int:pk>/', views.NotebookDetailView.as_view(), name='detalle_notebook'),
    path('detalle_minipc/<int:pk>/', views.MiniPCDetailView.as_view(), name='detalle_minipc'),
    path('detalle_proyector/<int:pk>/', views.ProyectorDetailView.as_view(), name='detalle_proyector'),
    path('detalle_bodegaadr/<int:pk>/', views.BodegaADRDetailView.as_view(), name='detalle_bodegaadr'),
    path('detalle_azotea/<int:pk>/', views.AzoteaDetailView.as_view(), name='detalle_azotea'),
    # Las URLs de detalle para Monitor, Audio y Tablet ya se agregaron arriba con sus respectivos bloques.
    
    # URL para la vista de detalle de activo desde búsqueda global
    path('detalle_activo/<str:model_name>/<int:pk>/', views.detalle_activo_busqueda, name='detalle_activo_busqueda'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)