from flask import Blueprint
from flask import request
import os

app = Blueprint('blacklist', __name__)

@app.route('/')
def hello_world():  # put application's code here
    return f'Hello {os.getenv("DB_NAME")}'


@app.route('/<name>')
def hello_world_name(name):  # put application's code here
    return f'Hello World! {name} {os.getenv("HOLA", False)}'
