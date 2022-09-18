from flask import Flask, Blueprint, request, jsonify
from utils.functions.trata_dados import trata_dados
from utils.database.DB import Database
from flask.views import MethodView

webhook_route = Blueprint('webhook_route', __name__)

class Webhook(MethodView):

    def __init__(self):
        self.db = Database()

    def get(self):
        resposta = request.args.get('hub.challenge')

        return resposta

    def post(self):
        data = request.json

        dados = trata_dados(data)

        if dados:
            self.db.insert('cb_menssage', dados)

        return jsonify({'mensagem': 'Mensagem recebida com sucesso!'}), 200

webhook_view = Webhook.as_view('webhook_view')
webhook_route.add_url_rule('/', view_func=webhook_view, methods=['POST', 'GET'])