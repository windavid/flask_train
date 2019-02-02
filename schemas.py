payment = {
    'type': 'object',
    'properties': {
        "amount": {"type": "number"},
        "patientId": {"type": "string"},
        "externalId": {"type": "string"},
    },
    "required": ["amount", "patientId", "externalId"]
}

payment_arr = {
    'type': 'array',
    'items': payment
}

patient = {
    'type': 'object',
    'properties': {
        'firstName': {'type': 'string'},
        'lastName': {'type': 'string'},
        'dateOfBirth': {'type': 'string', 'format': 'date-time'},  # TODO: validate string is date
        'externalId': {'type': 'string'},
    },
    'required': ['firstName', 'lastName', 'dateOfBirth', 'externalId']
}

patient_arr = {
    'type': 'array',
    'items': patient
}
