import unittest
from collections import OrderedDict
from CasimirSimulation import CasimirSimulation
from flask import Flask, request, json, jsonify
from flask_restplus import Resource, Api, reqparse, Swagger,fields
from flask.views import View

app = Flask(__name__)

class TestCasimirSimulation(unittest.TestCase):

    def test_casimir_simulation_is_initialized_correctly(self):
        
        casimir_simulation = CasimirSimulation(app)

        