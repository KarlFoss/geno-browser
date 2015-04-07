import unittest
from gb import db,app
from gb.models import (Wig,
    WigValue,
    BasePair,
    Bed,
    Annotation,
    Fasta,
    User,
    Track,
    View,
    ViewTrack)

import logging
logging.basicConfig()

LOG = logging.getLogger(__name__)


class TestSetUp(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_set_up(self):
        self.assertFalse(db.session.query(User).all())


class TestWig(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_empty_variable_wig(self):
        wig = Wig(chrom='EBV')
        db.session.add(wig)
        db.session.commit()
        self.assertEqual(wig.id == 1)

    def test_create_empty_fixed_wig(self):
        wig = Wig(chrom='EBV')
        db.session.add(wig)
        db.session.commit()
        self.assertEqual(wig.id == 1)

    def test_create_wig_with_values(self):
        wig = Wig(chrom='EBV')
        wig.values = [WigValue(i,x,None) for i,x in enumerate(range(0,1000,10))]
        db.session.add(wig)
        db.session.commit()
        self.assertEqual(len(range(0,1000,10)),len(db.session.query(Wig).first().values))
