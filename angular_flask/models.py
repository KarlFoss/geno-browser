from datetime import datetime

from angular_flask.core import db
from angular_flask import app


class Wig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    span = db.Column(db.String)

    def __repr__(self):
        return "Wig: {}".format(self.id)

class WigValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    value = db.Column(db.Integer)
    id_wig = db.Column(db.Integer, db.ForeignKey('wig.id'))
    
    wig = db.relationship("Wig",backref=db.backref("values",order_by=position))

    def __init__(self, position, value):
        self.position = position
        self.value = value

    def __repr__(self):
            return "{}".format(self.value)


class Bed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chrom = db.Column(db.String)
    chromStart = db.Column(db.Integer)
    chromEnd = db.Column(db.Integer)
    name = db.Column(db.String)
    score = db.Column(db.Integer)
    strand = db.Column(db.Boolean)
    thick_start = db.Column(db.Integer)
    thick_end = db.Column(db.Integer)
    item_RGB = db.Column(db.Integer)
    item_RGB = db.Column(db.Integer)
    blockCount = db.Column(db.Integer)
    blockSizes = db.Column(db.Integer)
    blockStarts = db.Column(db.Integer)

    def __repr__(self):
            return "{}".format(self.name)

class Annotation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seqname = db.Column(db.String)
    source = db.Column(db.String)
    feature = db.Column(db.String)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    score = db.Column(db.Integer)
    strand = db.Column(db.Boolean)
    frame = db.Column(db.Integer)
    attribute = db.Column(db.String)

    def __repr__(self):
            return "{}".format(self.seqname)

class Fasta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    header = db.Column(db.String)

    def __init__(self, header):
        self.header = header

    def __repr__(self):
            return "{}".format(self.header)

class BasePair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nucleotide = db.Column(db.String(1))
    position = db.Column(db.Integer)
    fasta_id = db.Column(db.Integer, db.ForeignKey('fasta.id'))

    fasta = db.relationship("Fasta",backref=db.backref("base_pairs",order_by=position))

    def __init__(self, position, nucleotide):
        self.position = position
        self.nucleotide = nucleotide

    def __repr__(self):
            return self.nucleotide

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    email = db.Column(db.String)

    def __init__(self,user_name,email):
        self.user_name = user_name
        self.email = email

    def __repr__(self):
        return self.user_name

# models for which we want to create API endpoints
app.config['API_MODELS'] = {}#{ 'post': BasePair }

# models for which we want to create CRUD-style URL endpoints,
# and pass the routing onto our AngularJS application
app.config['CRUD_URL_MODELS'] = {}#{ 'post': Post }
