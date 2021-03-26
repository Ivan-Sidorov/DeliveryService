from app import db
from marshmallow import Schema, fields, validate, exceptions


class Courier(db.Model):
    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.relationship('Type', backref=db.backref('courier', lazy=True))
    regions = db.relationship('Regions', backref=db.backref('courier', lazy=True))
    working_hours = db.relationship('WorkingHours', backref=db.backref('courier', lazy=True))

    def __init__(self, courier_id):
        self.courier_id = courier_id


class CourierSchema(Schema):
    courier_id = fields.Int(required=True)
    courier_type = fields.Str(required=True, validate=validate.OneOf(['foot', 'bike', 'car']))
    regions = fields.List(cls_or_instance=fields.Int(), required=True)
    working_hours = fields.List(cls_or_instance=fields.Str(
        validate=validate.Regexp(r"^(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1][0-9])|(2[0-3])):[0-5][0-9]$")),
        required=True)


class CourierEditSchema(Schema):
    courier_id = fields.Int()
    courier_type = fields.Str(validate=validate.OneOf(['foot', 'bike', 'car']))
    regions = fields.List(cls_or_instance=fields.Int(required=True))
    working_hours = fields.List(
        cls_or_instance=fields.Str(
            validate=validate.Regexp(r"^(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1][0-9])|(2[0-3])):[0-5][0-9]$")))


class WorkingHours(db.Model):
    wh_id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.String(15))
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    def __init__(self, hours, courier_id):
        self.hours = hours
        self.courier_id = courier_id

    def __repr__(self):
        return str(self.hours)


class Type(db.Model):
    type_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))
    vol = db.Column(db.Integer)
    coef = db.Column(db.Integer)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    def __init__(self, courier_type, courier_id):
        self.type = courier_type
        self.vol, self.coef = self.calc_vol_coef()
        self.courier_id = courier_id

    def __repr__(self):
        return str(self.type)

    def calc_vol_coef(self):
        vol = (self.type == "foot") * 10 + (self.type == "bike") * 15 + (self.type == "car") * 50
        coef = (self.type == "foot") * 2 + (self.type == "bike") * 5 + (self.type == "car") * 9
        return vol, coef


class Regions(db.Model):
    region_id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.Integer)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))

    def __init__(self, region, courier_id):
        self.region = region
        self.courier_id = courier_id

    def __repr__(self):
        return str(self.region)


class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float)
    region = db.Column(db.Integer)
    assign = db.Column(db.String(30))
    complete = db.Column(db.String(30))
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.courier_id'))
    hours = db.relationship('PreferredTime', backref=db.backref('order', lazy=True))

    def __init__(self, order_id, weight, region):
        self.order_id = order_id
        self.weight = weight
        self.region = region


class OrderSchema(Schema):
    order_id = fields.Int(required=True)
    weight = fields.Float(required=True)
    region = fields.Int(required=True)
    delivery_hours = fields.List(
        cls_or_instance=fields.Str(validate=validate.Regexp(
            r"^(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1][0-9])|(2[0-3])):[0-5][0-9]$"), required=True), required=True)


class AssignSchema(Schema):
    courier_id = fields.Int(required=True)


class CompleteSchema(Schema):
    courier_id = fields.Int(required=True)
    order_id = fields.Int(required=True)
    complete_time = fields.DateTime(format='iso', required=True)


class PreferredTime(db.Model):
    dt_id = db.Column(db.Integer, primary_key=True)  # dt -- delivery time (aka preferred time)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    hours = db.Column(db.String(30))

    def __init__(self, order_id, hours):
        self.order_id = order_id
        self.hours = hours
