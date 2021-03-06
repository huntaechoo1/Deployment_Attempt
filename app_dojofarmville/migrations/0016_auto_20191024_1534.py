# Generated by Django 2.2.6 on 2019-10-24 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_dojofarmville', '0015_auto_20191024_1447'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blacktomato',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='blacktomato',
            name='user',
        ),
        migrations.RemoveField(
            model_name='blacktomatoseed',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='blacktomatoseed',
            name='user',
        ),
        migrations.RemoveField(
            model_name='carrot',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='carrot',
            name='user',
        ),
        migrations.RemoveField(
            model_name='carrotseed',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='carrotseed',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='corn',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='corn',
            name='user',
        ),
        migrations.RemoveField(
            model_name='cornseed',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='cornseed',
            name='user',
        ),
        migrations.RemoveField(
            model_name='event',
            name='attender',
        ),
        migrations.RemoveField(
            model_name='event',
            name='uploader',
        ),
        migrations.RemoveField(
            model_name='farm',
            name='user',
        ),
        migrations.RemoveField(
            model_name='leek',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='leek',
            name='user',
        ),
        migrations.RemoveField(
            model_name='leekseed',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='leekseed',
            name='user',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.RemoveField(
            model_name='wheat',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='wheat',
            name='user',
        ),
        migrations.RemoveField(
            model_name='wheatseed',
            name='farm',
        ),
        migrations.RemoveField(
            model_name='wheatseed',
            name='user',
        ),
        migrations.DeleteModel(
            name='Badge',
        ),
        migrations.DeleteModel(
            name='BlackTomato',
        ),
        migrations.DeleteModel(
            name='BlackTomatoSeed',
        ),
        migrations.DeleteModel(
            name='Carrot',
        ),
        migrations.DeleteModel(
            name='CarrotSeed',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='Corn',
        ),
        migrations.DeleteModel(
            name='CornSeed',
        ),
        migrations.DeleteModel(
            name='Event',
        ),
        migrations.DeleteModel(
            name='Farm',
        ),
        migrations.DeleteModel(
            name='Leek',
        ),
        migrations.DeleteModel(
            name='LeekSeed',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.DeleteModel(
            name='Wheat',
        ),
        migrations.DeleteModel(
            name='WheatSeed',
        ),
    ]
