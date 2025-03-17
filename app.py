from flask import Flask, request
import json

from LOL_Pro_API import players_api
from LOL_Pro_API import teams_api

app = Flask(__name__)

@app.route('/player')
def get_player_info():
    pseudo = request.args.get('name', '')
    return json.dumps(players_api.Player(pseudo))

@app.route('/team')
def get_team_info():
    pseudo = request.args.get('name', '')
    return teams_api.Team(pseudo).__str__()

@app.route('/')
def helloworld():
    return 'hello world'

app.run("0.0.0.0", 3000)
