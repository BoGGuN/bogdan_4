import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app import models

# 1
print(models.Profile.objects.all())
for element in models.Profile.objects.all():
    print(element.name)
print(models.Comment.objects.all())
for element in models.Comment.objects.all():
    print(f'{element.author} - {element.text}')
print(models.Item.objects.all())
for element in models.Item.objects.all():
    print(f'{element.type} - {element.name}')