"""
Main script.
"""
from dotenv import load_dotenv
from flask import Flask

from core import init_app

load_dotenv()

app = Flask(__name__)
init_app(app)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
