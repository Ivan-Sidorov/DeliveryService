from app import app, db
from flask import json
from Tests.test_data import *


class TestViews(object):

    def setup(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/TestViews'
        # app.testing = True
        self.app = app.test_client()
        db.create_all()
        create_cour = self.app.post('/couriers', data=json.dumps(initial_couriers), content_type='application/json')
        create_ord = self.app.post('/orders', data=json.dumps(initial_orders), content_type='application/json')

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_couriers_400(self):
        resp = self.app.post('/couriers', data=json.dumps(couriers_400), content_type='application/json')
        assert resp.status_code == 400
        assert resp.json == couriers_400_resp

    def test_orders_400(self):
        resp = self.app.post('/orders', data=json.dumps(orders_400), content_type='application/json')
        assert resp.status_code == 400
        assert resp.json == orders_400_resp

    def test_couriers_400_data(self):
        resp = self.app.post('/couriers', data=json.dumps(couriers_no_data_400), content_type='application/json')
        assert resp.status_code == 400
        assert resp.json == couriers_no_data_400_resp

    def test_couriers_200(self):
        resp = self.app.post('/couriers', data=json.dumps(couriers_201), content_type='application/json')
        assert resp.status_code == 201
        assert resp.json == couriers_201_resp

    def test_assign_orders_400_val(self):
        resp = self.app.post('/orders/assign', data=json.dumps(assign_orders_400_val), content_type='application/json')
        assert resp.status_code == 400

    def test_assign_orders_400_nf(self):
        resp = self.app.post('/orders/assign', data=json.dumps(assign_orders_400_nf), content_type='application/json')
        assert resp.status_code == 400

    def test_assign_orders_200(self):
        resp = self.app.post('/orders/assign', data=json.dumps(assign_orders_200), content_type='application/json')
        assert resp.status_code == 200
        resp.json.pop('assign_time')
        assign_orders_200_resp.pop('assign_time')
        assert resp.json == assign_orders_200_resp

    def test_orders_201(self):
        resp = self.app.post('/orders', data=json.dumps(orders_201), content_type='application/json')
        print(resp.json)
        assert resp.status_code == 201
        assert resp.json == orders_201_resp

    def test_complete_400(self):
        resp = self.app.post('/orders/complete', data=json.dumps(complete_400), content_type='application/json')
        assert resp.status_code == 400

    def test_complete_200(self):
        initial_resp = self.app.post('/orders/assign', data=json.dumps(assign_orders_200),
                                     content_type='application/json')
        resp = self.app.post('/orders/complete', data=json.dumps(complete_200), content_type='application/json')
        print(resp.json)
        assert resp.status_code == 200
        assert resp.json == complete_200_resp

    def test_edit_courier_404(self):
        resp = self.app.patch('/couriers/777', data=json.dumps(edit_courier_200), content_type='application/json')
        assert resp.status_code == 404

    def test_edit_courier_400(self):
        resp = self.app.patch('/couriers/2', data=json.dumps(edit_courier_400), content_type='application/json')
        assert resp.status_code == 400
        assert resp.json == edit_courier_400_resp

    def test_edit_200(self):
        initial_assign = self.app.post('/orders/assign', data=json.dumps(assign_orders_200),
                                     content_type='application/json')
        initial_complete = self.app.post('/orders/complete', data=json.dumps(complete_200),
                                         content_type='application/json')
        resp = self.app.patch('/couriers/2', data=json.dumps(edit_courier_200), content_type='application/json')
        assert resp.status_code == 200
        assert resp.json == edit_courier_200_resp

    def test_get_404(self):
        resp = self.app.get('/couriers/777')
        assert resp.status_code == 404

    def test_get_200(self):
        initial_assign = self.app.post('/orders/assign', data=json.dumps(assign_orders_200),
                                       content_type='application/json')
        initial_complete = self.app.post('/orders/complete', data=json.dumps(complete_200),
                                         content_type='application/json')
        initial_edit = resp = self.app.patch('/couriers/2', data=json.dumps(edit_courier_200),
                                             content_type='application/json')
        resp = self.app.get('/couriers/2')
        get_courier_200.pop('rating')
        resp.json.pop('rating')
        assert resp.status_code == 200
        assert resp.json == get_courier_200
