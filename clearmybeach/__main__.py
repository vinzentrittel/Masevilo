'''
Hook for starting the service
'''

import argparse
from flask import Flask, redirect, url_for
from clearmybeach.main_map import create_blueprint

PARSER = argparse.ArgumentParser(description='Initialize ClearMyBeach web app')
PARSER.add_argument('--debug', action='store_true', help='Run the service in debug mode. Changes in source files will be applied instantly on the running service.')
ARGUMENTS = PARSER.parse_args()

def create_app():
    app = Flask(__name__)
    app.register_blueprint(create_blueprint())
    return app

create_app().run(debug=ARGUMENTS.debug)
