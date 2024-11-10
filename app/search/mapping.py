user_mapping = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'text'},
            'email': {'type': 'keyword'},
            'phone': {'type': 'long'},
            'role': {'type': 'keyword'},
            'acc_status': {'type': 'boolean'}
        }
    }
}


booking_mapping = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'user_id': {'type': 'integer'},
            'vehicle_id': {'type': 'integer'},
            'start_date': {
                'type': 'date',
                'format': 'dd-MM-yyy'
            },
            'end_date': {
                'type': 'date',
                'format': 'dd-MM-yyy'
            },
            'status': {'type': 'keyword'},
            'price': {'type': 'float'}
        }
    }
}


service_mapping = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'service_name': {'type': 'tetx'},
            'description': {'type': 'text'},
            'price': {'type': 'float'}
        }
    }
}


vehicle_maintenance_mapping = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'vehicle_id': {'type': 'integer'},
            'workshop_id': {'type': 'integer'},
            'service_date': {
                'type': 'date',
                'format': 'dd-MM-yyy'
            },
            'current_mileage': {'type': 'integer'},
            'status': {'type': 'keyword'}
        }
    }
}


vehicle_mapping = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'brand': {'type': 'text'},
            'model': {'type': 'text'},
            'release': {'type': 'integer'},
            'plate': {'type': 'text'},
            'mileage': {'type': 'integer'},
            'status': {'type': 'keyword'}
        }
    }
}


workshop_mapping = {
    'mappings': {
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'text'},
            'adress': {'type': 'text'},
            'phone': {'type': 'long'}
        }
    }
}

    
    