from django.contrib import admin
from .models import AllInOne, AllInOneAdmins, Notebook, MiniPC, Proyectores, Azotea, BodegaADR, Monitor, Audio, Tablet

@admin.register(AllInOne)
class AllInOneAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'netbios', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(AllInOneAdmins)
class AllInOneAdminAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'netbios', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(Notebook)
class NotebookAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'asignado_a', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'netbios', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(MiniPC)
class MiniPCAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(Proyectores)
class ProyectoresAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(Azotea)
class AzoteaAdmin(admin.ModelAdmin):
    list_display = ('activo', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(BodegaADR)
class BodegaADRAdmin(admin.ModelAdmin):
    list_display = ('activo', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'netbios', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(Audio)
class AudioAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'ubicacion', 'creado_por', 'fecha_creacion')

@admin.register(Tablet)
class TabletAdmin(admin.ModelAdmin):
    list_display = ('activo', 'estado', 'marca', 'modelo', 'n_serie', 'unive', 'bdo', 'netbios', 'ubicacion', 'creado_por', 'fecha_creacion')
