""" helper functions for datasets table data """
from trcconfig.models import Datasets


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
