from flask import Flask, config,render_template
from flask_cors import CORS
from flask_mail import Mail, Message
from config import Config
from models import db
from routes import routes
from resources import email
from common import gloVar

app = Flask(__name__)
db.init_app(app)
gloVar._init()
CORS(app, supports_credentials=True)
app.register_blueprint(routes, url_prefix='/')
app.config.from_object(Config)
app.config['MAIL_SERVER'] = "smtp.163.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "medicalge@163.com"
app.config['MAIL_PASSWORD'] = "TVLVJKBKVIOUREOC"
app.config['MAIL_DEFAULT_SENDER'] = 'medicalge@163.com'
mail = Mail(app)
gloVar.set_value('mailData',mail)
@app.route('/')
def hello_world():
    return 'Hello World part1!'
   

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
