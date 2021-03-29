import arrow
from datetime import timedelta

initial_couriers = {
    "data": [
        {
            "courier_id": 1,
            "courier_type": "foot",
            "regions": [1, 5, 7, 20, 14],
            "working_hours": ["11:30-14:05", "09:00-11:00", "20:00-21:00"]
        },
        {
            "courier_id": 2,
            "courier_type": "car",
            "regions": [7, 3, 2, 1, 20],
            "working_hours": ["19:00-23:15", "11:35-14:05"]
        },
        {
            "courier_id": 3,
            "courier_type": "bike",
            "regions": [12, 22, 23, 33],
            "working_hours": ["01:30-06:45"]
        },
        {
            "courier_id": 4,
            "courier_type": "bike",
            "regions": [7, 8],
            "working_hours": ["14:46-17:09", "11:00-12:00"]
        },
        {
            "courier_id": 5,
            "courier_type": "car",
            "regions": [11],
            "working_hours": ["12:00-16:00", "09:13-10:45", "18:11-20:16", "21:44-23:15"]
        },
        {
            "courier_id": 6,
            "courier_type": "foot",
            "regions": [12, 22, 23, 33],
            "working_hours": ["17:00-22:15", "11:35-14:00"]
        },
        {
            "courier_id": 7,
            "courier_type": "bike",
            "regions": [46, 47],
            "working_hours": ["19:00-21:15"]
        }
    ]
}
couriers_400 = {
    "data": [
        {
            "courier_id": 1,
            "courier_type": "foot",
            "regions": [1, 5, 7, 20, 14],
            "working_hours": ["11:30-14:05", "09:00-11:00", "20:00-21:00"]
        },
        {
            "courier_id": 8,
            "courier_type": "plane",
            "regions": [],
            "working_hours": []
        },
        {
            "courier_id": 9,
            "courier_type": "bike",
            "regions": [12, 22, 23, 33],
            "working_hours": ["01:3-06:45"]
        },
        {
            "courier_id": "10",
            "courier_type": 81,
            "regions": ["7", 8],
            "working_hours": ["14:46-17:64", "12:00-11:00"]
        }
    ]
}
couriers_400_resp = {
    "validation_error": {
        "couriers": [
            {
                "courier_id": "Courier with this id already exists.",
                "id": 1
            },
            {
                "courier_type": [
                    "Must be one of: foot, bike, car."
                ],
                "regions": [
                    "This field is empty."
                ],
                "working_hours": [
                    "This field is empty."
                ],
                "id": 8
            },
            {
                "working_hours": {
                    "0": [
                        "String does not match expected pattern."
                    ]
                },
                "id": 9
            },
            {
                "courier_id": [
                    "Not a valid integer."
                ],
                "working_hours": {
                    "0": [
                        "String does not match expected pattern."
                    ],
                    "_schema": [
                        "String does not match expected pattern."
                    ]
                },
                "regions": {
                    "0": [
                        "Not a valid integer."
                    ]
                },
                "courier_type": [
                    "Not a valid string."
                ],
                "id": "10"
            }
        ]
    }
}
couriers_no_data_400 = {
    "courier_id": 11,
    "courier_type": "bike",
    "regions": [46, 47],
    "working_hours": ["19:00-21:15"]
}
couriers_no_data_400_resp = {
    "message": "Wrong structure, field 'Data' is required."
}
couriers_201 = {
    "data": [
        {
            "courier_id": 8,
            "courier_type": "bike",
            "regions": [46, 47],
            "working_hours": ["19:00-21:15"]
        }
    ]
}
couriers_201_resp = {
    "couriers": [
        {
            "id": 8
        }
    ]
}
initial_orders = {
    "data": [
        {
            "order_id": 1,
            "weight": 4.45,
            "region": 7,
            "delivery_hours": ["09:00-13:45", "20:15-21:40"]
        },
        {
            "order_id": 2,
            "weight": 4,
            "region": 20,
            "delivery_hours": ["09:00-20:30"]
        },
        {
            "order_id": 3,
            "weight": 34.46,
            "region": 11,
            "delivery_hours": ["10:45-11:30", "20:07-23:16"]
        },
        {
            "order_id": 4,
            "weight": 14,
            "region": 3,
            "delivery_hours": ["09:00-11:35"]
        },
        {
            "order_id": 5,
            "weight": 4,
            "region": 20,
            "delivery_hours": ["09:00-20:30"]
        },
        {
            "order_id": 6,
            "weight": 1.25,
            "region": 7,
            "delivery_hours": ["15:00-16:30", "00:00-01:36"]
        },
        {
            "order_id": 7,
            "weight": 4,
            "region": 7,
            "delivery_hours": ["09:00-20:30"]
        },
        {
            "order_id": 8,
            "weight": 14.99,
            "region": 33,
            "delivery_hours": ["21:00-23:59", "00:05-01:35"]
        },
        {
            "order_id": 9,
            "weight": 8,
            "region": 46,
            "delivery_hours": ["20:00-20:30", "07:45-11:35", "14:34-16:46"]
        },
        {
            "order_id": 10,
            "weight": 4,
            "region": 20,
            "delivery_hours": ["09:00-20:30"]
        },
        {
            "order_id": 11,
            "weight": 0.65,
            "region": 12,
            "delivery_hours": ["13:45-18:00", "21:30-23:00"]
        },
        {
            "order_id": 12,
            "weight": 17.6,
            "region": 4,
            "delivery_hours": ["15:55-19:04", "07:11-15:54"]
        }
    ]
}
orders_400 = {
    "data": [
        {
            "order_id": 1,
            "weight": 4.456,
            "region": "region",
            "delivery_hours": ["13:45-09:00", "26:15-21:40"]
        },
        {
            "order_id": -13,
            "weight": 0,
            "region": -20,
            "delivery_hours": []
        },
        {
            "order_id": 14,
            "weight": 51,
            "region": 11,
            "delivery_hours": ["10:4-11:30", 12345]
        }
    ]
}
orders_400_resp = {
    "validation_error": {
        "orders": [
            {
                "order_id": "Order with this id already exists.",
                "delivery_hours": {
                    "1": [
                        "String does not match expected pattern."
                    ],
                    "_schema": [
                        "String does not match expected pattern."
                    ]
                },
                "region": [
                    "Not a valid integer."
                ],
                "id": 1
            },
            {
                "order_id": [
                    "Must be greater than or equal to 1."
                ],
                "region": [
                    "Must be greater than or equal to 1."
                ],
                "weight": [
                    "Value out of range."
                ],
                "delivery_hours": [
                    "This field is empty."
                ],
                "id": -13
            },
            {
                "delivery_hours": {
                    "0": [
                        "String does not match expected pattern."
                    ],
                    "1": [
                        "Not a valid string."
                    ]
                },
                "weight": [
                    "Value out of range."
                ],
                "id": 14
            }
        ]
    }
}
orders_no_data = {
    "order_id": 12,
    "weight": 17.6,
    "region": 4,
    "delivery_hours": ["15:55-19:04", "07:11-15:54"]
}
orders_201 = {
    "data": [
        {
            "order_id": 13,
            "weight": 17.6,
            "region": 4,
            "delivery_hours": ["14:00-16:00"]
        }
    ]
}
orders_201_resp = {
    "orders": [
        {
            "id": 13
        }
    ]
}
assign_orders_400_val = {

}
assign_orders_400_nf = {
    "courier_id": 777
}
assign_orders_200 = {
    "courier_id": 2
}
assign_time = arrow.utcnow().isoformat()[:-10] + 'Z'
assign_orders_200_resp = {
    "orders": [
        {
            "id": 2
        },
        {
            "id": 5
        },
        {
            "id": 7
        },
        {
            "id": 10
        },
        {
            "id": 1
        }
    ],
    "assign_time": assign_time
}
complete_time = (arrow.utcnow() + timedelta(minutes=15)).isoformat()[:-10] + 'Z'
complete_200 = {
    "courier_id": 2,
    "order_id": 5,
    "complete_time": complete_time
}
complete_200_resp = {
    "order_id": 5
}
complete_400 = {
    "courier_id": 777,
    "order_id": 5,
    "complete_time": "2021-03-29T03:34:12.05Z"
}
edit_courier_400 = {
    "unknown": "unknown"
}
edit_courier_400_resp = {
    "unknown": [
        "Unknown field."
    ]
}
edit_courier_200 = {
    "regions": [3, 2, 1]
}
edit_courier_200_resp = {
    "courier_id": 2,
    "courier_type": "car",
    "regions": [
        3,
        2,
        1
    ],
    "working_hours": [
        "19:00-23:15",
        "11:35-14:05"
    ]
}
# courier_id = 2
get_courier_200 = {
    "courier_id": 2,
    "courier_type": "car",
    "regions": [3, 2, 1],
    "working_hours": [
        "19:00-23:15",
        "11:35-14:05"
    ],
    "earnings": 4500,
    "rating": 3.75
}
