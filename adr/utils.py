# profiles/utils.py
from io import BytesIO
from uuid import uuid4
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
def make_avatar_square(django_file, size=512, fmt="WEBP", quality=86):
    """
    - Corrige orientación EXIF
    - Recorte centrado a cuadrado
    - Redimensiona con LANCZOS
    - Exporta a WEBP (o JPEG)
    """
    img = Image.open(django_file)
    img = ImageOps.exif_transpose(img)     # corrige orientación
    img = img.convert("RGB")

    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top  = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize((size, size), Image.LANCZOS)

    buf = BytesIO()
    if fmt.upper() == "WEBP":
        img.save(buf, "WEBP", quality=quality, method=6)
        ext = "webp"
    else:
        img.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
        ext = "jpg"

    name = f"avatar_{uuid4().hex}.{ext}"
    return ContentFile(buf.getvalue(), name=name)

def enviar_notificacion_asunto(asunto: str, mensaje: str, destinatarios: list[str], from_email: str | None = None):
    """
    Envía un correo en TEXTO PLANO.
    """
    send_mail(
        subject=asunto,
        message=mensaje,
        from_email=from_email or getattr(settings, "DEFAULT_FROM_EMAIL", None),
        recipient_list=destinatarios,
        fail_silently=False,
    )