from flask import Flask, request
import players_api

app = Flask(__name__)

@app.route('/player')
def get_player_info():
    pseudo = request.args.get('name', '')
    return players_api.Player(pseudo).__str__()

app.run("localhost", 3030)
