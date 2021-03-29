from app import app, db
from flask import json


class TestViews(object):

    def setup(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/TestViews'
        # app.testing = True
        self.app = app.test_client()
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_test(self):
        resp = {
            "data": [
                {
                    "courier_id": 1,
                    "courier_type": "foot",
                    "regions": [7, 20],
                    "working_hours": ["11:30-14:05", "09:00-11:00", "20:00-21:00"]
                },
                {
                    "courier_id": 2,
                    "courier_type": "car",
                    "regions": [1, 2, 3],
                    "working_hours": ["19:00-23:15"]
                },
                {
                    "courier_id": 3,
                    "courier_type": "bike",
                    "regions": [12, 22, 23, 33],
                    "working_hours": ["19:00-23:15", "11:35-14:05"]
                }
            ]
        }
        response = self.app.post('/couriers', data=json.dumps(resp), content_type='application/json')
        assert response.status_code == 201
