from django.core.management.base import NoArgsCommand
from django.core.management import call_command
from django.db import connection
from django.conf import settings

import sys, os, subprocess, shutil

class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        self.dropdb()
        self.createdb()
        self.delete_migrations()

        # add the commands you want to run when the database is nuked.
        commands = [{'makemigrations':None,},
                    {'migrate':None,},
                   ]

        for c in commands:
            for key,value in c.items():
                if value:
                    call_command(key, value)
                else:
                    call_command(key)

    #==============================================================================#

    def dropdb(self):

        cmd = "dropdb %s" % settings.DATABASES['default']['NAME']

        dropped = subprocess.call(cmd, shell=True)

        if dropped == 0:
            print "Database has been dropped\n"
            return
        print "Database has not been dropped. Likely because it doesn't exist.\n"

    #==============================================================================#

    def createdb(self):

        cmd = "createdb %s" % settings.DATABASES['default']['NAME']

        created = subprocess.call(cmd, shell=True)

        if created == 0:

            print "Database has been created successfully"
            return
        print "Database has not been created successfully.\n Aborting..."
        sys.exit(1)

    #==============================================================================#

    def delete_migrations(self):
        """
        This script goes through the migration directories of this PROJECT'S apps
        and deletes the scripts to reset the database back to point 0.

        Applications must be in the "apps directory"
        """
        for app in settings.PROJECT_APPS:

            path = os.path.join(settings.BASE_DIR, 'apps', app, 'migrations')

            if os.path.exists(path):

                if len(os.listdir(path)) == 0:
                    os.rmdir(path)
                else:
                    shutil.rmtree(path)

            os.makedirs(path)
            open(os.path.join(path,"__init__.py"),'w').close()

    #==============================================================================#
