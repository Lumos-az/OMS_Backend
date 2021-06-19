from flask import Flask
from flask_cors import CORS
from config import Config
from models import db
from routes import routes

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app, supports_credentials=True)
app.register_blueprint(routes, url_prefix='/')


@app.route('/')
def hello_world():
    return 'Hello World231!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
