import pandas as pd
import doctest
import os

import logging
logging.basicConfig()
LOG = logging.getLogger(__name__)

def parse_file(filepath_or_buffer):
     
    if hasattr(filepath_or_buffer,'filename'):
        filename = filepath_or_buffer.filename
    else:
        filename = filepath_or_buffer

    base,ext = os.path.splitext(filename)

    if ext == '.gtf':
        return read_gtf(filename)
    elif ext == '.wig':
        return read_wig(filename)


def read_gtf(filepath_or_buffer):
    """
    Read a GTF (annotation) file and return a pandas DataFrame

    >>> gtf = read_gtf('sampleData/EBOLA.gtf')
    >>> gtf.columns
    Index([u'seqname', u'source', u'feature', u'start', u'end', u'score', u'strand', u'frame', u'gene_id', u'transcript_id'], dtype='object')
    """
    gtf = pd.read_table('sampleData/EBOLA.gtf',
                '\s+',
                names=['seqname','source','feature','start','end','score','strand','frame','gene_id','transcript_id'],
                header=None,
                index_col=False,
                usecols=[0,1,2,3,4,5,6,7,9,11],
                na_values=['.'],
                true_values=['+'])
    return gtf

def read_wig(filepath_or_buffer):
    """
    Read a WIG file and return a pandas DataFrame

    >>> wig = read_wig('sampleData/EBOLA.wig')
    >>> wig.columns 
    Index([u'wig'], dtype='object')
    >>> wig.shape
    (171323, 1)
    >>> wig.ix[wig.wig == 0,'wig'].index.values.mean()
    65220.647293912356
    """
    wig = pd.read_csv('sampleData/EBOLA.wig',header=None,skiprows=[0,1],names=['wig'])
    return wig
