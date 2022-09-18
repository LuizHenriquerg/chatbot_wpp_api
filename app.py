from flask import Flask
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

from controllers.webhook.Webhook import Webhook
from controllers.webhook.Webhook import webhook_route

app.register_blueprint(webhook_route, url_prefix='/webhook')

if __name__ == '__main__':
    app.run(port='3030')