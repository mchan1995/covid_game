import json

# The map class contains a list of rooms
class Map:
    # The first room created gets id=0, if no rooms have been created the counter is -1
    room_id_counter = -1
    # limit the number of rooms
    #map_room_limit = 100
    # A dict of the rooms on the map
    rooms = {}

    # Creates a new map
    # Rooms are created based on the mapfile
    # TODO If no mapfile is specified, creates some random rooms instead
    def __init__(self, map_file):
        if map_file:
            print("Creating map from file: " + map_file)
            # read map json
            with open(map_file, 'r') as myfile:
                json_data = myfile.read()
            # parse file
            json_obj = json.loads(json_data)

            # the keys should be the rooms' names, we get them with [*json_obj]
            # we're going to create rooms using the names as the keys
            for room_name in [*json_obj]:
                # add a new room into rooms-dict with the key room_name
                # create a room and pass the specs from the json_obj using the room_name key
                # we pass an empty "" as the last argument, since the rooms have their directions already mapped
                self.rooms[room_name] = self.create_room(json_obj[room_name],"")

        # TODO in case no map file is provided, create some random rooms instead

    # Room id is based on this
    def increment_room_counter(self):
        self.room_id_counter += 1

    # Returns the count of how many rooms there are
    # (+1 because the first room's id is 0)
    def get_room_count(self):
        return self.room_id_counter+1

    # Returns a dictionary with the rooms in it
    def get_rooms(self):
        return self.rooms
    
    # Returns a Room-object
    # increments the room count by one and assigns the room a
    def create_room(self,room_specs,entered_from):
        self.increment_room_counter()
        return Room(self.get_room_count,room_specs,entered_from)

class Room:

    # Room variables
    id = -1
    #name = "Uninitialized room" # The name of the room is the key (TODO maybe id should be used instead)
    pretty = "This room hasn't been intialized"
    description = [ "The house is not structurally sound, <br>YOU DIED</br> ¯\\_(ツ)_/¯" ]
    items = []
    directions = {}

    # Creates a new room based on specs given
    # room_id is an int based on the room_id_counter in the map containing the room
    # entered_from is the room this room was entered from
    # room_specs is the other info associated with the room, name, description, directions etc.
    def __init__(self,room_id,room_specs,entered_from):

        self.id = room_id
        #self.name = room_specs.name
        self.pretty = room_specs["pretty"]
        self.description = room_specs["description"]
        self.directions = room_specs["directions"]
        self.items = room_specs["items"]

        if entered_from:
            self.directions["Go back"] = entered_from

    def get_specs(self):
        room_specs = {
                        "pretty": self.pretty,
                        "description": self.description,
                        "directions": self.directions,
                        "items": self.items,
                    }
        return room_specs 