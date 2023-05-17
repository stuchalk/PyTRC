from django.db import models


class Journals(models.Model):
    name = models.CharField(max_length=256)
    coden = models.CharField(max_length=128, blank=True, null=True)
    issn = models.CharField(max_length=9, blank=True, null=True)
    set = models.CharField(max_length=8, blank=True, null=True)
    language = models.CharField(max_length=201)
    abbrev = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, blank=True, null=True)
    homepage = models.CharField(max_length=255, blank=True, null=True)
    doiprefix = models.CharField(max_length=100, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'journals'
        app_label = 'journals'


class References(models.Model):
    id = models.SmallAutoField(primary_key=True)
    journal = models.ForeignKey(Journals, models.DO_NOTHING)
    authors = models.CharField(max_length=2048, blank=True, null=True)
    aulist = models.CharField(max_length=2048, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    volume = models.CharField(max_length=12, blank=True, null=True)
    issue = models.CharField(max_length=16, blank=True, null=True)
    startpage = models.CharField(max_length=16, blank=True, null=True)
    endpage = models.CharField(max_length=16, blank=True, null=True)
    title = models.CharField(max_length=1024, blank=True, null=True)
    doi = models.CharField(max_length=256)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'references'
        app_label = 'references'
