""" datasets views file """
from django.shortcuts import render
from django.http import JsonResponse
from trcconfig.models import *
from crosswalks.models import *
from datasets.functions import *
from scidatalib.scidata import SciData
from sigfig import round


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
    sys = dset.system
    return render(request, '../templates/datasets/view.html', {'ref': ref, 'quants': quants, 'rels': rels,
                                                               'sets': sets, 'method': method, 'phases': pstr,
                                                               'subs': subs, 'sys': sys})


def scidata(request, dsid=None):
    """ create scidata JSON-LD"""

    # get the dataset
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
    base = 'https://scidata.unf.edu/tranche/trc/' + jcode + '/' + uid + '/'
    jld.base(base)
    jld.context(['https://stuchalk.github.io/scidata/contexts/crg_mixture.jsonld',
                 'https://stuchalk.github.io/scidata/contexts/crg_chemical.jsonld',
                 'https://stuchalk.github.io/scidata/contexts/crg_substance.jsonld'])

    # set graph id
    jld.docid(base)

    # add namespaces
    otids = Crosswalks.objects.values_list('ontterm_id', flat=True).all().distinct()
    nsids = Ontterms.objects.filter(id__in=otids).values_list('nspace', flat=True).all().distinct()
    nspaces = Nspaces.objects.filter(id__in=nsids).values('ns', 'path')
    nss = {}
    for nspace in nspaces:
        nss.update({nspace['ns']: nspace['path']})
    jld.namespaces(nss)
    jld.title('SciData JSON-LD file of data from the NIST TRC dataset')
    jld.description('SciData JSON-LD generated using the SciDataLib (v 0.3.0) Python package')
    au1 = {'name': 'Montana Sloan', 'orcid': '0000-0003-2127-9752', 'role': 'developer'}
    au2 = {'name': 'Stuart J. Chalk', 'orcid': '0000-0002-0703-7776', 'organization': 'University of North Florida',
           'role': 'developer', 'email': 'schalk@unf.edu'}
    jld.author([au1, au2])
    jld.version('1')

    # add discipline and subdiscipline
    jld.discipline('w3i:Chemistry')
    jld.subdiscipline('w3i:PhysicalChemistry')

    # ADD METHODOLOGY DATA
    jld.evaluation('experimental')
    jld.evaluation('obo:NCIT_C28041')
    sprops = Sampleprops.objects.filter(dataset_id=dsid).values_list('method_name', flat=True)
    spropstr = ', '.join(sprops)
    jld.aspects([{'@id': 'method', 'method': spropstr}])

    # ADD SYSTEM DATA

    # add substances
    subids = SubstancesSystems.objects.filter(system_id=dset.system_id).values_list('substance_id', flat=True)
    sublist = Substances.objects.filter(id__in=subids)
    subs, chms = [], []
    for sidx, sub in enumerate(sublist):
        # substances
        s = {}
        s.update({'@id': 'substance'})
        s.update({'name': sub.name})
        s.update({'formula': sub.formula})
        s.update({'molweight': sub.mw})
        s.update({'inchikey': sub.inchikey})
        idents = sub.identifiers_set.filter(type__in=['casrn', 'inchi', 'iupacname'])
        for ident in idents:
            s.update({ident.type: ident.value})
        subs.append(s)

        # chemicals
        chm = sub.chemicals_set.all()[0]
        c = {}
        c.update({'@id': 'chemical'})
        c.update({'substance#': 'substance/' + str(sidx + 1) + '/'})
        c.update({'formula': sub.name})
        c.update({'sourcetype': chm.sourcetype})
        chms.append(c)

    jld.facets(subs)
    jld.facets(chms)

    # add conditions
    scondlist = dset.conditions_set.all().filter(datapoint_id__isnull=True).values_list('quantity_id', flat=True)
    condlist = dset.conditions_set.all().filter(datapoint_id__isnull=False).values_list('quantity_id', flat=True)
    sqids = list(set(scondlist))
    qids = list(set(condlist))
    quants, cons, qidxs = [], [], []
    # index for datapoints and their conditions (dictionary of lists - key is dpid and list are conditions)
    dpidx, scondnum, condnum, sconds = {}, 0, 0, []
    # series conditions
    if sqids:
        # quantities first then the conditions referencing back to the quantity
        for sqid in sqids:
            # get data
            quant = Quantities.objects.get(id=sqid)
            cond = dset.conditions_set.filter(quantity_id=sqid)[0]
            # capture the unique quantities (quantity, phase, component)
            qstr = quant.quantitykind.name
            if cond.phase:
                qstr += ':' + cond.phase.phasetype.name.lower()
            if cond.component:
                qstr += ':' + str(cond.component.compnum)
            if qstr not in qidxs:
                qidxs.append(qstr)
            qidx = str(qidxs.index(qstr) + 1)
            # quantity (metadata only no values)
            quantity = {'@id': 'quantity'}
            quantity.update({'quantitykind': quant.quantitykind.name})
            cw = Crosswalks.objects.get(table='conditions', field=quant.name)
            if cw:
                quantity.update({'quantitykind#': cw.ontterm.nspace.ns + ':' + cw.ontterm.code})
            quantity.update({'quantity': quant.name})
            if cond.component:
                quantity['quantity'] += ' of Constituent ' + str(cond.component.compnum)
                quantity.update({'constituent': 'constituent/' + str(cond.component.compnum) + '/'})
            if cond.phase:
                quantity['quantity'] += ' (' + cond.phase.phasetype.name.lower() + ')'
                quantity.update({'phase': cond.phase.phasetype.name.lower()})
            if cond.unit:
                quantity.update({'unit': cond.unit.name})
                if cond.unit.qudt:
                    qns = Nspaces.objects.get(ns='qudt')
                    jld.namespaces({'qudt': qns.path})
                    quantity.update({'unit#': 'qudt:' + cond.unit.qudt})
            quantity.update({'temp': qstr})
            quants.append(quantity)
            # condition (only one condition value expected for series conditions)
            scondnum += 1
            condnum += 1  # needed to offset the regular condnums by the # of sconds
            sconds.append('condition/' + str(scondnum) + '/')
            if cond.datapoint_id not in dpidx.keys():
                dpidx.update({cond.datapoint_id: []})
            dpidx[cond.datapoint_id].append('condition/' + str(condnum) + '/')
            con = {'@id': 'condition'}
            con.update({'quantity#': 'quantity/' + qidx + '/'})
            number = float(cond.number)
            if isinstance(number, int):
                con.update({'datatype': 'xsd:integer'})
            else:
                con.update({'datatype': 'xsd:float'})
            con.update({'number': round(number, sigfigs=cond.accuracy)})
            if not cond.exact:
                con.update({'sigfigs': cond.accuracy})
                con.update({'error': pow(10, int(cond.exponent) - cond.accuracy + 1)})
                con.update({'errortype': 'absolute'})
                con.update({'errornote': 'estimated from data'})
            cons.append(con)

    # regular (individual datapoint) conditions
    if qids:
        for qid in qids:
            # get data
            quant = Quantities.objects.get(id=qid)
            conds = dset.conditions_set.filter(quantity_id=qid).order_by('datapoint__row_index')
            # conditions (one to many)
            for cond in conds:
                # capture the unique quantities (quantity, phase, component)
                qstr = quant.quantitykind.name
                if cond.phase:
                    qstr += ':' + cond.phase.phasetype.name.lower()
                if cond.component:
                    qstr += ':' + str(cond.component.compnum)
                if qstr not in qidxs:
                    qidxs.append(qstr)
                    # go ahead a process and add quantity to file
                    quant = Quantities.objects.get(id=qid)
                    quantity = {'@id': 'quantity'}
                    quantity.update({'quantitykind': quant.quantitykind.name})
                    cw = Crosswalks.objects.get(table='conditions', field=quant.name)
                    quantity.update({'quantitykind#': cw.ontterm.nspace.ns + ':' + cw.ontterm.code})
                    quantity.update({'quantity': quant.name})
                    if cond.component:
                        quantity['quantity'] += ' of Constituent ' + str(cond.component.compnum)
                        quantity.update({'constituent': 'constituent/' + str(cond.component.compnum) + '/'})
                    if cond.phase:
                        quantity['quantity'] += ' (' + cond.phase.phasetype.name.lower() + ')'
                        quantity.update({'phase': cond.phase.phasetype.name.lower()})
                    if cond.unit:
                        quantity.update({'unit': cond.unit.name})
                        if cond.unit.qudt:
                            qns = Nspaces.objects.get(ns='qudt')
                            jld.namespaces({'qudt': qns.path})
                            quantity.update({'unit#': 'qudt:' + cond.unit.qudt})
                    quants.append(quantity)
                else:
                    # quantity already added - just process condition
                    pass

                # get quantity index #
                qidx = str(qidxs.index(qstr) + 1)
                # update datpoint idx
                condnum += 1
                if cond.datapoint_id not in dpidx.keys():
                    dpidx.update({cond.datapoint_id: []})
                dpidx[cond.datapoint_id].append('condition/' + str(condnum) + '/')
                # create condition
                con = {'@id': 'condition'}
                con.update({'quantity#': 'quantity/' + qidx + '/'})
                number = float(cond.number)
                if isinstance(number, int):
                    con.update({'datatype': 'xsd:integer'})
                else:
                    con.update({'datatype': 'xsd:float'})
                con.update({'number': round(number, sigfigs=cond.accuracy)})
                if not cond.exact:
                    con.update({'sigfigs': cond.accuracy})
                    con.update({'error': pow(10, int(cond.exponent) - cond.accuracy + 1)})
                    con.update({'errortype': 'absolute'})
                    con.update({'errornote': 'estimated from data'})
                cons.append(con)

    jld.facets(quants)
    jld.facets(cons)

    # create rels variable to lookup conditions that are for a specfic datapoint
    rels = {}
    pnts = dset.conditions_set.filter(datapoint__isnull=False).order_by('datapoint__row_index')
    for pnt in pnts:
        if str(pnt.datapoint_id) not in rels:
            rels.update({str(pnt.datapoint_id): []})

    rels.update()

    # add sources
    citestr = ref.title + " " + ref.aulist + "; " + ref.journal.name + \
        " " + str(ref.year) + ", " + ref.volume + ", " + ref.startpage
    if ref.endpage:
        citestr += "-" + ref.endpage
    src1 = {'citation': citestr, 'url': 'https://doi.org/' + ref.doi, 'type': 'paper'}
    jld.sources([src1])

    # add rights
    jld.rights(
        [
            {'holder': 'NIST Thermodynamics Research Center (Boulder, CO)',
             'license': 'https://www.nist.gov/open/license'}
        ])

    # output the JSON
    output = jld.output
    return JsonResponse(output, status=200)
