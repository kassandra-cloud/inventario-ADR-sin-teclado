import os
import gzip
import shutil
import subprocess
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Realiza un backup de MySQL con mysqldump, comprime y envía por correo.'

    def handle(self, *args, **kwargs):
        # Carpeta de backups
        os.makedirs(settings.BACKUP_DIR, exist_ok=True)

        # Credenciales desde ENV; fallback a settings.DATABASES["default"]
        db = settings.DATABASES.get("default", {})
        mysql_host = os.getenv("MYSQL_HOST", db.get("HOST", "localhost"))
        mysql_user = os.getenv("MYSQL_USER", db.get("USER", "root"))
        mysql_pass = os.getenv("MYSQL_PASSWORD", db.get("PASSWORD", ""))
        mysql_db   = os.getenv("MYSQL_DATABASE", db.get("NAME", ""))

        # Nombres de archivo
        ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        sql_path = os.path.join(settings.BACKUP_DIR, f"backup_{mysql_db}_{ts}.sql")
        gz_path  = f"{sql_path}.gz"

        # Comando mysqldump
        cmd = [
            "mysqldump",
            "-h", mysql_host,
            "-u", mysql_user,
            f"-p{mysql_pass}",
            "--no-tablespaces",
            mysql_db,
        ]

        # Ejecutar dump
        try:
            with open(sql_path, "wb") as out:
                subprocess.run(cmd, stdout=out, stderr=subprocess.PIPE, check=True)
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error en mysqldump: {e.stderr.decode(errors='ignore') if e.stderr else e}")
            return

        # Comprimir y limpiar .sql
        try:
            with open(sql_path, "rb") as fin, gzip.open(gz_path, "wb") as fout:
                shutil.copyfileobj(fin, fout)
        finally:
            if os.path.exists(sql_path):
                os.remove(sql_path)

        # Enviar por correo
        try:
            self._send_backup_email(gz_path, mysql_db, ts)
        except Exception as e:
            self.stderr.write(f"Error al enviar correo: {e}")
            return

        self.stdout.write(self.style.SUCCESS(f"Backup generado y enviado: {gz_path}"))

    def _send_backup_email(self, file_path: str, dbname: str, ts: str) -> None:
        subject = f"Backup {dbname} - {ts}"
        body = f"Adjunto backup de {dbname} generado el {ts}."

        # EMAIL_RECIPIENTS puede ser lista o string con comas (vía entorno/settings)
        recipients = settings.EMAIL_RECIPIENTS
        if isinstance(recipients, str):
            recipients = [x.strip() for x in recipients.split(",") if x.strip()]

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=recipients,
        )
        email.attach_file(file_path)
        email.send(fail_silently=False)
