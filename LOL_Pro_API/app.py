from flask import Flask, request
import players_api

app = Flask(__name__)

@app.route('/')
def get_player_info():
    pseudo = request.args.get('pseudo', '')
    return players_api.Player(pseudo).__str__()

app.run("localhost", 3030)
