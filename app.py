from flask import Flask, request, jsonify
from flask_cors import CORS

import json

from LOL_Pro_API import players_api
from LOL_Pro_API import teams_api

app = Flask(__name__)
CORS(app)

@app.route('/player', methods=['GET'])
def get_player_info():
    name = request.args.get('name', '')
    player = players_api.Player(name)

    # Use to_dict() for serialization
    if player.Team:
        player.Team = player.Team.to_dict()

    return jsonify(player.__dict__)

@app.route('/team', methods=['GET'])
def get_team_info():
    name = request.args.get('name', '')
    team = teams_api.Team(name)

    return jsonify(team.__dict__)

@app.route('/')
def helloworld():
    return 'hello world'

@app.route('/test')
def test():
    return "test"

app.run("0.0.0.0", 3000)
