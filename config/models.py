""" TRC project model definitions """
from django.db import models


class Journals(models.Model):
    """ journals table model """
    id = models.SmallAutoField(primary_key=True)
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
    """ references table model """
    id = models.SmallAutoField(primary_key=True)
    journal = models.ForeignKey(Journals, models.DO_NOTHING, db_column='journal_id')
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


class Substances(models.Model):
    """ substances table model """
    name = models.CharField(max_length=1024)
    type = models.CharField(max_length=9, blank=True, null=True)
    subtype = models.CharField(max_length=256, blank=True, null=True)
    formula = models.CharField(max_length=256)
    mw = models.CharField(max_length=16, blank=True, null=True)
    mwsrc = models.CharField(max_length=16, blank=True, null=True)
    inchikey = models.CharField(max_length=27, blank=True, null=True)
    files = models.PositiveSmallIntegerField(blank=True, null=True)
    systems = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'substances'
        app_label = 'substances'


class Identifiers(models.Model):
    """ identifiers table model """
    substance = models.ForeignKey(Substances, models.DO_NOTHING, db_column='substance_id')
    type = models.CharField(max_length=12)
    value = models.CharField(max_length=1024)
    source = models.CharField(max_length=8, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'identifiers'
        app_label = 'identifiers'


class Files(models.Model):
    """ files table model """
    trcid = models.CharField(max_length=32, blank=True, null=True)
    abstract = models.CharField(max_length=4096, blank=True, null=True)
    date = models.CharField(max_length=16, blank=True, null=True)
    year = models.TextField(blank=True, null=True)
    reference = models.ForeignKey(References, models.DO_NOTHING, db_column='reference_id')
    filename = models.CharField(max_length=128)
    points = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'files'
        app_label = 'files'


class Reports(models.Model):
    """ reports table model """
    title = models.CharField(max_length=512, blank=True, null=True)
    description = models.CharField(max_length=1024, blank=True, null=True)
    file = models.ForeignKey(Files, models.DO_NOTHING, blank=True, null=True, db_column='file_id')
    reference = models.ForeignKey(References, models.DO_NOTHING, blank=True, null=True, db_column='reference_id')
    points = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reports'
        app_label = 'reports'


class Keywords(models.Model):
    """ keywords table model """
    id = models.SmallAutoField(primary_key=True)
    report = models.ForeignKey(Reports, models.DO_NOTHING, blank=True, null=True, db_column='report_id')
    term = models.CharField(max_length=256, blank=True, null=True)
    chk = models.BooleanField(db_column='check')
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'keywords'
        app_label = 'keywords'


class Systems(models.Model):
    """ systems table model """
    name = models.CharField(max_length=300)
    composition = models.CharField(max_length=19, blank=True, null=True)
    identifier = models.CharField(unique=True, max_length=128)
    refcnt = models.PositiveSmallIntegerField(blank=True, null=True)
    setcnt = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'systems'
        app_label = 'systems'


class SubstancesSystems(models.Model):
    """ substances_system join table model """
    substance = models.ForeignKey(Substances, models.DO_NOTHING, db_column='substance_id')
    system = models.ForeignKey(Systems, models.DO_NOTHING, db_column='system_id')
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'substances_systems'
        app_label = 'substances_systems'


class Datasets(models.Model):
    """ journals table model """
    title = models.CharField(max_length=512, blank=True, null=True)
    setnum = models.PositiveSmallIntegerField(blank=True, null=True)
    file = models.ForeignKey(Files, models.DO_NOTHING, blank=True, null=True, db_column='file_id')
    report = models.ForeignKey(Reports, models.DO_NOTHING, blank=True, null=True, db_column='report_id')
    system = models.ForeignKey(Systems, models.DO_NOTHING, blank=True, null=True, db_column='system_id')
    reference = models.ForeignKey(References, models.DO_NOTHING, blank=True, null=True, db_column='reference_id')
    trcidset_id = models.CharField(max_length=32, blank=True, null=True)
    points = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'datasets'
        app_label = 'datasets'


class Dataseries(models.Model):
    """ dataseries table model """
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, db_column='dataset_id')
    idx = models.PositiveSmallIntegerField()
    points = models.PositiveSmallIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'dataseries'
        app_label = 'dataseries'


class Datapoints(models.Model):
    """ datapoints table model """
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, blank=True, null=True, db_column='dataset_id')
    dataseries = models.ForeignKey(Dataseries, models.DO_NOTHING, blank=True, null=True, db_column='dataseries_id')
    row_index = models.CharField(max_length=10, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'datapoints'
        app_label = 'datapoints'


class Units(models.Model):
    """ units table model """
    name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=128)
    type = models.CharField(max_length=9)
    exact = models.IntegerField()
    factor = models.FloatField()
    si_equivalent = models.CharField(max_length=128)
    qudt = models.CharField(max_length=128)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'units'
        app_label = 'units'


class Quantitykinds(models.Model):
    """ quantitykinds table model """
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    altname = models.CharField(max_length=64, blank=True, null=True)
    symbol = models.CharField(max_length=64)
    definition = models.CharField(max_length=1024, blank=True, null=True)
    source = models.CharField(max_length=128, blank=True, null=True)
    si_unit = models.ForeignKey(Units, models.DO_NOTHING, db_column='si_unit')
    dim_symbol = models.CharField(max_length=64)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'quantitykinds'
        app_label = 'quantitykinds'


class Quantities(models.Model):
    """ quantities table model """
    id = models.SmallAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    phase = models.CharField(max_length=128, blank=True, null=True)
    field = models.CharField(max_length=256, blank=True, null=True)
    label = models.CharField(max_length=64)
    group = models.CharField(max_length=34, blank=True, null=True)
    vartype = models.CharField(max_length=21, blank=True, null=True)
    symbol = models.CharField(max_length=64, blank=True, null=True)
    definition = models.CharField(max_length=1024, blank=True, null=True)
    source = models.CharField(max_length=256, blank=True, null=True)
    kind = models.CharField(max_length=128, blank=True, null=True)
    quantitykind = models.ForeignKey(Quantitykinds, models.DO_NOTHING, db_column='quantitykind_id')
    defunit = models.ForeignKey(Units, models.DO_NOTHING, blank=True, null=True, db_column='defunit_id')
    condcnt = models.PositiveIntegerField(blank=True, null=True)
    datacnt = models.PositiveIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'quantities'
        app_label = 'quantities'


class Chemicals(models.Model):
    """ chemicals table model """
    file = models.ForeignKey(Files, models.DO_NOTHING, db_column='file_id')
    substance = models.ForeignKey(Substances, models.DO_NOTHING, blank=True, null=True, db_column='substance_id')
    orgnum = models.PositiveIntegerField()
    sourcetype = models.CharField(max_length=33, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'chemicals'
        app_label = 'chemicals'


class Mixtures(models.Model):
    """ mixtures table model """
    system = models.ForeignKey(Systems, models.DO_NOTHING, blank=True, null=True, db_column='system_id')
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, blank=True, null=True, db_column='dataset_id')
    updated = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mixtures'
        app_label = 'mixtures'
        unique_together = (('system', 'dataset'),)


class Components(models.Model):
    """ components table model """
    chemical = models.ForeignKey(Chemicals, models.DO_NOTHING, db_column='chemical_id')
    mixture = models.ForeignKey(Mixtures, models.DO_NOTHING, db_column='mixture_id')
    compnum = models.PositiveIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'components'
        app_label = 'components'


class Phasetypes(models.Model):
    """ phasetypes table model """
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=14, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'phasetypes'
        app_label = 'phasetypes'


class Phases(models.Model):
    """ phases table model """
    mixture = models.ForeignKey(Mixtures, models.DO_NOTHING, db_column='mixture_id')
    phasetype = models.ForeignKey(Phasetypes, models.DO_NOTHING, db_column='phasetype_id')
    orgnum = models.PositiveIntegerField(blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'phases'
        app_label = 'phases'


class Conditions(models.Model):
    """ conditions table model """
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, blank=True, null=True, db_column='dataset_id')
    dataseries = models.ForeignKey(Dataseries, models.DO_NOTHING, blank=True, null=True, db_column='dataseries_id')
    datapoint = models.ForeignKey(Datapoints, models.DO_NOTHING, blank=True, null=True, db_column='datapoint_id')
    quantity = models.ForeignKey(Quantities, models.DO_NOTHING, blank=True, null=True, db_column='quantity_id')
    system = models.ForeignKey(Systems, models.DO_NOTHING, blank=True, null=True, db_column='system_id')
    component = models.ForeignKey(Components, models.DO_NOTHING, blank=True, null=True, db_column='component_id')
    phase = models.ForeignKey(Phases, models.DO_NOTHING, blank=True, null=True, db_column='phase_id')
    number = models.TextField(blank=True, null=True)
    significand = models.TextField(blank=True, null=True)
    exponent = models.TextField(blank=True, null=True)
    unit = models.ForeignKey(Units, models.DO_NOTHING, blank=True, null=True, db_column='unit_id')
    accuracy = models.IntegerField(blank=True, null=True)
    exact = models.IntegerField()
    text = models.CharField(max_length=128, blank=True, null=True)
    issue = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'conditions'
        app_label = 'conditions'

    @property
    def nval(self):
        man = self.significand
        pwr = self.exponent
        return man * pow(10, pwr)


class Sampleprops(models.Model):
    """ sampleprops table model """
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, db_column='dataset_id')
    propnum = models.CharField(max_length=256, blank=True, null=True)
    orgnum = models.CharField(max_length=256, blank=True, null=True)
    quantity_group = models.CharField(max_length=256, blank=True, null=True)
    quantity_name = models.CharField(max_length=256, blank=True, null=True)
    quantity = models.ForeignKey(Quantities, models.DO_NOTHING, blank=True, null=True)
    unit = models.ForeignKey(Units, models.DO_NOTHING, blank=True, null=True)
    method_name = models.CharField(max_length=256, blank=True, null=True)
    phase = models.CharField(max_length=256, blank=True, null=True)
    presentation = models.CharField(max_length=256, blank=True, null=True)
    solventorgnum = models.CharField(max_length=256, blank=True, null=True)
    uncnum = models.CharField(max_length=256, blank=True, null=True)
    unceval = models.CharField(max_length=256, blank=True, null=True)
    uncconf = models.CharField(max_length=8, blank=True, null=True)
    uncchk = models.CharField(max_length=3)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'sampleprops'
        app_label = 'sampleprops'


class Data(models.Model):
    """ data table model """
    dataset = models.ForeignKey(Datasets, models.DO_NOTHING, blank=True, null=True, db_column='dataset_id')
    dataseries = models.ForeignKey(Dataseries, models.DO_NOTHING, blank=True, null=True, db_column='dataseries_id')
    datapoint = models.ForeignKey(Datapoints, models.DO_NOTHING, blank=True, null=True, db_column='datapoint_id')
    quantity = models.ForeignKey(Quantities, models.DO_NOTHING, blank=True, null=True, db_column='quantity_id')
    sampleprop = models.ForeignKey(Sampleprops, models.DO_NOTHING, blank=True, null=True, db_column='sampleprop_id')
    component = models.ForeignKey(Components, models.DO_NOTHING, blank=True, null=True, db_column='component_id')
    phase = models.ForeignKey(Phases, models.DO_NOTHING, blank=True, null=True, db_column='phase_id')
    number = models.TextField(blank=True, null=True)
    significand = models.TextField(blank=True, null=True)
    exponent = models.TextField(blank=True, null=True)
    error = models.TextField(blank=True, null=True)
    error_type = models.CharField(max_length=8)
    unit = models.ForeignKey(Units, models.DO_NOTHING, blank=True, null=True, db_column='unit_id')
    accuracy = models.IntegerField(blank=True, null=True)
    exact = models.IntegerField()
    text = models.CharField(max_length=128, blank=True, null=True)
    issue = models.CharField(max_length=32, blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'data'
        app_label = 'data'


class Purificationsteps(models.Model):
    chemical = models.ForeignKey(Chemicals, models.DO_NOTHING, db_column='chemical_id')
    step = models.PositiveIntegerField()
    type = models.CharField(max_length=128, db_collation='utf8_bin', blank=True, null=True)
    purity = models.CharField(max_length=16, db_collation='utf8_bin', blank=True, null=True)
    puritysf = models.PositiveIntegerField(blank=True, null=True)
    purityunit = models.ForeignKey(Units, models.DO_NOTHING, blank=True, null=True, db_column='unit_id')
    analmeth = models.CharField(max_length=1024, db_collation='utf8_bin', blank=True, null=True)
    purimeth = models.CharField(max_length=1024, db_collation='utf8_bin', blank=True, null=True)
    updated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'purificationsteps'
        app_label = 'purificationsteps'
