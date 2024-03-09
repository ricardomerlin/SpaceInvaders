from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, Player
# import request


app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

db.init_app(app)

@app.get('/players')
def get_players():
    players = Player.query.all()
    sorted_players = sorted(players, key=lambda player: player.score, reverse=True)[:10]
    return {'players': [{'username': player.username, 'score': player.score} for player in sorted_players]}

@app.post('/players')
def create_player():
    data = request.get_json()

    new_player = Player(
        username=data['username'],
        score=data.get('score')
    )

    db.session.add(new_player)
    db.session.commit()

    return {'id': new_player.id}, 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)