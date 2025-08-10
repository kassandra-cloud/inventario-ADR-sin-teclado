def plural_singular(name):
    """
    Convierte nombres de grupos de plural a singular
    """
    mapping = {
        'ADR': 'ADR',
        'Operadores ADR': 'Operador ADR',
        'Auxiliares Operadores ADR': 'Auxiliar Operador ADR',
        'Usuario': 'Usuario'
    }
    return mapping.get(name, name)