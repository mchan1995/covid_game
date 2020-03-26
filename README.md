# COVID Game

A simple text-based game about self-isolation built with [Python](https://www.python.org/downloads/).

Uses [Flask](https://palletsprojects.com/p/flask/) to build into a basic web app. Install using [pip](https://pip.pypa.io/en/stable/quickstart/):

```
pip install Flask
```

Start the app locally by running the following in the project folder:

```
flask run
```

The map used right now is loaded from default_map.json. That 'journey path' can be extended by adding more rooms, items or whatever you wish into that file. Alternatively, another map can be created - to load it, change the MAP_FILE_PATH variable in app.py.

TODO: Random generation of rooms *should* be possible now that the rooms and map live in their respective objects. How will that be gameplaywise? Hard to say - it could be really cool or really dumb.