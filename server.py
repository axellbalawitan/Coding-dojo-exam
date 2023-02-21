from flask_app import app
from flask_app.controller import controller
from flask_app.model import appointment
from flask_app.model import users


if __name__=="__main__":
    app.run(debug=True)

