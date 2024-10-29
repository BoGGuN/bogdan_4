# Generated by Django 5.1.2 on 2024-10-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('type', models.CharField(blank=True, choices=[('default', 'Неизвестно'), ('toy', 'Игрушка'), ('food', 'Еда')], default='default', max_length=255)),
            ],
            options={
                'verbose_name': 'Вещь',
                'verbose_name_plural': 'Вещи',
                'ordering': ['-type', '-name'],
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='purchased_items',
            field=models.ManyToManyField(blank=True, related_name='items', to='app.item', verbose_name='Корзина'),
        ),
    ]