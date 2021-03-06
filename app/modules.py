from app import db
from marshmallow import Schema, fields, validate, exceptions, validates_schema, validates
# import datetime


class Courier(db.Model):
    courier_id = db.Column(db.Integer, primary_key=True)
    courier_type = db.relationship('Type', backref=db.backref('courier', lazy=True))
    regions = db.relationship('Regions', backref=db.backref('courier', lazy=True))
    working_hours = db.relationship('WorkingHours', backref=db.backref('courier', lazy=True))
    earnings = db.Column(db.Integer, default=0)

    def __init__(self, courier_id):
        self.courier_id = courier_id


class CourierSchema(Schema):
    courier_id = fields.Int(strict=True, required=True, validate=validate.Range(1))
    courier_type = fields.Str(required=True, validate=validate.OneOf(['foot', 'bike', 'car']))
    regions = fields.List(cls_or_instance=fields.Int(strict=True, validate=validate.Range(1)), required=True)
    working_hours = fields.List(cls_or_instance=fields.Str(
        validate=validate.Regexp(r"^(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1][0-9])|(2[0-3])):[0-5][0-9]$")),
        required=True)

    @validates("regions")
    def is_regions_empty(self, lst):
        if not lst:
            raise exceptions.ValidationError("This field is empty.")

    @validates("working_hours")
    def is_wh_empty(self, lst):
        if not lst:
            raise exceptions.ValidationError("This field is empty.")

    @validates("working_hours")
    def is_interval_ok(self, intervals):
        for interval in intervals:
            if interval[:5] >= interval[6:]:
                raise exceptions.ValidationError("String does not match expected pattern.")


class CourierEditSchema(Schema):
    courier_id = fields.Int(strict=True)
    courier_type = fields.Str(validate=validate.OneOf(['foot', 'bike', 'car']))
    regions = fields.List(cls_or_instance=fields.Int(strict=True, validate=validate.Range(1)))
    working_hours = fields.List(
        cls_or_instance=fields.Str(
            validate=validate.Regexp(r"^(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1][0-9])|(2[0-3])):[0-5][0-9]$")))

    @validates("regions")
    def is_regions_empty(self, lst):
        if not lst:
            raise exceptions.ValidationError("This field is empty.")

    @validates("working_hours")
    def is_wh_empty(self, lst):
        if not lst:
            raise exceptions.ValidationError("This field is empty.")


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
    coef = db.Column(db.Integer)
    hours = db.relationship('PreferredTime', backref=db.backref('order', lazy=True))
    bunch_complete = db.Column(db.Integer)

    def __init__(self, order_id, weight, region):
        self.order_id = order_id
        self.weight = weight
        self.region = region


class OrderSchema(Schema):
    order_id = fields.Int(strict=True, required=True, validate=validate.Range(1))
    weight = fields.Float(required=True)
    region = fields.Int(strict=True, required=True, validate=validate.Range(1))
    delivery_hours = fields.List(
        cls_or_instance=fields.Str(validate=validate.Regexp(
            r"^(([0-1][0-9])|(2[0-3])):[0-5][0-9]-(([0-1][0-9])|(2[0-3])):[0-5][0-9]$"), required=True), required=True)

    @validates("delivery_hours")
    def is_wh_empty(self, lst):
        if not lst:
            raise exceptions.ValidationError("This field is empty.")

    @validates("weight")
    def is_valid_float(self, n):
        # print(type(n))
        # if type(n) == str:
        #     raise exceptions.ValidationError("Not a valid float.")
        if n < 0.01 or n > 50:
            raise exceptions.ValidationError("Value out of range.")
        if len(str(n)) > 5:
            raise exceptions.ValidationError("Allowed no more than two digits after decimal point.")

    @validates("delivery_hours")
    def is_interval_ok(self, intervals):
        for interval in intervals:
            if interval[:5] >= interval[6:]:
                raise exceptions.ValidationError("String does not match expected pattern.")


class AssignSchema(Schema):
    courier_id = fields.Int(strict=True, required=True)


class CompleteSchema(Schema):
    courier_id = fields.Int(strict=True, required=True)
    order_id = fields.Int(strict=True, required=True)
    complete_time = fields.DateTime(format='iso', required=True)


class PreferredTime(db.Model):
    dt_id = db.Column(db.Integer, primary_key=True)  # dt -- delivery time (aka preferred time)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    hours = db.Column(db.String(30))

    def __init__(self, order_id, hours):
        self.order_id = order_id
        self.hours = hours
