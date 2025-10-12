from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apconect', '0004_anuncio_endereco_exibicao_mensagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='anuncio',
            name='imagem_url',
            field=models.URLField(blank=True, max_length=1000, null=True),
        ),
    ]
