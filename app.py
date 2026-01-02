from flask import Flask, render_template, request, redirect, url_for
from battleship import BattleshipGame

app = Flask(__name__)

# Global game instance (simple & acceptable for Project 3)
game = None


@app.route("/", methods=["GET", "POST"])
def setup():
    """
    Setup screen:
    - choose grid size
    - choose number of ships
    """
    global game

    if request.method == "POST":
        size = int(request.form.get("size", 8))
        ships = int(request.form.get("ships", 3))

        game = BattleshipGame(size=size, num_ships=ships)
        return redirect(url_for("play_game"))

    return render_template("setup.html")


@app.route("/game")
def play_game():
    """
    Main game screen (browser playable)
    """
    if game is None:
        return redirect(url_for("setup"))

    letters = [chr(65 + i) for i in range(game.size)]

    return render_template(
        "game.html",
        game=game,
        letters=letters
    )


@app.route("/fire", methods=["POST"])
def fire():
    """
    Handle a player shot from the browser
    """
    if game is None:
        return redirect(url_for("setup"))

    position = request.form.get("position", "").upper()
    game.player_turn(position)
    game.enemy_turn()

    return redirect(url_for("play_game"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
