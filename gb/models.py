from gb import app, db, session
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class Wig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chrom = db.Column(db.String)

    def __repr__(self):
        return "Wig: {} - {}".format(self.id, self.chrom)

    def __init__(self,chrom):
        self.chrom = chrom

class WigValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    value = db.Column(db.Integer)
    wig_id = db.Column(db.Integer, db.ForeignKey('wig.id'))
    
    wig = db.relationship("Wig",backref=db.backref("values",order_by=position))

    def __init__(self, position, value, wig_id):
        self.position = position
        self.value = value
        self.wig_id = wig_id

    def __repr__(self):
        return "wig_id: {} - pos: {} - score: {}".format(self.wig_id, self.position, self.value)

class Gtf(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class GtfValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # actal atters
    seqname = db.Column(db.String)
    source = db.Column(db.String)
    feature = db.Column(db.String)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    score = db.Column(db.Float)
    strand = db.Column(db.Enum("+","-","."))
    frame = db.Column(db.Integer)
    attribute = db.Column(db.String)

    # relationship
    gtf_id = db.Column(db.Integer, db.ForeignKey("gtf.id"))
    gtf = db.relationship("Gtf",backref=db.backref("values",order_by=start))

    def __init__(self, seqname, source, feature, start, end, score, strand, frame, attribute, gtf_id):
        self.seqname = seqname
        self.source = source
        self.feature = feature
        self.start = start
        self.end = end
        self.score = score
        self.strand = strand
        self.frame = frame
        self.attribute = attribute
        self.gtf_id = gtf_id

    def to_json(self):
        return {
            'seqname' : self.seqname, 
            'source' : self.source, 
            'feature' : self.feature, 
            'start' : self.start, 
            'end' : self.end, 
            'score' : self.score, 
            'strand' : self.strand, 
            'frame' : self.frame, 
            'attribute' : self.attribute, 
        }


class Bed(db.Model):
    id = db.Column(db.Integer, primary_key=True)

class BedValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chrom = db.Column(db.String)
    start = db.Column(db.Integer)
    end = db.Column(db.Integer)
    name = db.Column(db.String)
    score = db.Column(db.Integer)
    strand = db.Column(db.Enum("+","-","."))
    thick_start = db.Column(db.Integer)
    thick_end = db.Column(db.Integer)
    item_rgb = db.Column(db.Integer)
    block_count = db.Column(db.Integer)

    # relationship
    bed_id = db.Column(db.Integer, db.ForeignKey("bed.id"))
    bed = db.relationship("Bed",backref=db.backref("values",order_by=start))

    def __init__(self, chrom, start, end, name, score, strand, thick_start, thick_end, item_rgb, block_count, bed_id):
        self.chrom = chrom
        self.start = start
        self.end = end
        self.name = name
        self.score = score
        self.strand = strand
        self.thick_start = thick_start
        self.thick_end = thick_end
        self.item_rgb = item_rgb
        self.block_count = block_count
        self.bed_id = bed_id

    def to_json(self):
        return {
            'chrom' : self.chrom, 
            'start' : self.start, 
            'end' : self.end, 
            'name' : self.name, 
            'score' : self.score, 
            'strand' : self.strand, 
            'thick_start' : self.thick_start, 
            'thick_end' : self.thick_end, 
            'item_rgb' : self.item_rgb,
            'block_count' : self.block_count,
            'block_sizes' : [size.value for size in self.block_sizes],
            'block_starts' : [start.value for start in self.block_starts] 
        }

class BedBlockSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    value = db.Column(db.Integer)
    bed_value_id = db.Column(db.Integer, db.ForeignKey("bed_value.id"))
    bed_value = db.relationship("BedValue",backref=db.backref("block_sizes",order_by=index))

    def __init__(self, index, value, bed_value_id):
        self.index = index
        self.value = value
        self.bed_value_id = bed_value_id

class BedBlockStart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer)
    value = db.Column(db.Integer)
    bed_value_id = db.Column(db.Integer, db.ForeignKey("bed_value.id"))
    bed_value = db.relationship("BedValue",backref=db.backref("block_starts",order_by=index))

    def __init__(self, index, value, bed_value_id):
        self.index = index
        self.value = value
        self.bed_value_id = bed_value_id

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

    def __init__(self, position, nucleotide,fasta_id):
        self.position = position
        self.nucleotide = nucleotide
        self.fasta_id = fasta_id

    def __repr__(self):
            return self.nucleotide       

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index = True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String)

    def __init__(self, username, password, email):
        self.username = username
        self.hash_password(password);
        self.email = email

    def __repr__(self):
        return self.username

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_token(token):
        s = Serializer(app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token

        user = User.query.get(data['id'])
        return user

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    data_id = db.Column(db.Integer)
    data_type = db.Column(db.Enum('wig','bed','gtf','fasta'))
    file_name = db.Column(db.String)

    def __init__(self,track_name,user_id,data_type,data_id, file_name):
        self.track_name = track_name
        self.user_id = user_id
        self.data_type = data_type
        self.data_id = data_id
        self.file_name = file_name

    def to_json(self):
        return {
            'track_id'   : self.id,
            'track_name' : self.track_name,
            'user_id'    : self.user_id,
            'data_type'  : self.data_type,
            'data_id'    : self.data_id,
            'file_name'  : self.file_name
        }

class View(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    view_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, view_name, user_id):
        self.view_name = view_name
        self.user_id = user_id

    def to_data(self):
        view_tracks = []
        for view_track in self.view_tracks:
            view_tracks.append(view_track.to_json())
        return {
            'view_name' : self.view_name,
            'view_tracks' : view_tracks,
            'user_id' : self.user_id,
            'view_id' : self.id
        }

    def to_json(self):
        track_ids = []
        for view_track in self.view_tracks:
            track_ids.append(view_track.track_id)
        return {
            'view_name' : self.view_name,
            'track_ids' : track_ids,
            'user_id' : self.user_id,
            'view_id' : self.id
        }

class ViewTrack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    view_id = db.Column(db.Integer, db.ForeignKey('view.id'))
    
    # display parameters
    sticky = db.Column(db.Boolean)
    hidden = db.Column(db.Boolean)
    y_max = db.Column(db.Integer)

    view = db.relationship('View', backref='view_tracks')
    track = db.relationship('Track', backref='view_tracks')
    
    def __init__(self, track_id, view_id):
        self.track_id = track_id
        self.view_id = view_id
        self.sticky = False
        self.hidden = False
        self.y_max = -1

    def to_json(self):
        track = session.query(Track).get(self.track_id)
        data = []
        if track.data_type == 'fasta':
            fasta = session.query(Fasta).get(track.data_id)
            data.append(fasta.header)
            data.append("".join(str(base) for base in fasta.base_pairs))

        elif track.data_type == 'wig':
            wig = session.query(Wig).get(track.data_id)
            for wig_val in wig.values:
                data.append([wig_val.position, wig_val.value])

        elif track.data_type == 'gtf':
            gtf = session.query(Gtf).get(track.data_id)
            for gtf_val in gtf.values:
                data.append(gtf_val.to_json())

        elif track.data_type == 'bed':
            bed = session.query(Bed).get(track.data_id)
            for bed_value in bed.values:
                data.append(bed_value.to_json())

        return {
            'track_name' : track.track_name,
            'track_id' : self.track_id,
            'data_type' : track.data_type,
            'data' : data
        }
