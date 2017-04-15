#!/usr/bin/env python3

import argparse
import bisect
import json
import random
from bottle import route, run, response, request, static_file
from functools import wraps
from time import time
import asyncio
import websockets
import threading


ROUND_TIME = 60*1000
service_names = ["capter", "electrohub", "fooddispenser", "redbutton", "settings", "stargate", "pool"]
team_names = ['Invisible', "saarsec", "Bushwhackers", "LC↯BC", "c00kies@venice", "ENOFLAG", "WE_0WN_Y0U",
              "Teamspin", "Honeypot", "Espacio", "Destructive Voice", "Переподвысмотрит", "[censored]",
              "SiBears", "Lights Out", "Shadow Servants", "BSUIR", "girav", "Tower Of Hanoi", "keva", "VoidHack", "MSHP SSL: The Elite Firm", "Гостевая 1", "Гостевая 2"]

def team_(x): return 't{}'.format(x)
def service_(x): return 's{}'.format(x)

def gtime(): return int(time()*1000)
def cround(): return (gtime() - start)//ROUND_TIME + 1

connected = set()


@route('/<filepath:path>')
def main_page(filepath):
    response = static_file(filepath, root='./')
    response.set_header("Cache-Control", "no-cache")
    return response


def tojson(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        response.content_type = 'application/json'
        return fn(*args, **kwargs)

    return wrapper


@route('/api/info')
@tojson
def info_page():
    return {
        'teams': {team_(i): team_names[i] for i in range(args.teams)},
        'services': {service_(i): service_names[i] for i in range(args.services)},
        'start': 0
    }


@route('/api/scoreboard')
@tojson
def scores_page():
    return {
        'table': scores,
        'status': '1',
        'round': cround()
    }


def update_events():
    last_upd = events[-1][1] if events else start
    current = gtime()

    for x in range(args.frequency*((current - last_upd)//1000)):
        attacker = random.randint(0, args.teams - 1)
        victim = attacker
        while victim == attacker:
            victim = random.randint(0, args.teams - 1)

        evt_time = int(last_upd + (x/args.frequency)*1000)
        events.append([
            (evt_time - start)//ROUND_TIME + 1,
            evt_time,
            service_(random.randint(0, args.services - 1)),
            team_(attacker), team_(victim)
        ])
        scores[team_(attacker)] += 1



@route('/scoreboard.json')
@tojson
def scoreboard_page():
    return {
        "round": cround(),
        "scoreboard": [
            {
                "name": team_names[t],
                "score": scores[team_(t)],
                "services": [
                    {
                        "flags": cround()*2 + 1,
                        "status": random.choice((101, 102, 103, 104, 110)),
                        "id": service_(s)
                    }
                    for s in range(args.services)
                ]
            }
            for t in range(args.teams)
        ]
    }


async def websockets_handler(websocket, path):
    global connected
    connected.add(websocket)
    await create_state()
    while True:
        await asyncio.sleep(1)
        if websocket not in connected:
            break


async def write_to_websocket(text):
    for ws in connected.copy():
        try:
            await ws.send(text)
        except:
            connected.remove(ws)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--teams', type=int, help='teams count',
                        default=22)
    parser.add_argument('-s', '--services', type=int, help='services count',
                        default=7)
    parser.add_argument('-q', '--frequency', type=int, help='attack frequency',
                        default=30)
    return parser.parse_args()


def websocket_server_run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(websockets_handler, '0.0.0.0', 8080)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    asyncio.ensure_future(create_states(), loop=loop)
    asyncio.ensure_future(create_attacks(), loop=loop)
    loop.run_forever()


async def create_attacks():
    while True:
        attacker = random.randint(0, args.teams - 1)
        victim = attacker
        while victim == attacker:
            victim = random.randint(0, args.teams - 1)

        event = {
            "type": "attack",
            "value": {
                "service_id": service_(random.randint(0, args.services - 1)),
                "attacker_id": team_(attacker),
                "victim_id": team_(victim)
            }
        }
        json_str = json.dumps(event)
        await write_to_websocket(json_str)
        await asyncio.sleep(1/args.frequency)


async def create_states():
    while True:
        await asyncio.sleep(10)
        await create_state()


async def create_state():
    update_events();
    container = {
        "type": "state",
        "value": gen_state()
    }
    json_str = json.dumps(container)
    await write_to_websocket(json_str)


def gen_state():
    return {
        "round": cround(),
        "scoreboard": [
            {
                "name": team_names[t],
                "score": scores[team_(t)],
                "services": [
                    {
                        "flags": random.choice((1, 2, 3)),
                        "status": random.choice((101, 102)),
                        "id": service_(s)
                    }
                    for s in range(args.services)
                    ]
            }
            for t in range(args.teams)
            ]
    }


if __name__ == '__main__':
    args = parse_args()
    start = gtime()
    events = []
    scores = {team_(i): 0 for i in range(args.teams)}

    thread = threading.Thread(target=websocket_server_run)
    thread.start()

    run(host='0.0.0.0', port=8000, debug=True, reloader=False)
