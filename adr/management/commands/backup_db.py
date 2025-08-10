import os
import subprocess
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
from django.core.mail import EmailMessage

class Command(BaseCommand):
    help = 'Realiza un backup de la base de datos MySQL usando mysqldump y lo envía por correo.'

    def handle(self, *args, **kwargs):
        # Asegurarse de que la carpeta de backups exista
        os.makedirs(settings.BACKUP_DIR, exist_ok=True)

        # Construir el nombre del archivo de backup con la fecha
        backup_filename = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"
        backup_filepath = os.path.join(settings.BACKUP_DIR, backup_filename)

        # Comando mysqldump para generar el backup
        mysqldump_command = [
            "mysqldump",
            "-h", "bqgae94o8ggp92gzivzz-mysql.services.clever-cloud.com",  # Servidor
            "-u", "ufakmr6kpb5hin6z",  # Usuario
            "-p" + "DOJF2hPPvB02K39GiNe6",  # Contraseña (sin espacio entre -p y la contraseña)
            "--no-tablespaces",  # Evitar la exportación de tablas de espacios
            "bqgae94o8ggp92gzivzz"  # Nombre de la base de datos
        ]
        # Ejecutar el comando mysqldump y guardar el backup en el archivo
        try:
            with open(backup_filepath, 'wb') as f:
                subprocess.run(mysqldump_command, stdout=f, stderr=subprocess.PIPE, check=True)
            self.stdout.write(self.style.SUCCESS(f'Backup realizado exitosamente: {backup_filepath}'))
        except subprocess.CalledProcessError as e:
            self.stderr.write(f"Error al ejecutar mysqldump: {e}")
            return

        # Enviar el archivo de backup por correo
        self.send_backup_email(backup_filepath)

    def send_backup_email(self, backup_filepath):
        # Crear el correo con el archivo adjunto
        subject = f"Backup MySQL {datetime.now().strftime('%Y-%m-%d')}"
        body = "Adjunto tienes el backup de la base de datos."
        email = EmailMessage(subject, body, settings.EMAIL_HOST_USER, settings.EMAIL_RECIPIENTS)
        email.attach_file(backup_filepath)  # Adjuntar el archivo de backup

        try:
            # Enviar el correo
            email.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS("Correo enviado exitosamente a múltiples destinatarios."))
        except Exception as e:
            self.stderr.write(f"Error al enviar el correo: {e}")
