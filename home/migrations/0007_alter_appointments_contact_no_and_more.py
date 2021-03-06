# Generated by Django 4.0.4 on 2022-06-25 14:16

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_appointments_date_time_fixed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='contact_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
        migrations.AlterField(
            model_name='testimonial',
            name='contact_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]
