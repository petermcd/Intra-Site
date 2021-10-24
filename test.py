# Turn off bytecode generation
import sys
sys.dont_write_bytecode = True

# Django specific settings
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Intranet.settings')
import django
django.setup()

# Import your models for use in your script
from settings.models import Setting

""" Replace the code below with your own """

a = Setting.objects.all()

for b in a:
    print(b.name)
