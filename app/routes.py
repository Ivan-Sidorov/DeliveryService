# -*- coding: utf-8 -*-
from app import app, db
from flask import request, make_response, jsonify, abort
from app.modules import *
import arrow
import datetime


@app.route('/couriers', methods=['POST'])
def post_couriers():
    # не допускать пустой список
    data = request.json['data']
    ids_error = []
    ids_success = []
    schema = CourierSchema()
    for courier in data:
        courier_id = courier['courier_id']
        if courier_id in list(map(lambda x: x.courier_id, Courier.query.all())):
            ids_error.append(courier_id)
            print("ok1")
        try:
            result = schema.load(courier)
        except exceptions.MarshmallowError as e:
            print("ok2")
            print(e)
            if courier['courier_id'] not in ids_error:
                ids_error.append(courier['courier_id'])
    for courier in data:
        courier_id = courier['courier_id']
        if not ids_error:
            courier_type = courier['courier_type']
            db.session.add(Courier(courier_id))
            db.session.add(Type(courier_type, courier_id))
            for reg in courier['regions']:
                db.session.add(Regions(reg, courier_id))
            for t in courier['working_hours']:
                db.session.add(WorkingHours(t, courier_id))
            db.session.commit()
            ids_success.append(courier_id)
    if ids_error:
        return make_response(jsonify({"validation_error": {"couriers": [{"id": c_id} for c_id in ids_error]}}), 400)
    return make_response(jsonify({"couriers": [{"id": c_id} for c_id in ids_success]}), 201)


@app.route('/couriers/<int:courier_id>', methods=['PATCH'])
def edit_courier(courier_id):
    schema = CourierEditSchema()
    try:
        result = schema.load(request.json)
        print(result)
    except exceptions.MarshmallowError as err:
        return make_response(jsonify(err.messages), 400)
    courier = Courier.query.get(courier_id)
    keys = list(result.keys())
    if "courier_type" in keys:
        courier_type = result['courier_type']
        courier.courier_type = courier_type
        type_info = Type.query.filter(Type.courier_id == courier_id).first()
        type_info.type = courier_type
        type_info.calc_vol_coef()
        orders = Orders.query.filter(
            Orders.courier_id == courier_id, Orders.complete == None, Orders.weight > type_info.vol).all()
        for order in orders:
            order.courier_id = None
            order.assign = None
        db.session.commit()
    if "regions" in keys:
        regions = result['regions']
        if not regions:
            return make_response(jsonify({"message": "The 'regions' field is not described"}), 400)
        regions_old = Regions.query.filter(Regions.courier_id == courier_id).all()
        for region in regions_old:
            db.session.delete(region)
        for region in regions:
            db.session.add(Regions(region, courier_id))
        orders = Orders.query.filter(
            Orders.courier_id == courier_id, Orders.complete == None, Orders.region not in regions).all()
        for order in orders:
            order.courier_id = None
            order.assign = None
        db.session.commit()
    if "working_hours" in keys:
        working_hours = result['working_hours']
        if not working_hours:
            return make_response(jsonify({"message": "The 'working_hours' field is not described"}), 400)
        orders = Orders.query.filter(Orders.courier_id == courier_id).all()
        wh_old = WorkingHours.query.filter(WorkingHours.courier_id == courier_id).all()
        for wh in wh_old:
            db.session.delete(wh)
        for wh in working_hours:
            db.session.add(WorkingHours(wh, courier_id))
        working_hours = WorkingHours.query.filter(WorkingHours.courier_id == courier_id)
        for work_hours in working_hours:
            start_cour, end_cour = to_time(work_hours.hours)
            for order in orders:
                flag = False
                for hours in order.hours:
                    start_ord, end_ord = to_time(hours.hours)
                    if (start_ord <= start_cour <= end_ord) or (start_cour <= start_ord <= end_cour):
                        flag = True
                if not flag:
                    order.courier_id = None
                    order.assign = None
        db.session.commit()
    courier = Courier.query.get(courier_id)
    courier_data = {
        "courier_id": courier.courier_id,
        "courier_type": courier.courier_type[0].__repr__(),
        "regions": [int(i.__repr__()) for i in courier.regions],
        "working_hours": [i.__repr__() for i in courier.working_hours]
    }
    return make_response(jsonify(courier_data), 200)


@app.route('/couriers/<int:courier_id>', methods=['GET'])
def get_courier(courier_id):
    if courier_id not in list(map(lambda x: x.courier_id, Courier.query.all())):
        return make_response(jsonify({"message": f"Courier with id={courier_id} does not exist"}), 404)
    courier = Courier.query.get(courier_id)
    courier_data = {
        "courier_id": courier.courier_id,
        "courier_type": courier.courier_type[0].__repr__(),
        "regions": [int(i.__repr__()) for i in courier.regions],
        "working_hours": [i.__repr__() for i in courier.working_hours]
    }
    orders_complete = Orders.query.filter(Orders.courier_id == courier_id, Orders.complete != None).all()
    courier_data["earnings"] = sum([500 * order.coef for order in orders_complete])
    rating = 0
    cour_regions = [int(i.__repr__()) for i in courier.regions]
    districts = []
    for i in range(len(cour_regions)):
        print(cour_regions[i], type(cour_regions[i]))
        print(courier_id, type(courier_id))
        districts.append(Orders.query.order_by(Orders.complete).filter(
            Orders.courier_id == courier_id, Orders.region == cour_regions[i]).all())
    durations = []
    for i in range(len(districts)):
        last = districts[i][-1]
        for j in range(len(districts[i])-1):
            start = arrow.get(districts[i][j].complete)
            end = arrow.get(districts[i][j+1].complete)
            durations.append((end - start).total_seconds())
        start = arrow.get(last.assign)
        end = arrow.get(last.complete)
        durations.append((end - start).total_seconds())
    courier_data["rating"] = (60 * 60 - min(min(durations), 60 * 60)) / (60 * 60) * 5
    return make_response(jsonify(courier_data), 201)






@app.route('/orders', methods=['POST'])
def post_orders():
    # разобраться с весами посылок (2 знака после запятой)
    # а что если нет поля data
    data = request.json['data']
    ids_error = []
    ids_success = []
    schema = OrderSchema()
    # а что если неверно названы поля или есть лишние
    for order in data:
        order_id = order['order_id']
        if order_id in list(map(lambda x: x.order_id, Orders.query.all())):
            ids_error.append(order_id)
        try:
            result = schema.load(order)
        except exceptions.MarshmallowError:
            if order['order_id'] not in ids_error:
                ids_error.append(order['order_id'])
    for order in data:
        order_id = order['order_id']
        if not ids_error:
            weight = order['weight']
            region = order['region']
            db.session.add(Orders(order_id, weight, region))
            for hours in order['delivery_hours']:
                db.session.add(PreferredTime(order_id, hours))
            db.session.commit()
            ids_success.append(order_id)
    if ids_error:
        return make_response(jsonify({"validation_error": {"orders": [{"id": o_id} for o_id in ids_error]}}), 400)
    return make_response(jsonify({"orders": [{"id": o_id} for o_id in ids_success]}), 201)


def to_time(interval):
    start = list(map(int, (interval.split('-')[0]).split(':')))
    end = list(map(int, (interval.split('-')[1]).split(':')))
    start = datetime.time(hour=start[0], minute=start[1])
    end = datetime.time(hour=end[0], minute=end[1])
    return start, end


@app.route('/orders/assign', methods=['POST'])
def assign_orders():
    courier_id = request.json['courier_id']
    if courier_id not in list(map(lambda x: x.courier_id, Courier.query.all())):
        return abort(404)
    courier_vol = (Type.query.filter(Type.courier_id == courier_id).first()).vol
    courier = Courier.query.get(courier_id)
    cour_coef = Type.query.filter(Type.courier_id == courier_id).first().coef
    courier_regions = [int(i.__repr__()) for i in courier.regions]
    orders = Orders.query.filter(Orders.weight <= courier_vol, Orders.region.in_(courier_regions),
                                 Orders.courier_id == None).all()
    courier_hours = courier.working_hours
    ids = []
    assign_time = arrow.utcnow().isoformat()[:-10] + 'Z'
    for work_hours in courier_hours:
        start_cour, end_cour = to_time(work_hours.hours)
        for order in orders:
            flag = False
            for hours in order.hours:
                start_ord, end_ord = to_time(hours.hours)
                if (start_ord <= start_cour <= end_ord) or (start_cour <= start_ord <= end_cour):
                    flag = True
            if flag and order.order_id not in ids:
                ids.append(order.order_id)
                res_ord = Orders.query.get(order.order_id)
                res_ord.courier_id = courier_id
                res_ord.assign = assign_time
                res_ord.coef = cour_coef
                db.session.commit()
    total_orders = Orders.query.filter(Orders.courier_id == courier_id,
                                       Orders.assign != None).with_entities(Orders.order_id).all()
    total_orders = [x[0] for x in total_orders]
    if not total_orders:
        return make_response(jsonify({"orders": []}), 201)
    times = Orders.query.filter(Orders.assign != None).order_by(Orders.complete).with_entities(Orders.assign).all()
    assign_time = times[-1][0]
    return make_response(jsonify({"orders": [{"id": ord_id} for ord_id in total_orders], "assign_time": assign_time}), 200)


@app.route('/orders/complete', methods=['POST'])
def orders_complete():
    # разобраться с датами
    # порядок вывода наоборот
    schema = CompleteSchema()
    try:
        result = schema.load(request.json)
    except exceptions.MarshmallowError:
        return make_response(jsonify({"message": "incorrect data type"}), 400)
    courier_id = result['courier_id']
    order_id = result['order_id']
    cour_exists = Courier.query.get(courier_id)
    order_exists = Orders.query.get(order_id)
    if cour_exists is None or order_exists is None:
        return make_response(jsonify({"message": "non-existent data"}), 400)
    cour_order = Orders.query.filter(Orders.courier_id == courier_id, Orders.order_id == order_id).first()
    if not cour_order:
        return make_response(jsonify({"message": "this order is not assigned to this courier"}), 400)
    if order_exists.complete:
        return make_response(jsonify({"order_id": order_exists.order_id}), 200)
    order_exists.complete = request.json['complete_time']
    db.session.commit()
    return make_response(jsonify({"order_id": order_exists.order_id}), 200)
