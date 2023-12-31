# Generated by Django 4.2.4 on 2023-09-27 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_is_draft'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='publish_status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10),
        ),
    ]
