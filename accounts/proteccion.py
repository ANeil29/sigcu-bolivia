"""
Protección del usuario fundador del sistema.
Este usuario NO puede ser editado, desactivado, eliminado
ni visualizado por ningún otro usuario, sin importar su rol.
"""

# ID del usuario protegido 
USUARIO_PROTEGIDO_ID = 1 

# Username como respaldo adicional
USUARIO_PROTEGIDO_USERNAME = 'SUPERADMIN'  


def es_usuario_protegido(usuario):
    """Devuelve True si el usuario dado es el usuario fundador protegido."""
    if usuario is None:
        return False
    return (
        usuario.pk       == USUARIO_PROTEGIDO_ID or
        usuario.username == USUARIO_PROTEGIDO_USERNAME
    )


def puede_gestionar(solicitante, objetivo):
    """
    Devuelve True si el solicitante puede gestionar al usuario objetivo.
    Reglas:
    - El usuario protegido SOLO puede ser gestionado por sí mismo.
    - Ningún otro usuario puede tocar al protegido.
    - El usuario protegido puede gestionar a cualquiera.
    """
    if es_usuario_protegido(objetivo):
        
        return solicitante.pk == USUARIO_PROTEGIDO_ID
    return True