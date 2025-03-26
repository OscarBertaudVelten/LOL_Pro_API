from flask import Flask, request, jsonify, Response, send_file

from LOL_Pro_API import players_api, game_scoreboard_api, match_scoreboard_api
from LOL_Pro_API import teams_api

app = Flask(__name__)

@app.route('/player', methods=['GET'])
def get_player_info():
    name = request.args.get('name', '')
    try:
        player = players_api.Player(name)

        # Use to_dict() for serialization
        if player.Team:
            player.Team = player.Team.to_dict()

        return jsonify(player.__dict__)
    except:
        return Response(status=404)

@app.route('/team', methods=['GET'])
def get_team_info():
    name = request.args.get('name', '')
    team = teams_api.Team(name)

    return jsonify(team.__dict__)


@app.route('/game', methods=['GET'])
def get_game_info():
    game_id = request.args.get('id', '')
    game = game_scoreboard_api.GameScoreboard(game_id)

    game.Team1Stats = game.Team1Stats.to_dict()
    game.Team2Stats = game.Team2Stats.to_dict()

    return jsonify(game.__dict__)


@app.route('/match', methods=['GET'])
def get_match_info():
    match_id = request.args.get('id', '')
    match = match_scoreboard_api.MatchScoreboard(match_id)

    for i in range (len(match.Games)):
        match.Games[i] = match.Games[i].to_dict()

    match.Team1 = match.Team1.to_dict()
    match.Team2 = match.Team2.to_dict()

    return jsonify(match.__dict__)


@app.route('/last_games', methods=['GET'])
def get_last_player_games():
    name = request.args.get('name', '')
    nb_games = request.args.get('nb_games', 5)

    return jsonify(match_scoreboard_api.get_last_n_matches_of_player(name, nb_games))


@app.route('/trending_players')
def get_trending_players():
    return send_file('LOL_Pro_API/scripts/top_players.json', mimetype='application/json')


@app.route('/')
def helloworld():
    return 'hello world'


app.run("0.0.0.0", 80)
