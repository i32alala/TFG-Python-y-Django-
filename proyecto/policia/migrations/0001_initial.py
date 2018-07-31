# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acto',
            fields=[
                ('idActo', models.AutoField(serialize=False, primary_key=True)),
                ('nombreActo', models.CharField(max_length=200)),
                ('fechaActo', models.DateField(null=True, blank=True)),
                ('descripcionActo', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActoPersona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('orden', models.IntegerField(default=b'-1', max_length=9, null=True, help_text=b'Orden en la lista de protocolo')),
                ('asistencia', models.BooleanField(default=0)),
                ('acto', models.ForeignKey(to='policia.Acto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ActoSala',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acto', models.ForeignKey(to='policia.Acto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Asiento',
            fields=[
                ('idAsiento', models.AutoField(serialize=False, primary_key=True)),
                ('numAsiento', models.IntegerField(max_length=9)),
                ('filaAsiento', models.IntegerField(default=0)),
                ('columnaAsiento', models.IntegerField(max_length=3, null=True)),
                ('idActo', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='policia.Acto', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Etiqueta',
            fields=[
                ('idEtiqueta', models.AutoField(serialize=False, primary_key=True)),
                ('nombreEtiqueta', models.CharField(max_length=200)),
                ('parteAbajo', models.CharField(max_length=200)),
                ('parteArriba', models.CharField(max_length=200)),
                ('gorro', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invitaciones',
            fields=[
                ('idInvitaciones', models.AutoField(serialize=False, primary_key=True)),
                ('nombreInvitacion', models.CharField(max_length=200)),
                ('pdf', models.FileField(null=True, upload_to=b'media/', blank=True)),
                ('archivo', models.FileField(null=True, upload_to=b'media/', blank=True)),
                ('idActo', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Acto', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('titulo', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organismo',
            fields=[
                ('idOrganismo', models.AutoField(serialize=False, primary_key=True)),
                ('nombreOrganismo', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonaOrganismo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cargo', models.CharField(help_text=b'Crargo de la persona en el Organismo', max_length=200, null=True)),
                ('nombreOrganismo', models.CharField(help_text=b'Crargo de la persona en el Organismo', max_length=200, null=True)),
                ('idOrganismo', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Organismo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='personaRol',
            fields=[
                ('idRol', models.AutoField(serialize=False, primary_key=True)),
                ('rol', models.CharField(max_length=200)),
                ('orden', models.IntegerField(max_length=200, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Personas',
            fields=[
                ('idPersona', models.AutoField(serialize=False, primary_key=True)),
                ('nombrePersona', models.CharField(max_length=200)),
                ('apellido', models.CharField(max_length=200, null=True)),
                ('correo', models.EmailField(max_length=75)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.personaRol', null=True)),
                ('idOrganismo', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Organismo', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('idSala', models.IntegerField(serialize=False, primary_key=True)),
                ('nombreSala', models.CharField(help_text=b'Introduzca el nombre de la sala', max_length=200)),
                ('numAsientos', models.IntegerField(default=0)),
                ('descripcionSala', models.CharField(help_text=b'Descriva brevemente el acto', max_length=200)),
                ('imagenSala', models.ImageField(null=True, upload_to=b'img', blank=True)),
                ('media', models.FileField(null=True, upload_to=b'archivos/', blank=True)),
                ('numFilas', models.IntegerField(max_length=200, null=True)),
                ('numColumnas', models.IntegerField(max_length=200, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='personarol',
            unique_together=set([('rol', 'orden')]),
        ),
        migrations.AddField(
            model_name='personaorganismo',
            name='idPersona',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Personas', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='noticia',
            name='tags',
            field=models.ManyToManyField(to='policia.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asiento',
            name='idSala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Sala', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='actosala',
            name='idSala',
            field=models.ForeignKey(to='policia.Sala'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='actosala',
            unique_together=set([('acto', 'idSala')]),
        ),
        migrations.AddField(
            model_name='actopersona',
            name='person',
            field=models.ForeignKey(to='policia.Personas'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='actopersona',
            unique_together=set([('acto', 'person')]),
        ),
        migrations.AddField(
            model_name='acto',
            name='idEtiqueta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Etiqueta', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='acto',
            name='idSala',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='policia.Sala', null=True),
            preserve_default=True,
        ),
    ]
