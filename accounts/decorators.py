from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def get_group_and_color(user):
    """
    Obtiene el grupo del usuario y devuelve información relacionada
    Returns: (group_id, group_name, group_name_singular, color)
    """
    if not user.groups.exists():
        return None, None, None, None
    
    group = user.groups.first()
    group_name = group.name
    
    # Mapeo de grupos a colores
    color_map = {
        'ADR': 'amber',
        'Operadores ADR': 'red',
        'Auxiliares Operadores ADR': 'fuchsia',
        'Usuario': 'gray'
    }
    
    # Conversión de plural a singular
    singular_map = {
        'ADR': 'ADR',
        'Operadores ADR': 'Operador ADR',
        'Auxiliares Operadores ADR': 'Auxiliar Operador ADR',
        'Usuario': 'Usuario'
    }
    
    color = color_map.get(group_name, 'gray')
    group_name_singular = singular_map.get(group_name, group_name)
    
    return group.id, group_name, group_name_singular, color

def add_group_name_to_context(view_func):
    """
    Decorador que añade el nombre del grupo al contexto
    """
    @wraps(view_func)
    def _wrapped_view(view_instance, *args, **kwargs):
        response = view_func(view_instance, *args, **kwargs)
        
        # Solo procesar si hay un usuario y es una respuesta con contexto
        if hasattr(view_instance, 'request') and hasattr(response, 'context_data'):
            user = view_instance.request.user
            if user.is_authenticated and user.groups.exists():
                group = user.groups.first()
                group_id, group_name, group_name_singular, color = get_group_and_color(user)
                
                response.context_data.update({
                    'group_name': group_name,
                    'group_name_singular': group_name_singular,
                    'color': color
                })
        
        return response
    return _wrapped_view