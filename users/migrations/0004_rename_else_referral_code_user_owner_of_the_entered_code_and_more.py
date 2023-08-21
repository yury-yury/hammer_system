# Generated by Django 4.2.4 on 2023-08-20 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_user_is_referral_code_activated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='else_referral_code',
            new_name='owner_of_the_entered_code',
        ),
        migrations.AlterField(
            model_name='callbacktoken',
            name='key',
            field=models.CharField(default='1234', max_length=4),
        ),
    ]
