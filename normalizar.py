from pathlib import Path
from PIL import Image, ImageChops, ImageOps

# === Rutas (no cambies si tu estructura es la misma) ===
SRC = Path("static/imagenes")                  # originales
DST = Path("static/imagenes_normalizadas")     # salida
DST.mkdir(parents=True, exist_ok=True)

# === Parámetros ===
TARGET   = 512   # tamaño del lienzo cuadrado final
MARGIN   = 32    # margen interior
TOLERANCE_WHITE = 230  # 0..255 (230–245 funciona bien). A mayor valor, más “casi blanco” se hace transparente

# (Opcional) alias para renombrar a nombres cortos
ALIASES = [
    (("monitor",),                     "monitor.png"),
    (("ipad", "tablet"),               "tablet.png"),
    (("speaker", "audio", "event"),    "eventos.png"),
]

def out_name_from_stem(stem: str) -> str:
    s = stem.lower()
    for keywords, outname in ALIASES:
        if any(k in s for k in keywords):
            return outname
    safe = stem[:80]
    return f"{safe}.png"

def white_to_alpha(img: Image.Image, tol: int) -> Image.Image:
    """Convierte a transparente los píxeles blancos o casi blancos."""
    rgba = img.convert("RGBA")
    rgb  = rgba.convert("RGB")

    # Diferencia con blanco puro
    diff = ImageChops.difference(rgb, Image.new("RGB", rgb.size, (255, 255, 255)))
    # Valores altos => más cercanos a blanco
    inv  = ImageOps.invert(ImageOps.grayscale(diff))

    # Máscara: > tol -> transparentar
    mask = inv.point(lambda p: 255 if p > tol else 0, mode="1")

    alpha = rgba.split()[-1]
    alpha = ImageChops.subtract(alpha, mask.convert("L"))
    rgba.putalpha(alpha)
    return rgba

def normalizar(path: Path):
    im = Image.open(path)

    # 1) Fondo blanco -> transparente (si lo hay)
    im = white_to_alpha(im, TOLERANCE_WHITE)

    # 2) Recorte por alfa
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)

    # 3) Escalado para que quepa con margen
    max_side = TARGET - 2 * MARGIN
    w, h = im.size
    scale = min(max_side / w, max_side / h) if w and h else 1.0
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    im = im.resize(new_size, Image.LANCZOS)

    # 4) Lienzo y centrado
    canvas = Image.new("RGBA", (TARGET, TARGET), (0, 0, 0, 0))
    x = (TARGET - im.width) // 2
    y = (TARGET - im.height) // 2
    canvas.paste(im, (x, y), im)

    # 5) Guardar siempre como PNG (nombre corto si aplica)
    out = DST / out_name_from_stem(path.stem)
    canvas.save(out, format="PNG", optimize=True)
    print(f"✅ {path.name} -> {out.name}")

def main():
    formatos = {".png", ".jpg", ".jpeg", ".webp", ".ico"}
    for p in SRC.iterdir():
        if p.is_file() and p.suffix.lower() in formatos:
            normalizar(p)

if __name__ == "__main__":
    main()
