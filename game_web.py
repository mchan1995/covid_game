from flask import Flask, request, redirect
from uuid import uuid4

# Import the map and room classes
import maps_rooms as mr

app = Flask(__name__)

user_state = {}

# This is the filepath for the map that will be loaded
MAP_FILE_PATH = "default_map.json"

def make_map():
    map = mr.Map(MAP_FILE_PATH)
    return map

def add_user():
    user_id = str(uuid4())

    user_state[user_id] = {
        # the map. This contains info about all the locations, where the location
        # leads to, what items the location contains, etc
        # We store it on the player as they can modify it (eg, take an item and
        # put it in their inventory)
        # The Map object holds a collection of Rooms and a few other things inside it. See maps_rooms.py.
        "map": make_map(),

        # the current location in the map
        "location": "main_hall",

        # The player's inventory
        "inventory": [],
    }

    return user_id


def user_not_found():
    return """
    <html>
        <head>
            <title>Not Found</title>
        </head>
        <body>
            <h1>Oops, looks like you took a wrong turn</h1>

            <a href="/">Start a new game</a>
        </body>
    </html>
    """, 404

# allows user to click on the desired directions as links, and returns directions.
def format_location_directions(user_id, user):
    directions = ""

    current_location = user["map"].get_rooms()[user["location"]]

    for direction, destination in current_location.get_specs()["directions"].items():
        directions += "<div>"

        directions += "<a href='/game/{user_id}/{direction}' style = 'color: #AEE5E8'>{direction}</a>".format(
            user_id=user_id, direction=direction)

        directions += "</div>"

    return directions

# look at the user's destination items and add them to their persisted state user id.
def format_inventory(new_items, inventory):

    for items in new_items:
          inventory.append(items)

    if len(inventory) == 0:
        return ("Nothing.")

    return str(inventory)

# logic for if the user has chosen to go right from the main hall, into drawing room.
# if they have a candle & matches, they can light and continue.

def door_handle(user_id):
    user = user_state[user_id]
    inventory = user["inventory"]

    if "Hand sanitiser" in inventory:
        print("success")
        user["location"] = "living_room"

    else:
        # print (str(inventory))
        print("oops")
        user["location"] = "door_handle"

    return redirect("/game/{}".format(user_id), code=302)

def wardrobe(user_id):
    user = user_state[user_id]
    inventory = user["inventory"]

    if "Key" in inventory:
        print("success")
        user["location"] = "wardrobe"

    else:
        # print (str(inventory))
        print("oops")
        user["location"] = "locked"

    return redirect("/game/{}".format(user_id), code=302)

######################
# Flask Web routes
######################


@app.route('/')
def index():
    user_id = add_user()

    # 302 is a temporary redirect
    return redirect("/game/{}".format(user_id), code=302)


@app.route('/game/<user_id>/<direction>')
# move the user to new chosen location
def move_left(user_id, direction):
    if user_id not in user_state:
        return user_not_found()

    user = user_state[user_id]

    location = user["map"].get_rooms()[user["location"]]

    if direction in location.get_specs()["directions"]:
        user["location"] = location.get_specs()["directions"][direction]

    if user["location"] == "living_room":
        return door_handle(user_id)

    if user["location"] == "wardrobe":
        return wardrobe(user_id)

    return redirect("/game/{}".format(user_id), code=302)


@app.route('/game/<user_id>')
# show chosen location, options and inventory contents in predefined format
def game_screen(user_id):
    if user_id not in user_state:
        return user_not_found()

    user = user_state[user_id]

    location = user["map"].get_rooms()[user["location"]]
    location_pretty = location.get_specs()["pretty"]

    location_description = location.get_specs()["description"]

    new_items = location.get_specs()["items"]

    location_directions = format_location_directions(user_id, user)
    inventory = format_inventory(new_items, user["inventory"])

    return """
        <html>
        <head>
            <title>Self Isolation</title>
            <style>
                body{{
                    background: black;
                }}           
                
                .main {{
                    padding: 100px 250px 100px 250px;
                    font-family: Monaco;
                    color: white;
                }}
            </style>
        </head>
        <body>
            <div class = 'main'>
            <h1>{location}</h1>
            <p>{location_description}</p>

            <hr />
            <p>{location_directions}</p>
            </hr />

            <h2>Your bag contains:</h2>
            <p>{inventory}</p>

            <hr />
            <a href="/" style = 'color: gray'>Start new game</a>
            </div>
        </body>
        </html>
        """.format(location=location_pretty, location_description=location_description, location_directions=location_directions, inventory=inventory)


app.run()
