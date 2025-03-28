import functools
import traceback
import os
import json
from flask import Flask, request, jsonify, Response, send_file
from LOL_Pro_API import players_api, game_scoreboard_api, match_scoreboard_api, teams_api

app = Flask(__name__)

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)  # Crée le dossier cache s'il n'existe pas

def cache_result(filename):
    """ Décorateur pour mettre en cache les résultats des requêtes. """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Utilisation de get() pour éviter les KeyError
            cache_path = os.path.join(CACHE_DIR, filename.format(
                name=request.args.get('name', 'unknown'),
                nb_games=request.args.get('nb_games', '5')  # Valeur par défaut "5"
            ))

            # Vérifie si un cache existe
            if os.path.exists(cache_path):
                with open(cache_path, "r", encoding="utf-8") as file:
                    return jsonify(json.load(file))

            try:
                result = func(*args, **kwargs)  # Appelle la fonction si pas de cache

                # Sauvegarde le résultat
                with open(cache_path, "w", encoding="utf-8") as file:
                    json.dump(result.json, file, ensure_ascii=False, indent=4)

                return result
            except Exception as e:
                print(f"Error in {func.__name__}: {str(e)}")
                traceback.print_exc()
                return Response(status=429 if "ratelimited" in str(e) else 404)

        return wrapper
    return decorator


@app.route('/player', methods=['GET'])
@cache_result("player_{name}.json")
def get_player_info():
    name = request.args.get('name', '')
    player = players_api.Player(name)
    if player.Team:
        player.Team = player.Team.to_dict()
    return jsonify(player.__dict__)

@app.route('/team', methods=['GET'])
@cache_result("team_{name}.json")
def get_team_info():
    name = request.args.get('name', '')
    team = teams_api.Team(name)
    return jsonify(team.__dict__)

@app.route('/game', methods=['GET'])
@cache_result("game_{id}.json")
def get_game_info():
    game_id = request.args.get('id', '')
    game = game_scoreboard_api.GameScoreboard(game_id)
    game.Team1Stats = game.Team1Stats.to_dict()
    game.Team2Stats = game.Team2Stats.to_dict()
    return jsonify(game.__dict__)

@app.route('/match', methods=['GET'])
@cache_result("match_{id}.json")
def get_match_info():
    match_id = request.args.get('id', '')
    match = match_scoreboard_api.MatchScoreboard(match_id)
    for i in range(len(match.Games)):
        match.Games[i] = match.Games[i].to_dict()
    match.Team1 = match.Team1.to_dict()
    match.Team2 = match.Team2.to_dict()
    return jsonify(match.__dict__)

@app.route('/last_games', methods=['GET'])
@cache_result("last_games_{name}_{nb_games}.json")
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
