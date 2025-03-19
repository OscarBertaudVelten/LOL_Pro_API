from flask import Flask, request
import json

from LOL_Pro_API import players_api
from LOL_Pro_API import teams_api

app = Flask(__name__)

@app.route('/player')
def get_player_info():
    name = request.args.get('name', '')
    return json.dumps(players_api.Player(name).to_dict())

@app.route('/team')
def get_team_info():
    name = request.args.get('name', '')
    return json.dumps(teams_api.Team(name).to_dict())

@app.route('/')
def helloworld():
    return 'hello world'

@app.route('/test')
def test():
    return "test"

app.run("0.0.0.0", 3000)
