from controller.main import controller as con_main
from controller.signup import controller as con_signup
from controller.profile import controller as con_profile
from controller.card_registration import controller as con_card_registration
from controller.error_handler import controller as con_error

from flask import Flask
app = Flask(__name__)


con_error(app)
con_signup(app)
con_main(app)
con_card_registration(app)
con_profile(app)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 