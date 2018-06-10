from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'AIfRZdlVfr4YomUmDGDItTgSWgsmFt1+bsaM95i0KaE='

from app import routes
