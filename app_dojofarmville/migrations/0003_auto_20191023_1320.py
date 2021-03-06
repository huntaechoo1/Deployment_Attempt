# Generated by Django 2.2.6 on 2019-10-23 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_dojofarmville', '0002_auto_20191023_1304'),
    ]

    operations = [
        migrations.CreateModel(
            name='Corn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crops', to='app_dojofarmville.Farm')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crops', to='app_dojofarmville.User')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Crop',
        ),
    ]
