""" helper functions for datasets table data """
from trcconfig.models import Datasets
from sigfig import round


def qlist(dsid=None):
    """ get the quantities that have been determined in a specific dataset """
    dset = Datasets.objects.get(id=dsid)
    samps = dset.sampleprops_set.all()
    qts = []
    for samp in samps:
        if samp.quantity.name not in qts:
            qts.append(samp.quantity.name)
    qstr = ", ".join(qts)
    return qstr


# noinspection DuplicatedCode
def getdset(dsid):
    """ function to aggregate data about a dataset """
    # get the dataset
    dset = Datasets.objects.get(id=dsid)
    # get conditions and data
    sers = dset.dataseries_set.all().order_by('idx')
    data = []
    for ser in sers:
        series = {'idx': ser.idx, 'hdrs': {}, 'cols': {}, 'colidx': [], 'rowidx': [], 'sconds': ""}
        rows = ser.datapoints_set.all().order_by('row_index')
        sconds = ser.conditions_set.all()  # series conditions
        # add series conditions
        for scidx, sc in enumerate(sconds):
            if scidx > 0:
                series['sconds'] += ", "
            val = round(sc.number, sigfigs=sc.accuracy, warn=False)
            series['sconds'] += sc.quantity.symbol + " = " + str(val) + " " + sc.unit.symbol
        for ridx, row in enumerate(rows):
            conds = row.conditions_set.all()
            datums = row.data_set.all()
            series['rowidx'].append(ridx)
            # get headers
            cidx = 1
            for cond in conds:
                # condition data
                col = 'col' + str(cidx)
                if ridx == 0:
                    cname, csym, cunit = cond.quantity.name, cond.quantity.symbol, cond.unit.symbol
                    hdr = '<span title="' + cname + '">' + csym + " (" + cunit + ")</span>"
                    series['hdrs'].update({col: hdr})
                    series['cols'].update({col: []})
                    series['colidx'].append(col)
                series['cols'][col].append(round(cond.number, sigfigs=cond.accuracy, warn=False))
                cidx += 1
            for didx, datum in enumerate(datums):
                # exptl data
                col = 'col' + str(cidx)
                if ridx == 0:
                    dname, dsym, dunit = datum.quantity.name, datum.quantity.symbol, datum.unit.symbol
                    hdr = '<span title="' + dname + '">' + dsym + " (" + dunit + ")</span>"
                    series['hdrs'].update({col: hdr})
                    series['cols'].update({col: []})
                    series['colidx'].append(col)
                # series['cols'][col].append(round(datum.number, sigfigs=datum.accuracy, warn=False))
                series['cols'][col].append(float(datum.number))

                cidx += 1
        data.append(series)
    return data
