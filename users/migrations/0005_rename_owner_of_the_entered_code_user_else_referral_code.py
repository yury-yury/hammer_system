# Generated by Django 4.2.4 on 2023-08-21 01:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_else_referral_code_user_owner_of_the_entered_code_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='owner_of_the_entered_code',
            new_name='else_referral_code',
        ),
    ]