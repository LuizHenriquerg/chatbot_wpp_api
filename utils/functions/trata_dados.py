from datetime import datetime
import re

def trata_dados(data):
    id_wpp = None
    number = None
    name = None
    timestamp = None
    body = None
    type_menssage = None

    if 'entry' in data:
        entry = data['entry'][0]
        data_messages = entry['changes'][0]['value']

        id_wpp = entry['id']

        if 'contacts' not in data_messages or 'messages' not in data_messages:
            return False

        number_format = re.search(r'(\d{2})(\d{2})(\d{8,9})', data_messages['messages'][0]['from'])

        if len(number_format.group(3)) == 8:
            new_number = f'{number_format.group(1)}{number_format.group(2)}9{number_format.group(3)}'
        else:
            new_number = f'{number_format.group(1)}{number_format.group(2)}{number_format.group(3)}'

        name = data_messages['contacts'][0]['profile']['name']
        number = new_number
        timestamp = data_messages['messages'][0]['timestamp']
        type_menssage = data_messages['messages'][0]['type']
        body = data_messages['messages'][0][type_menssage]
    
    response = {
        'id_wpp': id_wpp,
        'number': number,
        'name': name,
        'timestamp': timestamp,
        'body': body,
        'type_menssage': type_menssage,
        'created_at': datetime.now(),
        'read': False
    }

    return response