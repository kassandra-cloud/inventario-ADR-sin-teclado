import logging
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from adr.models import Notebook

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Populates the creado_por field for existing Notebooks that have it as null.'

    def handle(self, *args, **options):
        User = get_user_model()

        try:
            # Get a user from the 'ADR' group
            from django.contrib.auth.models import Group
            adr_group = Group.objects.get(name='ADR')
            user_to_assign = adr_group.user_set.first()

            if not user_to_assign:
                 self.stdout.write(self.style.ERROR('No user found in "ADR" group. Aborting.'))
                 return
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('Group "ADR" does not exist. Aborting.'))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error fetching user from "ADR" group: {e}. Aborting.'))
            return

        self.stdout.write(self.style.SUCCESS(f'Attempting to populate creado_por for Notebooks with user from "ADR" group ("{user_to_assign.username}")...'))

        notebooks_to_update = Notebook.objects.filter(creado_por__isnull=True)
        updated_count = 0

        for notebook in notebooks_to_update:
            notebook.creado_por = user_to_assign
            notebook.save()
            updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} Notebooks.'))