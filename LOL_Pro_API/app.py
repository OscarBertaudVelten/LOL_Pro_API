from flask import Flask, request
import players_api

app = Flask(__name__)

@app.route('/player')
def get_player_info():
    pseudo = request.args.get('name', '')
    return players_api.Player(pseudo).__str__()

@app.route('/')
def helloworld():
    return 'hello world'

app.run("https://lol-pro-api-hnfpfecxbgddf6eg.francecentral-01.azurewebsites.net", 3030)
