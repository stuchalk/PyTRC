from django.db import models


# Create your models here.
class Nspaces(models.Model):
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=64)
    ns = models.CharField(max_length=8)
    path = models.CharField(unique=True, max_length=128)
    homepage = models.CharField(max_length=128)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'nspaces'
        app_label = 'nspaces'

class Ontterms(models.Model):
    id = models.SmallAutoField(primary_key=True)
    title = models.CharField(max_length=256)
    definition = models.CharField(max_length=2048, blank=True, null=True)
    code = models.CharField(max_length=64)
    url = models.CharField(max_length=512)
    nspace = models.ForeignKey(Nspaces, models.DO_NOTHING, db_column='nspace_id')
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=64, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ontterms'
        app_label = 'ontterms'


class Crosswalks(models.Model):
    context_id = models.SmallIntegerField()
    dataset_id = models.SmallIntegerField()
    table = models.CharField(max_length=128)
    field = models.CharField(max_length=256)
    ontterm = models.ForeignKey(Ontterms, models.DO_NOTHING, db_column='ontterm_id')
    sdsection = models.CharField(max_length=11, blank=True, null=True)
    sdsubsection = models.CharField(max_length=128, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'crosswalks'
        app_label = 'crosswalks'
