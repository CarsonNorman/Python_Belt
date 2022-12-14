from flask_app import app

from flask_app.controllers import login_controller
from flask_app.controllers import items_controller
from flask_app.controllers import likes_controller

if __name__ == '__main__':
    app.run(debug = True)