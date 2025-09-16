def group_and_user(request):
    if request.user.is_authenticated:
        group = (request.user.groups.first().name
                 if request.user.groups.exists() else "Usuario")
        return {
            "group_name_singular": group,
            "user_profile": request.user,   # si tu navbar muestra el avatar
        }
    return {}