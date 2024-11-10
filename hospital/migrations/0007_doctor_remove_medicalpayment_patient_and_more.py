# Generated by Django 5.1.1 on 2024-10-27 13:58

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0006_product_created_at_alter_product_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('specialty', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.TextField(blank=True)),
                ('years_of_experience', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='medicalpayment',
            name='patient',
        ),
        migrations.RemoveField(
            model_name='medicalpayment',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='medicalpayment',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='medicalpayment',
            name='payment_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hospital.patient')),
                ('products', models.ManyToManyField(to='hospital.product')),
            ],
        ),
        migrations.AddField(
            model_name='medicalpayment',
            name='voucher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='hospital.voucher'),
        ),
    ]