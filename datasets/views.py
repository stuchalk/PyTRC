""" datasets views file """
from django.shortcuts import render
from django.http import JsonResponse
from trcconfig.models import *
from datasets.functions import *
from scidatalib.scidata import SciData


def view(request, dsid=None):
    """ function to aggregate data about a dataset """
    # get the dataset
    dset = Datasets.objects.get(id=dsid)
    refid = dset.reference_id
    # get the reference data
    ref = References.objects.get(id=refid)
    # get the quantity(s) that was measured
    quants = qlist(dsid)
    # get the related datasets (from the same paper)
    rellst = Datasets.objects.filter(reference_id=refid).exclude(id=dset.id).values('id', 'setnum').order_by('setnum')
    rels = []
    for rel in rellst:
        rels.append({'id': rel['id'], 'title': 'Dataset ' + str(rel['setnum']) + ' in paper ' + ref.doi})
    # get methodology
    method = dset.sampleprops_set.all()[0].method_name
    # get phase(s)
    cphases = dset.conditions_set.values_list('phase__phasetype__name', flat=True).all().distinct()
    dphases = dset.data_set.values_list('phase__phasetype__name', flat=True).all().distinct()
    phases = []
    for ph in cphases:
        if ph not in phases:
            phases.append(ph)
    for ph in dphases:
        if ph not in phases:
            phases.append(ph)
    phases.sort()
    pstr = "' ".join(phases)
    # get substance(s)
    comps = dset.mixtures_set.all()[0].components_set.all().order_by('compnum')
    subs = []
    for comp in comps:
        chem = comp.chemical
        sub = {}
        sub.update({'id': chem.substance.id})
        sub.update({'name': chem.substance.name})
        sub.update({'formula': chem.substance.formula})
        sub.update({'ikey': chem.substance.inchikey})
        sub.update({'source': chem.sourcetype})
        subs.append(sub)
    # get datasets
    sets = getdset(dsid)

    return render(request, '../templates/datasets/view.html', {'ref': ref, 'quants': quants, 'rels': rels, 'sets': sets,
                                                               'method': method, 'phases': pstr, 'subs': subs})


def scidata(request, dsid=None):
    """ create scidata JSON-LD"""
    # get the data
    dset = Datasets.objects.get(id=dsid)
    refid = dset.reference_id
    # get the reference data
    ref = References.objects.get(id=refid)
    # generate the JSON-LD
    dparts = ref.doi.split("/")
    jcode = ref.journal.set
    uid = 'trc_' + jcode + '_' + dparts[1] + '_' + str(dset.setnum)
    # create SciData object
    jld = SciData(uid)
    base = 'https://scidata.unf.edu/tranche/trc/' + jcode + '/' + uid
    jld.base(base)
    jld.context(['https://stuchalk.github.io/scidata/contexts/crg_mixture.jsonld',
                 'https://stuchalk.github.io/scidata/contexts/crg_chemical.jsonld',
                 'https://stuchalk.github.io/scidata/contexts/crg_substance.jsonld'])
    # set graph id
    jld.docid(base)
    # add namespaces

    # jld.namespaces()
    jld.title('SciData JSON-LD file of data from the NIST TRC dataset')
    jld.description('SciData JSON-LD generate using the SciDataLib Python package')
    au1 = {'name': 'Montana Sloan', 'orcid': '0000-0003-2127-9752', 'role': 'developer'}
    au2 = {'name': 'Stuart J. Chalk', 'orcid': '0000-0002-0703-7776', 'organization': 'University of North Florida',
           'role': 'developer', 'email': 'schalk@unf.edu'}
    jld.author([au1, au2])
    jld.version('1')
    # add substances
    # add sources
    citestr = ref.title + " " + ref.aulist + "; " + ref.journal.name + " " + str(ref.year) + ", " + \
              ref.volume + ", " + ref.startpage
    if ref.endpage:
        citestr += "-" + ref.endpage
    src1 = {'citation': citestr, 'url': 'https://doi.org/' + ref.doi, 'type': 'paper'}

    jld.sources([src1])
    # add rights
    jld.rights('NIST Thermodynamics Research Center (Boulder, CO)', 'https://www.nist.gov/open/license')
    output = jld.output
    return JsonResponse(output, status=200)
