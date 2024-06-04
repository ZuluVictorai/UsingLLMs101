<!DOCTYPE html>
<html>
<head>
    <title>Rock, Paper, Scissors</title>
</head>
<body>
    <h1>Rock, Paper, Scissors</h1>
    <form action="{{ url_for('play') }}" method="post">
        <label>
            <input type="radio" name="choice" value="rock" checked>Rock
        </label>
        <label>
            <input type="radio" name="choice" value="paper">Paper
        </label>
        <label>
            <input type="radio" name="choice" value="scissors">Scissors
        </label>
        <br>
        <input type="submit" value="Play">
    </form>
</body>
</html>