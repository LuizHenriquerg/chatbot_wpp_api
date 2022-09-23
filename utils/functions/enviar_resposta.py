from datetime import date, datetime
from utils.database.DB import Database
import requests
import json
import time
import re
import os

class SendMessage:

    def __init__(self):
        self.db_harmony = Database('harmony')
        self.db = Database()
        self.url = os.environ.get('URL_SEND_MESSAGE')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {os.environ.get('TOKEN_WPP')}",
        }

    def save_reading_message(self, name, timestamp, number, step=None):
        self.db.update(
            'cb_menssage',
            {'read': True, 'step': step},
            {
                'name': name, 
                'number': number, 
                'timestamp': timestamp
            }
        )

    def verify_message(self, data):
        data = data[0]

        body = data.get('body')
        name = data.get('name')
        number = data.get('number')
        timestamp = data.get('timestamp')

        if body is not None:
            text_user = body.get('body', '0')

            if str(text_user) in ['1', '2', '3']:
                self.send_verify_user_message(number, name, timestamp, step=text_user)

                return True
            
            elif re.search(r'(\d{11}|\d{3}\.\d{3}\.\d{3}\-\d{2})', text_user) is not None:
                cpf = re.search(r'(\d{11}|\d{3}\.\d{3}\.\d{3}\-\d{2})', text_user).group()
                self.verify_user_message(number, name, timestamp, cpf)

                return True

            elif re.search(r'(falar)|(com)|(atendente)', text_user, flags=re.IGNORECASE) is not None or str(text_user) == '4':
                pass
            
            else:
                self.send_message_welcome(name, number, timestamp)

                return True

    def verify_user_message(self, number, name, timestamp, cpf):
        data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {
                "body": "Obrigada! Estamos verificando os seus dados...\nPor favor, aguarde um instante 😊"
            }
        }

        data = json.dumps(data)
    
        send = requests.post(self.url, headers=self.headers, data=data)

        verify_user = list(self.db_harmony.find_object('usuarios', 
            {
                'cpf': cpf.replace('-', '').replace('.', ''),
                'status': 'ativo'
            }
        ))

        if len(verify_user) > 0:
            step = list(self.db.find_object('cb_menssage',
                {
                    "number" : "5584999195328",
                    "name" : "Luiz Henrique",
                    "step": {"$ne": None}
                }
            ).sort('created_at', -1).limit(1))

            if len(step) == 0:
                pass

            step = str(step[0]['step'])

            if step == '1':
                dates_available = list(self.db_harmony.find_object('datas_consultas', {'status': None, 'id_cliente': None}).sort('data_formatada', 1).limit(10))
                print(dates_available)

                if len(dates_available) > 0:
                    rows = []

                    meses = {
                        '1': 'jan.',
                        '2': 'fev.',
                        '3': 'mar.',
                        '4': 'abr.',
                        '5': 'mai.',
                        '6': 'jun.',
                        '7': 'jul.',
                        '8': 'ago',
                        '9': 'set.',
                        '10': 'out.',
                        '11': 'nov.',
                        '12': 'dez.'
                    }

                    for dates in dates_available:
                        row = {
                            'id': str(dates['_id']),
                            'title': f'{dates["dia"]} de {meses[str(dates["mes"])]} às {dates["hora"]}:00.'
                        }
                        rows.append(row)
                    
                    data = {
                        "messaging_product": "whatsapp",
                        "recipient_type": "individual",
                        "to": "5584999195328",
                        "type": "interactive",
                        "interactive":{
                                "type": "list",
                                "body": {
                                "text": "Selecione uma data para marcar a sua consulta:"
                            },
                            "action": {
                                "button": "Datas disponíveis",
                                "sections":[
                                    {
                                        "title":"Datas:",
                                        "rows": rows
                                    }
                                ]
                            }
                        }
                    }

                    data = json.dumps(data)
                
                    send = requests.post(self.url, headers=self.headers, data=data)
                    self.db.insert('db_log_api', 
                        {
                            'created_at': datetime.now(),
                            'message': send.text,
                            'local': 'send_verify_user_message'  
                        }
                    )

                    self.save_reading_message(name, timestamp, number, step)

                    return True
                else:
                    data = {
                        "messaging_product": "whatsapp",
                        "to": number,
                        "type": "text",
                        "text": {
                            "body": "Infelizmente estamos sem datas disponíveis no momento...🙁\nMas assim que tiver uma disponível avisaremos por aqui! 😁\n\nAjudo em algo mais? Caso sim, digite *Falar com atendente* e caso não precise mais de ajuda digite *Sair*."
                        }
                    }

                    data = json.dumps(data)
                
                    send = requests.post(self.url, headers=self.headers, data=data)
                    self.db.insert('db_log_api', 
                        {
                            'created_at': datetime.now(),
                            'message': send.text,
                            'local': 'send_verify_user_message'  
                        }
                    )

                    self.save_reading_message(name, timestamp, number, step)

            if step == '2':
                pass

            if step == '3':
                pass

    def send_verify_user_message(self, number, name, timestamp, step):
        data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {
                "body": "Certo! Por favor digite seu CPF para verificar seu cadastro:"
            }
        }

        data = json.dumps(data)
    
        send = requests.post(self.url, headers=self.headers, data=data)
        self.db.insert('db_log_api', 
            {
                'created_at': datetime.now(),
                'message': send.text,
                'local': 'send_verify_user_message'  
            }
        )

        self.save_reading_message(name, timestamp, number, step)
    
    def send_message_talk_attendant(self, name, number, timestamp):
        pass

    def send_message_welcome(self, name, number, timestamp):
        data = {
            "messaging_product": "whatsapp",
            "to": number,
            "type": "text",
            "text": {
                "body": f"Olá, {name}. Seja bem-vindo ao Harmony! Como podemos lhe ajudar? \n\n1- Marcar consulta\n2- Remarcar consulta\n3- Cancelar consulta\n4- Falar com atendente\n\nHarmony agradece pelo contato. 😁"
            }
        }

        data = json.dumps(data)
    
        send = requests.post(self.url, headers=self.headers, data=data)

        self.db.insert('db_log_api', 
            {
                'created_at': datetime.now(),
                'message': send.text,
                'local': 'send_verify_user_message'  
            }
        )

        self.save_reading_message(name, timestamp, number)

