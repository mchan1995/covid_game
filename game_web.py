from flask import Flask, request, redirect
from uuid import uuid4

app = Flask(__name__)

user_state = {}


def make_map():
    return {
        "main_hall": {
            "pretty": "Entrance",
            "description": """
                <p>
                    You're in self isolation. You've started showing some symptoms of illness including a fever and new persistent cough.  
                </p>
                <p>
                    Your goal is to work out if you have COVID-19 and to survive self-isolation.
                </p>
               <p>
                    On your left is a is a bathroom. On your right is a door, and ahead of you is a staircase...
                </p>       
                <p>
                    What do you do?
                </p>

            """,
            "directions": {
                "Go to the bathroom": "bathroom",
                "Go through the doors on your right": "living_room",
                "Ascend the staircase": "staircase",
            },
            "items": []
        },


        "bathroom": {
            "pretty": "Bathroom",
            "description": """
                <p> 
                    You chose to go to the bathroom.
                </p>
                <p>
                    You wash your hands for at least 20 seconds. Did you know that this recommended time is to allow the lipids of the virus to be destroyed?
                </p>
                <p>
                    You also found some hand sanitiser, nice. Put it in your bag for later.
                </p>
            """,
            "directions": {
                "Back to the hall": "main_hall",
            },
            "items": ["Hand sanitiser"]
        },


        "living_room": {
            "pretty": "Living Room",
            "description": """
                <p>
                    You chose to go through the doors on your right...
                </p>
                <p>
                    "You can't come in unless you've washed your hands." you hear.
                </p>
                <p>
                    "It's fine, I've washed them and I even have hand sanitiser"
                </p>
                <p>
                    "OK fine"
                </p>
                 <p>
                    The door swings open.
                </p>
                <p>
                    On the wall opposite you are several <b>shelves</b>.
                    On your right there is a large <b>wardrobe</b>.
                    On your left is a <b>corridor</b> leading down into darkness.
                </p>
            """,
            "directions": {
                "Go back": "main_hall",
                "Explore the shelves": "shelves",
                "Try and open the wardrobe": "wardrobe",
                "Head down the corridor": "tbc",
            },
            "items": []
        },


        "staircase": {
            "pretty": "NJRKESLNJNZINZILFNRJS nooooooo NJRKLESNGKJLSNLKSJGNS",
            "description": """
                <p style = 'color: red'>
                    The house is not structurally sound, the staircase collapses and <br>YOU DIE</br>.
                </p>
                <p>
                    Not to worry, the powers that be have decided to revive you and give you one more chance.
                </p>
            """,
            "directions": {
            },
            "items": []
        },

        "door_handle":{
            "pretty": "Door is blocked",
            "description": """
                <p>
                    You try to go through the doors on your right...
                </p>
                <p>
                    "You can't come in unless you've washed your hands." you hear.
                </p>
                <p>
                    You haven't washed your hands yet and must go back.
                </p>
            """,
            "directions": {
                "Go back": "main_hall",
            },
            "items": []
        },

        "shelves":{
            "pretty": "These shelves are dusty...",
            "description": """
                <p>
                    The shelves contain nothing but a key and a screwdriver, which you put in your bag.
                </p>
               """,
            "directions": {
                "Continue exploring the room": "living_room",
            },
            "items": ["Key", "Screwdriver"]
        },

        "locked": {
            "pretty": "Damn it's locked",
            "description": """
            <p>
                You try and open the wardrobe but it is locked. Where could the key be?
            </p>
           """,
            "directions": {
                "Go back": "living_room",
            },
            "items": []
        },

        "wardrobe": {
            "pretty": "Wardrobe",
            "description": """
            <p>
                You try and open the wardrobe which is locked. You try the key from the shelf, which works.
            <p>
            <p>
                You find a thermometer.
            </p>
           """,
            "directions": {
                "Take temperature": "temperature",
                "Go back": "living_room"
            },
            "items": ["Thermometer"]
        },

        "temperature": {
            "pretty": "You take your temperature",
            "description": """
                    <p>
                        Uh oh, looks like your temperature is over 38.7 degrees...
                    </p>
                   """,
            "directions": {
                "Go back": "living_room",
            },
            "items": []
        },

        "tbc": {
            "pretty": "To be continued...",
            "description": """
                <p>
                    I haven't done any further than this. Watch this space.
                </p>
               """,
            "directions": {
                "Go back": "living_room",
            },
            "items": []
        }

    }


def add_user():
    user_id = str(uuid4())

    user_state[user_id] = {
        # the map. This contains info about all the locations, where the location
        # leads to, what items the location contains, etc
        # We store it on the player as they can modify it (eg, take an item and
        # put it in their inventory)
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

    current_location = user["map"][user["location"]]

    for direction, destination in current_location["directions"].items():
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

    location = user["map"][user["location"]]

    if direction in location["directions"]:
        user["location"] = location["directions"][direction]

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

    location = user["map"][user["location"]]
    location_pretty = location["pretty"]

    location_description = location["description"]

    new_items = location["items"]

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
            {location_description}

            <hr />
            {location_directions}
            </hr />

            <h2>Your bag contains:</h2>
            {inventory}

            <hr />
            <a href="/" style = 'color: gray'>Start new game</a>
            </div>
        </body>
        </html>
        """.format(location=location_pretty, location_description=location_description, location_directions=location_directions, inventory=inventory)


app.run()
