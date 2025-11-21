from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_article_options_alter_comment_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=32)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('city', models.CharField(blank=True, default='', max_length=32)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_hidden', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': '留言',
                'verbose_name_plural': '留言',
            },
        ),
    ]