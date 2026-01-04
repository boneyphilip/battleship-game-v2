from flask import Flask, render_template, request, redirect, url_for
from battleship import BattleshipGame

app = Flask(__name__)

# Global game instance (simple & acceptable for Project 3)
game = None


@app.route("/", methods=["GET"])
def home():
    return render_template("setup.html")


@app.route("/setup", methods=["POST"])
def setup():
    """
    Create a new game from setup form
    """
    global game
    size = int(request.form.get("size", 8))
    ships = int(request.form.get("ships", 3))
    game = BattleshipGame(size=size, num_ships=ships)
    return redirect(url_for("play_game"))


@app.route("/game", methods=["GET"])
def play_game():
    """
    Main game screen (browser playable)
    """
    global game
    if game is None:
        return redirect(url_for("home"))

    return render_template("game.html", game=game, chr=chr)


@app.route("/fire", methods=["POST"])
def fire():
    """
    Handle a player shot from the browser
    """
    global game
    if game is None:
        return redirect(url_for("home"))

    position = request.form.get("position", "").upper()
    game.player_turn(position)

    # Enemy only plays if game still running
    if game.enemy_ships and game.player_ships:
        game.enemy_turn()

    return redirect(url_for("play_game"))


@app.route("/new-game", methods=["POST"])
def new_game():
    """
    Reset and go to setup again
    """
    global game
    game = None
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
