import json

ban_msg = [
    "flew to close to the radar and got banned",
    "messed up bad and got banned",
    "has been struck by the BAN HAMMER",
    "annoyed some staff and got banned",
    "wanted to see what would happen if you broke rules and got banned",
    "tried to dodge the ban hammer :rofl:",
    "was blown up by Creeper",
    "was killed by [Intentional Game Design]",
    "tried to swim in lava",
    "experienced kinetic energy",
    "drowned",
    "hit the ground too hard",
    "was squashed by a falling anvil",
    "was squished too much",
    "fell out of the world",
    "went up in flames",
    "went off with a bang",
    "was struck by lightning",
    "discovered the floor was lava",
]

kick_msg = [
    "got booted and got kicked?",
    "got kicked, imagine getting kicked...",
    "got kicked... I ran out of jokes",
]

def fetch_data(fn):
    with open("json/" + str(fn), "r") as f:
        data = json.load(f)
    return data


def write_data(fn, data):
    with open("json/" + str(fn), "w") as f:
        json.dump(data, f, indent=4)

def read_database():
    try:
        with open("database.json") as f:
            database=json.load(f)
    except:
        write_database(data={})
        database={}
    return database

def write_database(*, data):
    with open("database.json","w+") as f:
        json.dump(data, f, indent=4)