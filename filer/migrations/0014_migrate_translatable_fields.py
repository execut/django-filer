# Generated by Django 3.0.11 on 2021-01-31 11:30

from django.db import migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def forwards_func(apps, schema_editor):
    File = apps.get_model('filer', 'File')
    FileTranslation = apps.get_model('filer', 'FileTranslation')

    for object in File.objects.all():
        FileTranslation.objects.create(
            master_id=object.pk,
            language_code=settings.LANGUAGE_CODE,
            name=object.name,
            description=object.description,
        )

    Image = apps.get_model('filer', 'Image')
    ImageTranslation = apps.get_model('filer', 'ImageTranslation')

    for object in Image.objects.all():
        ImageTranslation.objects.create(
            master_id=object.pk,
            language_code=settings.LANGUAGE_CODE,
            default_alt_text=object.default_alt_text,
            default_caption=object.default_caption,
            author=object.author,
        )

def backwards_func(apps, schema_editor):
    File = apps.get_model('filer', 'File')
    FileTranslation = apps.get_model('filer', 'FileTranslation')

    for object in File.objects.all():
        translation = _get_translation(object, FileTranslation)
        object.name = translation.name
        object.description = translation.description
        object.save()

    Image = apps.get_model('filer', 'Image')
    ImageTranslation = apps.get_model('filer', 'ImageTranslation')

    for object in Image.objects.all():
        translation = _get_translation(object, ImageTranslation)
        object.default_alt_text = translation.default_alt_text
        object.default_caption = translation.default_caption
        object.author = translation.author
        object.save()

def _get_translation(object, FileTranslation):
    translations = FileTranslation.objects.filter(master_id=object.pk)
    try:
        # Try default translation
        return translations.get(language_code=settings.LANGUAGE_CODE)
    except ObjectDoesNotExist:
        try:
            # Try default language
            return translations.get(language_code=settings.PARLER_DEFAULT_LANGUAGE_CODE)
        except ObjectDoesNotExist:
            # Maybe the object was translated only in a specific language?
            # Hope there is a single translation
            return translations.get()


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0013_add_translations_tables'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
