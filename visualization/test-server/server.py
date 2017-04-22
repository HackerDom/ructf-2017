#!/usr/bin/env python3

import argparse
import json
import random
from bottle import route, run, response, static_file
from functools import wraps
from time import time
import asyncio
import websockets
import threading

stat = [
  {"round":475,"scoreboard":[{"d":0,"host":"team4.ructf","n":1,"name":"Bushwhackers","round":475,"score":"17532.39","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":2563,"fp":15552.13,"id":2,"sflags":43,"sla":98.53,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":14,"sla":68.21,"status":104,"stdout":"connection problem\n"},{"flags":509,"fp":1620.23,"id":4,"sflags":95,"sla":70.74,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":247,"fp":985.76,"id":6,"sflags":84,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":4},{"d":0,"host":"team14.ructf","n":2,"name":"Shadow Servants","round":475,"score":"11106.11","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":17,"sla":91.16,"status":104,"stdout":"No connect\n"},{"flags":11,"fp":89.86,"id":3,"sflags":24,"sla":68.21,"status":104,"stdout":""},{"flags":221,"fp":863.79,"id":4,"sflags":152,"sla":78.53,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1697,"fp":10755.31,"id":6,"sflags":331,"sla":95.58,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.74,"status":101,"stdout":""}],"team_id":14},{"d":0,"host":"team12.ructf","n":3,"name":"Lights Out","round":475,"score":"10498.68","services":[{"flags":10,"fp":34.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":431,"fp":6335.53,"id":2,"sflags":1,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":81.05,"status":104,"stdout":""},{"flags":116,"fp":1379.16,"id":4,"sflags":93,"sla":79.37,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.42,"status":101,"stdout":""},{"flags":662,"fp":3277.22,"id":6,"sflags":777,"sla":92.63,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":95.37,"status":101,"stdout":""}],"team_id":12},{"d":0,"host":"team15.ructf","n":4,"name":"SiBears","round":475,"score":"10321.23","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":135,"sla":97.68,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":74.53,"status":104,"stdout":""},{"flags":1177,"fp":7531.98,"id":4,"sflags":2,"sla":92.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.32,"status":101,"stdout":""},{"flags":796,"fp":3296.78,"id":6,"sflags":47,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":15},{"d":0,"host":"team18.ructf","n":5,"name":"Tower Of Hanoi","round":475,"score":"10269.83","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":166.0,"id":2,"sflags":69,"sla":58.74,"status":103,"stdout":"Put failed\n"},{"flags":0,"fp":0.0,"id":3,"sflags":18,"sla":54.95,"status":104,"stdout":"\nhttp http:\/\/electrohub.team18.ructf\/signup\/ status 500\n"},{"flags":936,"fp":4765.29,"id":4,"sflags":31,"sla":82.74,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.21,"status":101,"stdout":""},{"flags":1344,"fp":6271.77,"id":6,"sflags":109,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.53,"status":101,"stdout":""}],"team_id":18},{"d":0,"host":"team11.ructf","n":6,"name":"LC↯BC","round":475,"score":"9112.16","services":[{"flags":1,"fp":25.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":75,"fp":350.41,"id":2,"sflags":152,"sla":55.58,"status":101,"stdout":""},{"flags":56,"fp":169.42,"id":3,"sflags":16,"sla":69.05,"status":104,"stdout":""},{"flags":501,"fp":2246.97,"id":4,"sflags":23,"sla":86.32,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.16,"status":101,"stdout":""},{"flags":1554,"fp":8166.7,"id":6,"sflags":14,"sla":83.16,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":94.95,"status":101,"stdout":""}],"team_id":11},{"d":0,"host":"team5.ructf","n":7,"name":"c00kies@venice","round":475,"score":"8203.13","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":280.66,"id":2,"sflags":210,"sla":89.47,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":85.89,"status":101,"stdout":""},{"flags":403,"fp":2027.61,"id":4,"sflags":15,"sla":56.42,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":2045,"fp":11366.76,"id":6,"sflags":8,"sla":58.95,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":96.42,"status":101,"stdout":""}],"team_id":5},{"d":0,"host":"team7.ructf","n":8,"name":"ENOFLAG","round":475,"score":"8055.68","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":126,"sla":88.42,"status":101,"stdout":""},{"flags":101,"fp":446.44,"id":3,"sflags":0,"sla":98.53,"status":101,"stdout":""},{"flags":167,"fp":595.61,"id":4,"sflags":381,"sla":84.84,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.47,"status":101,"stdout":""},{"flags":1229,"fp":7037.36,"id":6,"sflags":10,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":7},{"d":0,"host":"team6.ructf","n":9,"name":"[censored]","round":475,"score":"7525.61","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":5,"fp":22.65,"id":2,"sflags":76,"sla":93.68,"status":101,"stdout":""},{"flags":166,"fp":851.26,"id":3,"sflags":0,"sla":78.74,"status":101,"stdout":""},{"flags":263,"fp":862.24,"id":4,"sflags":553,"sla":87.37,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1050,"fp":6044.17,"id":6,"sflags":930,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":6},{"d":0,"host":"team16.ructf","n":10,"name":"TeamSpin","round":475,"score":"6897.84","services":[{"flags":13,"fp":37.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1,"fp":0.0,"id":2,"sflags":181,"sla":88.21,"status":101,"stdout":""},{"flags":17,"fp":148.19,"id":3,"sflags":9,"sla":19.58,"status":103,"stdout":"add order item failed\n"},{"flags":239,"fp":2092.37,"id":4,"sflags":191,"sla":78.11,"status":103,"stdout":"Couldn't find flag!\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.16,"status":101,"stdout":""},{"flags":911,"fp":5160.99,"id":6,"sflags":742,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.53,"status":101,"stdout":""}],"team_id":16},{"d":0,"host":"team13.ructf","n":11,"name":"saarsec","round":475,"score":"6822.34","services":[{"flags":23,"fp":47.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":177,"sla":97.68,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":8,"sla":86.11,"status":101,"stdout":""},{"flags":352,"fp":2843.71,"id":4,"sflags":105,"sla":88.84,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":88.63,"status":103,"stdout":"Invalid HTTP response\n"},{"flags":1353,"fp":4487.58,"id":6,"sflags":99,"sla":93.68,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.89,"status":101,"stdout":""}],"team_id":13},{"d":0,"host":"team19.ructf","n":12,"name":"WE_0WN_Y0U","round":475,"score":"4358.86","services":[{"flags":0,"fp":24.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":37,"fp":508.62,"id":2,"sflags":230,"sla":99.79,"status":101,"stdout":""},{"flags":88,"fp":530.78,"id":3,"sflags":22,"sla":75.16,"status":104,"stdout":""},{"flags":177,"fp":857.99,"id":4,"sflags":745,"sla":81.47,"status":104,"stdout":"Response timed out\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.58,"status":101,"stdout":""},{"flags":478,"fp":2683.78,"id":6,"sflags":644,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":19},{"d":0,"host":"team20.ructf","n":13,"name":"Destructive Voice","round":475,"score":"4248.30","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":142,"sla":99.16,"status":101,"stdout":""},{"flags":259,"fp":1304.65,"id":3,"sflags":0,"sla":72.21,"status":104,"stdout":""},{"flags":359,"fp":2338.99,"id":4,"sflags":68,"sla":85.89,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":272,"fp":1276.99,"id":6,"sflags":868,"sla":95.37,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.68,"status":101,"stdout":""}],"team_id":20},{"d":0,"host":"team2.ructf","n":14,"name":"Переподвысмотрит","round":475,"score":"3713.07","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":140,"fp":1898.46,"id":2,"sflags":216,"sla":93.89,"status":101,"stdout":""},{"flags":16,"fp":150.98,"id":3,"sflags":20,"sla":78.53,"status":104,"stdout":""},{"flags":148,"fp":129.42,"id":4,"sflags":647,"sla":93.05,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.79,"status":101,"stdout":""},{"flags":2296,"fp":1725.84,"id":6,"sflags":922,"sla":93.05,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.53,"status":101,"stdout":""}],"team_id":2},{"d":0,"host":"team3.ructf","n":15,"name":"BSUIR","round":475,"score":"3056.64","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":264,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":15,"sla":90.32,"status":101,"stdout":""},{"flags":295,"fp":2679.01,"id":4,"sflags":163,"sla":87.58,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.68,"status":101,"stdout":""},{"flags":107,"fp":826.35,"id":6,"sflags":1477,"sla":76.42,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.68,"status":101,"stdout":""}],"team_id":3},{"d":0,"host":"team17.ructf","n":16,"name":"VoidHack","round":475,"score":"2205.47","services":[{"flags":11,"fp":35.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":254,"sla":99.58,"status":101,"stdout":""},{"flags":66,"fp":429.5,"id":3,"sflags":23,"sla":73.05,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":933,"sla":52.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":170,"fp":2341.69,"id":6,"sflags":225,"sla":77.26,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.68,"status":101,"stdout":""}],"team_id":17},{"d":0,"host":"team22.ructf","n":17,"name":"Гостевая 2","round":475,"score":"1651.44","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":164,"sla":99.16,"status":104,"stdout":"No connect\n"},{"flags":0,"fp":0.0,"id":3,"sflags":113,"sla":26.74,"status":103,"stdout":"add order item failed\n"},{"flags":174,"fp":2032.05,"id":4,"sflags":206,"sla":77.47,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1819,"sla":94.74,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.47,"status":101,"stdout":""}],"team_id":22},{"d":0,"host":"team10.ructf","n":18,"name":"keva","round":475,"score":"1612.05","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":137,"sla":74.32,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":73.89,"status":104,"stdout":""},{"flags":102,"fp":1651.75,"id":4,"sflags":54,"sla":91.37,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1319,"sla":72.84,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":10},{"d":0,"host":"team9.ructf","n":19,"name":"girav","round":475,"score":"1244.85","services":[{"flags":7,"fp":31.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":207,"sla":85.68,"status":104,"stdout":"No connect\n"},{"flags":59,"fp":440.13,"id":3,"sflags":7,"sla":73.68,"status":104,"stdout":""},{"flags":261,"fp":2287.76,"id":4,"sflags":227,"sla":36.84,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.05,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":686,"sla":55.37,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.47,"status":101,"stdout":""}],"team_id":9},{"d":0,"host":"team23.ructf","n":20,"name":"MSHP SSL: The Elite Firm","round":475,"score":"762.02","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":88,"sla":89.05,"status":101,"stdout":""},{"flags":3,"fp":2.21,"id":3,"sflags":387,"sla":57.26,"status":101,"stdout":""},{"flags":361,"fp":913.7,"id":4,"sflags":792,"sla":73.68,"status":110,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":2021,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.89,"status":101,"stdout":""}],"team_id":23},{"d":0,"host":"team1.ructf","n":21,"name":"Honeypot","round":475,"score":"729.52","services":[{"flags":5,"fp":29.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":98,"sla":82.32,"status":101,"stdout":""},{"flags":127,"fp":818.38,"id":3,"sflags":0,"sla":79.79,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":47,"sla":92.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":422,"sla":40.63,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":1},{"d":0,"host":"team8.ructf","n":22,"name":"Espacio","round":475,"score":"694.69","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":189,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":90.32,"status":101,"stdout":""},{"flags":205,"fp":992.91,"id":4,"sflags":811,"sla":59.16,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1512,"sla":73.47,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":96.21,"status":101,"stdout":""}],"team_id":8},{"d":0,"host":"team21.ructf","n":23,"name":"Гостевая 1","round":475,"score":"554.29","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":204,"sla":99.58,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":293,"sla":38.32,"status":104,"stdout":""},{"flags":421,"fp":920.35,"id":4,"sflags":1053,"sla":50.74,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":95.16,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1145,"sla":70.95,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.89,"status":101,"stdout":""}],"team_id":21},{"d":0,"host":"team24.ructf","n":24,"name":"Invisible","round":475,"score":"0.00","services":[{"flags":0,"fp":0.0,"id":1,"sflags":250,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":2,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":4,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":6,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":0.0,"status":104,"stdout":""}],"team_id":24}]},
  {"round":476,"scoreboard":[{"d":0,"host":"team4.ructf","n":1,"name":"Bushwhackers","round":476,"score":"17552.76","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":2567,"fp":15568.63,"id":2,"sflags":43,"sla":98.53,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":14,"sla":68.07,"status":104,"stdout":"connection problem\n"},{"flags":509,"fp":1620.23,"id":4,"sflags":95,"sla":70.8,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":248,"fp":988.39,"id":6,"sflags":84,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":4},{"d":0,"host":"team14.ructf","n":2,"name":"Shadow Servants","round":476,"score":"11116.30","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":17,"sla":90.97,"status":104,"stdout":"No connect\n"},{"flags":11,"fp":89.86,"id":3,"sflags":24,"sla":68.07,"status":104,"stdout":""},{"flags":221,"fp":863.79,"id":4,"sflags":152,"sla":78.57,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1699,"fp":10764.65,"id":6,"sflags":331,"sla":95.59,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.74,"status":101,"stdout":""}],"team_id":14},{"d":0,"host":"team12.ructf","n":3,"name":"Lights Out","round":476,"score":"10524.39","services":[{"flags":10,"fp":34.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":432,"fp":6348.63,"id":2,"sflags":1,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":81.09,"status":101,"stdout":""},{"flags":116,"fp":1379.16,"id":4,"sflags":93,"sla":79.2,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.43,"status":101,"stdout":""},{"flags":667,"fp":3292.75,"id":6,"sflags":777,"sla":92.65,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":95.38,"status":101,"stdout":""}],"team_id":12},{"d":0,"host":"team15.ructf","n":4,"name":"SiBears","round":476,"score":"10322.46","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":143,"sla":97.69,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":74.37,"status":104,"stdout":""},{"flags":1177,"fp":7531.98,"id":4,"sflags":2,"sla":92.02,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.32,"status":101,"stdout":""},{"flags":796,"fp":3296.78,"id":6,"sflags":47,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":15},{"d":0,"host":"team18.ructf","n":5,"name":"Tower Of Hanoi","round":476,"score":"10271.61","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":166.0,"id":2,"sflags":69,"sla":58.61,"status":103,"stdout":"Put failed\n"},{"flags":0,"fp":0.0,"id":3,"sflags":18,"sla":54.83,"status":104,"stdout":"\nhttp http:\/\/electrohub.team18.ructf\/signup\/ status 500\n"},{"flags":936,"fp":4765.29,"id":4,"sflags":31,"sla":82.77,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.22,"status":101,"stdout":""},{"flags":1344,"fp":6271.77,"id":6,"sflags":109,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.53,"status":101,"stdout":""}],"team_id":18},{"d":0,"host":"team11.ructf","n":6,"name":"LC↯BC","round":476,"score":"9116.34","services":[{"flags":1,"fp":25.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":79,"fp":379.21,"id":2,"sflags":152,"sla":55.67,"status":101,"stdout":""},{"flags":56,"fp":169.42,"id":3,"sflags":16,"sla":68.91,"status":104,"stdout":""},{"flags":501,"fp":2246.97,"id":4,"sflags":23,"sla":86.34,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.18,"status":101,"stdout":""},{"flags":1555,"fp":8168.72,"id":6,"sflags":14,"sla":82.98,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":94.96,"status":101,"stdout":""}],"team_id":11},{"d":0,"host":"team5.ructf","n":7,"name":"c00kies@venice","round":476,"score":"8186.20","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":65,"fp":275.38,"id":2,"sflags":211,"sla":89.5,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":85.71,"status":104,"stdout":""},{"flags":403,"fp":2027.61,"id":4,"sflags":15,"sla":56.51,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":2045,"fp":11366.76,"id":6,"sflags":8,"sla":58.82,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":96.43,"status":101,"stdout":""}],"team_id":5},{"d":0,"host":"team7.ructf","n":8,"name":"ENOFLAG","round":476,"score":"8062.13","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":127,"sla":88.45,"status":101,"stdout":""},{"flags":101,"fp":446.44,"id":3,"sflags":0,"sla":98.53,"status":101,"stdout":""},{"flags":167,"fp":595.61,"id":4,"sflags":381,"sla":84.87,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.48,"status":101,"stdout":""},{"flags":1231,"fp":7043.59,"id":6,"sflags":10,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":7},{"d":0,"host":"team6.ructf","n":9,"name":"[censored]","round":476,"score":"7526.83","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":5,"fp":22.65,"id":2,"sflags":76,"sla":93.7,"status":101,"stdout":""},{"flags":166,"fp":851.26,"id":3,"sflags":0,"sla":78.78,"status":101,"stdout":""},{"flags":263,"fp":862.24,"id":4,"sflags":553,"sla":87.18,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1051,"fp":6046.5,"id":6,"sflags":930,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":6},{"d":0,"host":"team16.ructf","n":10,"name":"TeamSpin","round":476,"score":"6896.11","services":[{"flags":13,"fp":37.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1,"fp":0.0,"id":2,"sflags":181,"sla":88.24,"status":101,"stdout":""},{"flags":17,"fp":148.19,"id":3,"sflags":9,"sla":19.54,"status":103,"stdout":"add order item failed\n"},{"flags":239,"fp":2092.37,"id":4,"sflags":191,"sla":78.15,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.16,"status":101,"stdout":""},{"flags":912,"fp":5158.33,"id":6,"sflags":743,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.53,"status":101,"stdout":""}],"team_id":16},{"d":0,"host":"team13.ructf","n":11,"name":"saarsec","round":476,"score":"6821.89","services":[{"flags":23,"fp":47.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":178,"sla":97.69,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":8,"sla":86.13,"status":101,"stdout":""},{"flags":352,"fp":2843.71,"id":4,"sflags":105,"sla":88.87,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":88.66,"status":101,"stdout":""},{"flags":1355,"fp":4485.75,"id":6,"sflags":100,"sla":93.7,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.9,"status":101,"stdout":""}],"team_id":13},{"d":0,"host":"team19.ructf","n":12,"name":"WE_0WN_Y0U","round":476,"score":"4551.08","services":[{"flags":0,"fp":24.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":45,"fp":700.62,"id":2,"sflags":230,"sla":99.79,"status":101,"stdout":""},{"flags":88,"fp":530.78,"id":3,"sflags":22,"sla":75.21,"status":101,"stdout":""},{"flags":177,"fp":857.99,"id":4,"sflags":745,"sla":81.51,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.6,"status":101,"stdout":""},{"flags":478,"fp":2683.78,"id":6,"sflags":644,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":19},{"d":0,"host":"team20.ructf","n":13,"name":"Destructive Voice","round":476,"score":"4254.34","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":143,"sla":99.16,"status":101,"stdout":""},{"flags":259,"fp":1304.65,"id":3,"sflags":0,"sla":72.06,"status":104,"stdout":""},{"flags":359,"fp":2338.99,"id":4,"sflags":68,"sla":85.92,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":273,"fp":1284.54,"id":6,"sflags":868,"sla":95.38,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.69,"status":101,"stdout":""}],"team_id":20},{"d":0,"host":"team2.ructf","n":14,"name":"Переподвысмотрит","round":476,"score":"3704.16","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":140,"fp":1888.63,"id":2,"sflags":218,"sla":93.91,"status":101,"stdout":""},{"flags":16,"fp":150.98,"id":3,"sflags":20,"sla":78.57,"status":101,"stdout":""},{"flags":148,"fp":129.42,"id":4,"sflags":647,"sla":92.86,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.79,"status":101,"stdout":""},{"flags":2296,"fp":1725.84,"id":6,"sflags":922,"sla":93.07,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.53,"status":101,"stdout":""}],"team_id":2},{"d":0,"host":"team3.ructf","n":15,"name":"BSUIR","round":476,"score":"3056.02","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":266,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":15,"sla":90.34,"status":101,"stdout":""},{"flags":295,"fp":2679.01,"id":4,"sflags":163,"sla":87.61,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.69,"status":101,"stdout":""},{"flags":107,"fp":826.35,"id":6,"sflags":1477,"sla":76.26,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.69,"status":101,"stdout":""}],"team_id":3},{"d":0,"host":"team17.ructf","n":16,"name":"VoidHack","round":476,"score":"2206.83","services":[{"flags":11,"fp":35.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":255,"sla":99.58,"status":101,"stdout":""},{"flags":66,"fp":429.5,"id":3,"sflags":23,"sla":73.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":933,"sla":51.89,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":170,"fp":2341.69,"id":6,"sflags":225,"sla":77.31,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.69,"status":101,"stdout":""}],"team_id":17},{"d":0,"host":"team22.ructf","n":17,"name":"Гостевая 2","round":476,"score":"1652.40","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":164,"sla":98.95,"status":104,"stdout":"No connect\n"},{"flags":0,"fp":0.0,"id":3,"sflags":113,"sla":26.68,"status":103,"stdout":"add order item failed\n"},{"flags":174,"fp":2032.05,"id":4,"sflags":206,"sla":77.52,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1824,"sla":94.75,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.48,"status":101,"stdout":""}],"team_id":22},{"d":0,"host":"team10.ructf","n":18,"name":"keva","round":476,"score":"1612.32","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":137,"sla":74.16,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":73.74,"status":104,"stdout":""},{"flags":102,"fp":1651.75,"id":4,"sflags":54,"sla":91.39,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1319,"sla":72.69,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":10},{"d":0,"host":"team9.ructf","n":19,"name":"girav","round":476,"score":"1242.40","services":[{"flags":7,"fp":31.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":207,"sla":85.5,"status":104,"stdout":"No connect\n"},{"flags":59,"fp":440.13,"id":3,"sflags":7,"sla":73.53,"status":104,"stdout":""},{"flags":261,"fp":2287.76,"id":4,"sflags":227,"sla":36.76,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.06,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":686,"sla":55.25,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.48,"status":101,"stdout":""}],"team_id":9},{"d":0,"host":"team23.ructf","n":20,"name":"MSHP SSL: The Elite Firm","round":476,"score":"760.60","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":88,"sla":89.08,"status":101,"stdout":""},{"flags":3,"fp":2.21,"id":3,"sflags":387,"sla":57.35,"status":101,"stdout":""},{"flags":361,"fp":913.7,"id":4,"sflags":792,"sla":73.53,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":2030,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.9,"status":101,"stdout":""}],"team_id":23},{"d":0,"host":"team1.ructf","n":21,"name":"Honeypot","round":476,"score":"728.15","services":[{"flags":5,"fp":29.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":98,"sla":82.35,"status":101,"stdout":""},{"flags":127,"fp":818.38,"id":3,"sflags":0,"sla":79.62,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":47,"sla":92.02,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":422,"sla":40.55,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":1},{"d":0,"host":"team8.ructf","n":22,"name":"Espacio","round":476,"score":"695.55","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":189,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":90.34,"status":101,"stdout":""},{"flags":205,"fp":992.91,"id":4,"sflags":811,"sla":59.24,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1512,"sla":73.32,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":96.22,"status":101,"stdout":""}],"team_id":8},{"d":0,"host":"team21.ructf","n":23,"name":"Гостевая 1","round":476,"score":"553.31","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":205,"sla":99.58,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":293,"sla":38.24,"status":104,"stdout":""},{"flags":421,"fp":920.35,"id":4,"sflags":1053,"sla":50.63,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":95.17,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1145,"sla":70.8,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":97.9,"status":101,"stdout":""}],"team_id":21},{"d":0,"host":"team24.ructf","n":24,"name":"Invisible","round":476,"score":"0.00","services":[{"flags":0,"fp":0.0,"id":1,"sflags":250,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":2,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":4,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":6,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":0.0,"status":104,"stdout":""}],"team_id":24}]},
  {"round":477,"scoreboard":[{"d":0,"host":"team4.ructf","n":1,"name":"Bushwhackers","round":477,"score":"17668.28","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":2569,"fp":15576.08,"id":2,"sflags":43,"sla":98.53,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":14,"sla":67.92,"status":104,"stdout":"connection problem\n"},{"flags":509,"fp":1596.23,"id":4,"sflags":96,"sla":70.65,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":249,"fp":991.02,"id":6,"sflags":84,"sla":100.0,"status":101,"stdout":""},{"flags":19,"fp":150.55,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":4},{"d":0,"host":"team14.ructf","n":2,"name":"Shadow Servants","round":477,"score":"11103.60","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":17,"sla":90.99,"status":101,"stdout":""},{"flags":11,"fp":89.86,"id":3,"sflags":24,"sla":67.92,"status":104,"stdout":""},{"flags":222,"fp":865.57,"id":4,"sflags":152,"sla":78.62,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1700,"fp":10772.21,"id":6,"sflags":331,"sla":95.39,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.74,"status":101,"stdout":""}],"team_id":14},{"d":0,"host":"team12.ructf","n":3,"name":"Lights Out","round":477,"score":"10550.74","services":[{"flags":10,"fp":34.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":435,"fp":6386.09,"id":2,"sflags":1,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":80.92,"status":104,"stdout":""},{"flags":116,"fp":1379.16,"id":4,"sflags":93,"sla":79.04,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.44,"status":101,"stdout":""},{"flags":669,"fp":3301.73,"id":6,"sflags":777,"sla":92.66,"status":101,"stdout":""},{"flags":0,"fp":5.79,"id":7,"sflags":1,"sla":95.39,"status":101,"stdout":""}],"team_id":12},{"d":0,"host":"team15.ructf","n":4,"name":"SiBears","round":477,"score":"10311.22","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":144,"sla":97.69,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":74.42,"status":101,"stdout":""},{"flags":1177,"fp":7531.98,"id":4,"sflags":2,"sla":92.03,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.32,"status":101,"stdout":""},{"flags":797,"fp":3299.82,"id":6,"sflags":47,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":8.14,"id":7,"sflags":1,"sla":98.11,"status":101,"stdout":""}],"team_id":15},{"d":0,"host":"team18.ructf","n":5,"name":"Tower Of Hanoi","round":477,"score":"10279.64","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":166.0,"id":2,"sflags":69,"sla":58.49,"status":103,"stdout":"Put failed\n"},{"flags":0,"fp":0.0,"id":3,"sflags":18,"sla":54.72,"status":104,"stdout":"\nhttp http:\/\/electrohub.team18.ructf\/signup\/ status 500\n"},{"flags":937,"fp":4789.29,"id":4,"sflags":31,"sla":82.81,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.23,"status":101,"stdout":""},{"flags":1344,"fp":6271.77,"id":6,"sflags":109,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":10.19,"id":7,"sflags":1,"sla":98.53,"status":101,"stdout":""}],"team_id":18},{"d":0,"host":"team11.ructf","n":6,"name":"LC↯BC","round":477,"score":"9094.67","services":[{"flags":1,"fp":25.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":79,"fp":379.21,"id":2,"sflags":152,"sla":55.77,"status":101,"stdout":""},{"flags":56,"fp":169.42,"id":3,"sflags":16,"sla":68.97,"status":101,"stdout":""},{"flags":501,"fp":2246.97,"id":4,"sflags":23,"sla":86.37,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.19,"status":101,"stdout":""},{"flags":1556,"fp":8172.16,"id":6,"sflags":14,"sla":82.81,"status":104,"stdout":""},{"flags":0,"fp":11.97,"id":7,"sflags":1,"sla":94.97,"status":101,"stdout":""}],"team_id":11},{"d":0,"host":"team5.ructf","n":7,"name":"c00kies@venice","round":477,"score":"8168.35","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":65,"fp":275.38,"id":2,"sflags":211,"sla":89.52,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":85.74,"status":101,"stdout":""},{"flags":403,"fp":2027.61,"id":4,"sflags":15,"sla":56.6,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":2047,"fp":11374.16,"id":6,"sflags":8,"sla":58.7,"status":104,"stdout":""},{"flags":0,"fp":13.52,"id":7,"sflags":1,"sla":96.44,"status":101,"stdout":""}],"team_id":5},{"d":0,"host":"team7.ructf","n":8,"name":"ENOFLAG","round":477,"score":"8059.63","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":127,"sla":88.47,"status":101,"stdout":""},{"flags":101,"fp":446.44,"id":3,"sflags":0,"sla":98.53,"status":101,"stdout":""},{"flags":167,"fp":595.61,"id":4,"sflags":381,"sla":84.91,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.48,"status":101,"stdout":""},{"flags":1233,"fp":7049.82,"id":6,"sflags":10,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":14.88,"id":7,"sflags":1,"sla":98.11,"status":101,"stdout":""}],"team_id":7},{"d":0,"host":"team6.ructf","n":9,"name":"[censored]","round":477,"score":"7526.88","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":5,"fp":12.97,"id":2,"sflags":77,"sla":93.71,"status":101,"stdout":""},{"flags":166,"fp":851.26,"id":3,"sflags":0,"sla":78.83,"status":101,"stdout":""},{"flags":263,"fp":862.24,"id":4,"sflags":553,"sla":87.21,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1058,"fp":6062.84,"id":6,"sflags":930,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":16.05,"id":7,"sflags":1,"sla":98.11,"status":101,"stdout":""}],"team_id":6},{"d":0,"host":"team16.ructf","n":10,"name":"TeamSpin","round":477,"score":"6883.18","services":[{"flags":13,"fp":37.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1,"fp":0.0,"id":2,"sflags":181,"sla":88.26,"status":101,"stdout":""},{"flags":17,"fp":148.19,"id":3,"sflags":9,"sla":19.5,"status":103,"stdout":"add order item failed\n"},{"flags":239,"fp":2092.37,"id":4,"sflags":191,"sla":77.99,"status":103,"stdout":"Couldn't find flag!\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.16,"status":101,"stdout":""},{"flags":913,"fp":5155.68,"id":6,"sflags":744,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":17.08,"id":7,"sflags":1,"sla":98.53,"status":101,"stdout":""}],"team_id":16},{"d":0,"host":"team13.ructf","n":11,"name":"saarsec","round":477,"score":"6815.69","services":[{"flags":23,"fp":47.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":179,"sla":97.69,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":8,"sla":86.16,"status":101,"stdout":""},{"flags":352,"fp":2843.71,"id":4,"sflags":105,"sla":88.89,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":88.47,"status":103,"stdout":"Invalid HTTP response\n"},{"flags":1356,"fp":4484.13,"id":6,"sflags":101,"sla":93.71,"status":101,"stdout":""},{"flags":0,"fp":17.97,"id":7,"sflags":1,"sla":97.9,"status":101,"stdout":""}],"team_id":13},{"d":0,"host":"team19.ructf","n":12,"name":"WE_0WN_Y0U","round":477,"score":"4585.46","services":[{"flags":0,"fp":24.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":51,"fp":750.54,"id":2,"sflags":230,"sla":99.79,"status":101,"stdout":""},{"flags":88,"fp":530.78,"id":3,"sflags":22,"sla":75.05,"status":104,"stdout":""},{"flags":177,"fp":833.99,"id":4,"sflags":746,"sla":81.34,"status":104,"stdout":"Response timed out\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.61,"status":101,"stdout":""},{"flags":479,"fp":2690.17,"id":6,"sflags":644,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.32,"status":101,"stdout":""}],"team_id":19},{"d":0,"host":"team20.ructf","n":13,"name":"Destructive Voice","round":477,"score":"4272.70","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":143,"sla":99.16,"status":101,"stdout":""},{"flags":259,"fp":1304.65,"id":3,"sflags":0,"sla":71.91,"status":104,"stdout":""},{"flags":360,"fp":2362.99,"id":4,"sflags":68,"sla":85.95,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":275,"fp":1290.9,"id":6,"sflags":868,"sla":95.18,"status":104,"stdout":""},{"flags":0,"fp":19.43,"id":7,"sflags":1,"sla":97.69,"status":101,"stdout":""}],"team_id":20},{"d":0,"host":"team2.ructf","n":14,"name":"Переподвысмотрит","round":477,"score":"3697.07","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":140,"fp":1884.65,"id":2,"sflags":219,"sla":93.92,"status":101,"stdout":""},{"flags":16,"fp":150.98,"id":3,"sflags":20,"sla":78.62,"status":101,"stdout":""},{"flags":148,"fp":129.42,"id":4,"sflags":647,"sla":92.87,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.79,"status":101,"stdout":""},{"flags":2296,"fp":1725.84,"id":6,"sflags":922,"sla":93.08,"status":101,"stdout":""},{"flags":0,"fp":20.02,"id":7,"sflags":1,"sla":98.53,"status":101,"stdout":""}],"team_id":2},{"d":0,"host":"team3.ructf","n":15,"name":"BSUIR","round":477,"score":"3121.35","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":267,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":15,"sla":90.36,"status":101,"stdout":""},{"flags":295,"fp":2679.01,"id":4,"sflags":163,"sla":87.63,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.69,"status":101,"stdout":""},{"flags":116,"fp":917.47,"id":6,"sflags":1477,"sla":76.1,"status":103,"stdout":""},{"flags":0,"fp":20.53,"id":7,"sflags":1,"sla":97.69,"status":101,"stdout":""}],"team_id":3},{"d":0,"host":"team17.ructf","n":16,"name":"VoidHack","round":477,"score":"2205.24","services":[{"flags":11,"fp":35.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":261,"sla":99.58,"status":101,"stdout":""},{"flags":66,"fp":429.5,"id":3,"sflags":23,"sla":73.17,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":933,"sla":51.78,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":170,"fp":2341.69,"id":6,"sflags":225,"sla":77.36,"status":101,"stdout":""},{"flags":0,"fp":20.98,"id":7,"sflags":1,"sla":97.69,"status":101,"stdout":""}],"team_id":17},{"d":0,"host":"team22.ructf","n":17,"name":"Гостевая 2","round":477,"score":"1646.54","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":164,"sla":98.74,"status":104,"stdout":"No connect\n"},{"flags":0,"fp":0.0,"id":3,"sflags":113,"sla":26.62,"status":103,"stdout":"add order item failed\n"},{"flags":174,"fp":2032.05,"id":4,"sflags":206,"sla":77.36,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1840,"sla":94.76,"status":101,"stdout":""},{"flags":0,"fp":21.37,"id":7,"sflags":1,"sla":97.48,"status":101,"stdout":""}],"team_id":22},{"d":0,"host":"team10.ructf","n":18,"name":"keva","round":477,"score":"1610.33","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":137,"sla":74.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":73.58,"status":104,"stdout":""},{"flags":102,"fp":1651.75,"id":4,"sflags":54,"sla":91.4,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1319,"sla":72.54,"status":104,"stdout":""},{"flags":0,"fp":21.71,"id":7,"sflags":1,"sla":98.32,"status":101,"stdout":""}],"team_id":10},{"d":0,"host":"team9.ructf","n":19,"name":"girav","round":477,"score":"1238.02","services":[{"flags":7,"fp":31.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":207,"sla":85.32,"status":104,"stdout":"No connect\n"},{"flags":59,"fp":440.13,"id":3,"sflags":7,"sla":73.38,"status":104,"stdout":""},{"flags":261,"fp":2287.76,"id":4,"sflags":227,"sla":36.69,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.06,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":686,"sla":55.14,"status":104,"stdout":""},{"flags":0,"fp":22.0,"id":7,"sflags":1,"sla":97.48,"status":101,"stdout":""}],"team_id":9},{"d":0,"host":"team23.ructf","n":20,"name":"MSHP SSL: The Elite Firm","round":477,"score":"756.19","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":88,"sla":89.1,"status":101,"stdout":""},{"flags":3,"fp":2.21,"id":3,"sflags":387,"sla":57.44,"status":101,"stdout":""},{"flags":361,"fp":911.92,"id":4,"sflags":793,"sla":73.38,"status":110,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":2043,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":22.26,"id":7,"sflags":1,"sla":97.9,"status":101,"stdout":""}],"team_id":23},{"d":0,"host":"team1.ructf","n":21,"name":"Honeypot","round":477,"score":"726.79","services":[{"flags":5,"fp":29.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":98,"sla":82.18,"status":103,"stdout":"Bad answer\n"},{"flags":127,"fp":818.38,"id":3,"sflags":0,"sla":79.45,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":47,"sla":92.03,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":422,"sla":40.46,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.11,"status":101,"stdout":""}],"team_id":1},{"d":0,"host":"team8.ructf","n":22,"name":"Espacio","round":477,"score":"693.06","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":189,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":90.36,"status":101,"stdout":""},{"flags":205,"fp":992.91,"id":4,"sflags":811,"sla":59.12,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.11,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1512,"sla":73.17,"status":104,"stdout":""},{"flags":0,"fp":22.68,"id":7,"sflags":1,"sla":96.23,"status":101,"stdout":""}],"team_id":8},{"d":0,"host":"team21.ructf","n":23,"name":"Гостевая 1","round":477,"score":"551.21","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":205,"sla":99.58,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":293,"sla":38.16,"status":104,"stdout":""},{"flags":421,"fp":920.35,"id":4,"sflags":1053,"sla":50.52,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":95.18,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1145,"sla":70.65,"status":104,"stdout":""},{"flags":0,"fp":22.85,"id":7,"sflags":1,"sla":97.9,"status":101,"stdout":""}],"team_id":21},{"d":0,"host":"team24.ructf","n":24,"name":"Invisible","round":477,"score":"0.00","services":[{"flags":0,"fp":0.0,"id":1,"sflags":250,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":2,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":4,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":6,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":0.0,"status":104,"stdout":""}],"team_id":24}]},
  {"round":478,"scoreboard":[{"d":0,"host":"team4.ructf","n":1,"name":"Bushwhackers","round":478,"score":"17686.87","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":2575,"fp":15594.17,"id":2,"sflags":43,"sla":98.54,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":14,"sla":67.78,"status":104,"stdout":"connection problem\n"},{"flags":509,"fp":1596.23,"id":4,"sflags":96,"sla":70.5,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":250,"fp":993.66,"id":6,"sflags":84,"sla":100.0,"status":101,"stdout":""},{"flags":19,"fp":150.55,"id":7,"sflags":0,"sla":98.33,"status":101,"stdout":""}],"team_id":4},{"d":0,"host":"team14.ructf","n":2,"name":"Shadow Servants","round":478,"score":"11084.06","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":18,"sla":91.0,"status":101,"stdout":""},{"flags":11,"fp":89.86,"id":3,"sflags":24,"sla":67.78,"status":104,"stdout":""},{"flags":222,"fp":865.57,"id":4,"sflags":152,"sla":78.66,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1701,"fp":10773.99,"id":6,"sflags":331,"sla":95.19,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.74,"status":101,"stdout":""}],"team_id":14},{"d":0,"host":"team12.ructf","n":3,"name":"Lights Out","round":478,"score":"10573.89","services":[{"flags":10,"fp":34.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":436,"fp":6397.35,"id":2,"sflags":1,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":80.75,"status":104,"stdout":""},{"flags":116,"fp":1379.16,"id":4,"sflags":93,"sla":78.87,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.44,"status":101,"stdout":""},{"flags":673,"fp":3316.49,"id":6,"sflags":777,"sla":92.68,"status":101,"stdout":""},{"flags":0,"fp":5.79,"id":7,"sflags":1,"sla":95.4,"status":101,"stdout":""}],"team_id":12},{"d":0,"host":"team15.ructf","n":4,"name":"SiBears","round":478,"score":"10296.73","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":144,"sla":97.7,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":74.48,"status":101,"stdout":""},{"flags":1177,"fp":7531.98,"id":4,"sflags":2,"sla":91.84,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.33,"status":101,"stdout":""},{"flags":797,"fp":3299.82,"id":6,"sflags":47,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":8.14,"id":7,"sflags":1,"sla":98.12,"status":101,"stdout":""}],"team_id":15},{"d":0,"host":"team18.ructf","n":5,"name":"Tower Of Hanoi","round":478,"score":"10271.39","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":166.0,"id":2,"sflags":69,"sla":58.37,"status":103,"stdout":"Put failed\n"},{"flags":0,"fp":0.0,"id":3,"sflags":18,"sla":54.6,"status":104,"stdout":"\nhttp http:\/\/electrohub.team18.ructf\/signup\/ status 500\n"},{"flags":937,"fp":4789.29,"id":4,"sflags":31,"sla":82.64,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.23,"status":101,"stdout":""},{"flags":1344,"fp":6271.77,"id":6,"sflags":109,"sla":98.12,"status":101,"stdout":""},{"flags":0,"fp":10.19,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":18},{"d":0,"host":"team11.ructf","n":6,"name":"LC↯BC","round":478,"score":"9099.32","services":[{"flags":1,"fp":25.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":81,"fp":411.53,"id":2,"sflags":152,"sla":55.86,"status":101,"stdout":""},{"flags":56,"fp":169.42,"id":3,"sflags":16,"sla":68.83,"status":104,"stdout":""},{"flags":501,"fp":2246.97,"id":4,"sflags":23,"sla":86.4,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.21,"status":101,"stdout":""},{"flags":1556,"fp":8172.16,"id":6,"sflags":14,"sla":82.64,"status":104,"stdout":""},{"flags":0,"fp":11.97,"id":7,"sflags":1,"sla":94.98,"status":101,"stdout":""}],"team_id":11},{"d":0,"host":"team5.ructf","n":7,"name":"c00kies@venice","round":478,"score":"8179.02","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":66,"fp":276.58,"id":2,"sflags":211,"sla":89.54,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":85.56,"status":104,"stdout":""},{"flags":403,"fp":2027.61,"id":4,"sflags":15,"sla":56.49,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":2048,"fp":11377.86,"id":6,"sflags":8,"sla":58.79,"status":101,"stdout":""},{"flags":0,"fp":13.52,"id":7,"sflags":1,"sla":96.23,"status":104,"stdout":"get \/ failed\n"}],"team_id":5},{"d":0,"host":"team7.ructf","n":8,"name":"ENOFLAG","round":478,"score":"8061.14","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":128,"sla":88.49,"status":101,"stdout":""},{"flags":101,"fp":446.44,"id":3,"sflags":0,"sla":98.33,"status":104,"stdout":""},{"flags":167,"fp":595.61,"id":4,"sflags":381,"sla":84.94,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.49,"status":101,"stdout":""},{"flags":1234,"fp":7052.03,"id":6,"sflags":10,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":14.88,"id":7,"sflags":1,"sla":98.12,"status":101,"stdout":""}],"team_id":7},{"d":0,"host":"team6.ructf","n":9,"name":"[censored]","round":478,"score":"7527.60","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":5,"fp":12.97,"id":2,"sflags":77,"sla":93.72,"status":101,"stdout":""},{"flags":166,"fp":851.26,"id":3,"sflags":0,"sla":78.87,"status":101,"stdout":""},{"flags":263,"fp":862.24,"id":4,"sflags":553,"sla":87.24,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1058,"fp":6062.84,"id":6,"sflags":930,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":16.05,"id":7,"sflags":1,"sla":98.12,"status":101,"stdout":""}],"team_id":6},{"d":0,"host":"team16.ructf","n":10,"name":"TeamSpin","round":478,"score":"6888.99","services":[{"flags":13,"fp":37.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1,"fp":0.0,"id":2,"sflags":181,"sla":88.28,"status":101,"stdout":""},{"flags":17,"fp":148.19,"id":3,"sflags":9,"sla":19.46,"status":104,"stdout":""},{"flags":239,"fp":2092.37,"id":4,"sflags":191,"sla":78.03,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.16,"status":101,"stdout":""},{"flags":914,"fp":5160.57,"id":6,"sflags":744,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":17.08,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":16},{"d":0,"host":"team13.ructf","n":11,"name":"saarsec","round":478,"score":"6819.65","services":[{"flags":23,"fp":47.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":179,"sla":97.7,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":8,"sla":86.19,"status":101,"stdout":""},{"flags":352,"fp":2843.71,"id":4,"sflags":105,"sla":88.7,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":88.49,"status":101,"stdout":""},{"flags":1360,"fp":4493.37,"id":6,"sflags":102,"sla":93.72,"status":101,"stdout":""},{"flags":0,"fp":17.97,"id":7,"sflags":1,"sla":97.91,"status":101,"stdout":""}],"team_id":13},{"d":0,"host":"team19.ructf","n":12,"name":"WE_0WN_Y0U","round":478,"score":"4611.62","services":[{"flags":0,"fp":24.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":53,"fp":779.05,"id":2,"sflags":231,"sla":99.79,"status":101,"stdout":""},{"flags":88,"fp":530.78,"id":3,"sflags":22,"sla":74.9,"status":104,"stdout":""},{"flags":177,"fp":833.99,"id":4,"sflags":746,"sla":81.17,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.63,"status":101,"stdout":""},{"flags":479,"fp":2690.17,"id":6,"sflags":644,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.12,"status":103,"stdout":"await msg failed\n"}],"team_id":19},{"d":0,"host":"team20.ructf","n":13,"name":"Destructive Voice","round":478,"score":"4274.12","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":146,"sla":99.16,"status":101,"stdout":""},{"flags":259,"fp":1304.65,"id":3,"sflags":0,"sla":71.76,"status":104,"stdout":""},{"flags":360,"fp":2362.99,"id":4,"sflags":68,"sla":85.77,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":277,"fp":1301.63,"id":6,"sflags":868,"sla":94.98,"status":104,"stdout":""},{"flags":0,"fp":19.43,"id":7,"sflags":1,"sla":97.7,"status":101,"stdout":""}],"team_id":20},{"d":0,"host":"team2.ructf","n":14,"name":"Переподвысмотрит","round":478,"score":"3689.71","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":140,"fp":1880.67,"id":2,"sflags":220,"sla":93.93,"status":101,"stdout":""},{"flags":16,"fp":150.98,"id":3,"sflags":20,"sla":78.45,"status":104,"stdout":""},{"flags":148,"fp":129.42,"id":4,"sflags":647,"sla":92.68,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.79,"status":101,"stdout":""},{"flags":2296,"fp":1725.84,"id":6,"sflags":922,"sla":92.89,"status":104,"stdout":""},{"flags":0,"fp":20.02,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":2},{"d":0,"host":"team3.ructf","n":15,"name":"BSUIR","round":478,"score":"3120.58","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":268,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":15,"sla":90.38,"status":101,"stdout":""},{"flags":295,"fp":2679.01,"id":4,"sflags":163,"sla":87.66,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.7,"status":101,"stdout":""},{"flags":116,"fp":917.47,"id":6,"sflags":1477,"sla":75.94,"status":103,"stdout":""},{"flags":0,"fp":20.53,"id":7,"sflags":1,"sla":97.7,"status":101,"stdout":""}],"team_id":3},{"d":0,"host":"team17.ructf","n":16,"name":"VoidHack","round":478,"score":"2205.69","services":[{"flags":11,"fp":35.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":262,"sla":99.58,"status":101,"stdout":""},{"flags":66,"fp":429.5,"id":3,"sflags":23,"sla":73.01,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":933,"sla":51.67,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":170,"fp":2341.69,"id":6,"sflags":225,"sla":77.41,"status":101,"stdout":""},{"flags":0,"fp":20.98,"id":7,"sflags":1,"sla":97.7,"status":101,"stdout":""}],"team_id":17},{"d":0,"host":"team22.ructf","n":17,"name":"Гостевая 2","round":478,"score":"1643.25","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":164,"sla":98.54,"status":104,"stdout":"No connect\n"},{"flags":0,"fp":0.0,"id":3,"sflags":113,"sla":26.57,"status":104,"stdout":""},{"flags":174,"fp":2032.05,"id":4,"sflags":206,"sla":77.2,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.95,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1848,"sla":94.77,"status":101,"stdout":""},{"flags":0,"fp":21.37,"id":7,"sflags":1,"sla":97.49,"status":101,"stdout":""}],"team_id":22},{"d":0,"host":"team10.ructf","n":18,"name":"keva","round":478,"score":"1610.59","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":137,"sla":73.85,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":73.43,"status":104,"stdout":""},{"flags":102,"fp":1651.75,"id":4,"sflags":54,"sla":91.42,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.12,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1319,"sla":72.38,"status":104,"stdout":""},{"flags":0,"fp":21.71,"id":7,"sflags":1,"sla":98.33,"status":101,"stdout":""}],"team_id":10},{"d":0,"host":"team9.ructf","n":19,"name":"girav","round":478,"score":"1235.59","services":[{"flags":7,"fp":31.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":207,"sla":85.15,"status":104,"stdout":"No connect\n"},{"flags":59,"fp":440.13,"id":3,"sflags":7,"sla":73.22,"status":104,"stdout":""},{"flags":261,"fp":2287.76,"id":4,"sflags":227,"sla":36.61,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.07,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":686,"sla":55.02,"status":104,"stdout":""},{"flags":0,"fp":22.0,"id":7,"sflags":1,"sla":97.49,"status":101,"stdout":""}],"team_id":9},{"d":0,"host":"team23.ructf","n":20,"name":"MSHP SSL: The Elite Firm","round":478,"score":"754.79","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":89,"sla":89.12,"status":101,"stdout":""},{"flags":3,"fp":2.21,"id":3,"sflags":387,"sla":57.32,"status":104,"stdout":""},{"flags":361,"fp":911.92,"id":4,"sflags":793,"sla":73.22,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":2049,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":22.26,"id":7,"sflags":1,"sla":97.91,"status":101,"stdout":""}],"team_id":23},{"d":0,"host":"team1.ructf","n":21,"name":"Honeypot","round":478,"score":"725.43","services":[{"flags":5,"fp":29.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":98,"sla":82.22,"status":101,"stdout":""},{"flags":127,"fp":818.38,"id":3,"sflags":0,"sla":79.29,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":47,"sla":91.84,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":422,"sla":40.38,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.12,"status":101,"stdout":""}],"team_id":1},{"d":0,"host":"team8.ructf","n":22,"name":"Espacio","round":478,"score":"693.87","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":190,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":90.17,"status":104,"stdout":""},{"flags":205,"fp":992.91,"id":4,"sflags":811,"sla":59.21,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.12,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1512,"sla":73.01,"status":104,"stdout":""},{"flags":0,"fp":22.68,"id":7,"sflags":1,"sla":96.23,"status":101,"stdout":""}],"team_id":8},{"d":0,"host":"team21.ructf","n":23,"name":"Гостевая 1","round":478,"score":"550.24","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":206,"sla":99.58,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":293,"sla":38.08,"status":104,"stdout":""},{"flags":421,"fp":920.35,"id":4,"sflags":1053,"sla":50.42,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":95.19,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1145,"sla":70.5,"status":104,"stdout":""},{"flags":0,"fp":22.85,"id":7,"sflags":1,"sla":97.91,"status":101,"stdout":""}],"team_id":21},{"d":0,"host":"team24.ructf","n":24,"name":"Invisible","round":478,"score":"0.00","services":[{"flags":0,"fp":0.0,"id":1,"sflags":250,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":2,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":4,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":6,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":0.0,"status":104,"stdout":""}],"team_id":24}]},
  {"round":479,"scoreboard":[{"d":0,"host":"team4.ructf","n":1,"name":"Bushwhackers","round":479,"score":"17705.42","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":2580,"fp":15626.03,"id":2,"sflags":43,"sla":98.54,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":14,"sla":67.64,"status":104,"stdout":"connection problem\n"},{"flags":509,"fp":1572.23,"id":4,"sflags":97,"sla":70.56,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":251,"fp":996.29,"id":6,"sflags":84,"sla":100.0,"status":101,"stdout":""},{"flags":19,"fp":150.55,"id":7,"sflags":0,"sla":98.33,"status":101,"stdout":""}],"team_id":4},{"d":0,"host":"team14.ructf","n":2,"name":"Shadow Servants","round":479,"score":"11069.97","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":18,"sla":91.02,"status":101,"stdout":""},{"flags":11,"fp":89.86,"id":3,"sflags":24,"sla":67.64,"status":104,"stdout":""},{"flags":222,"fp":865.57,"id":4,"sflags":152,"sla":78.5,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1703,"fp":10783.33,"id":6,"sflags":331,"sla":94.99,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.75,"status":101,"stdout":""}],"team_id":14},{"d":0,"host":"team12.ructf","n":3,"name":"Lights Out","round":479,"score":"10593.52","services":[{"flags":10,"fp":34.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":437,"fp":6410.46,"id":2,"sflags":1,"sla":98.96,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":80.58,"status":104,"stdout":""},{"flags":116,"fp":1379.16,"id":4,"sflags":93,"sla":78.71,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.45,"status":101,"stdout":""},{"flags":675,"fp":3325.47,"id":6,"sflags":777,"sla":92.69,"status":101,"stdout":""},{"flags":0,"fp":5.79,"id":7,"sflags":1,"sla":95.41,"status":101,"stdout":""}],"team_id":12},{"d":0,"host":"team15.ructf","n":4,"name":"SiBears","round":479,"score":"10322.87","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":146,"sla":97.7,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":74.53,"status":101,"stdout":""},{"flags":1179,"fp":7559.02,"id":4,"sflags":2,"sla":91.86,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.33,"status":101,"stdout":""},{"flags":797,"fp":3299.82,"id":6,"sflags":47,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":8.14,"id":7,"sflags":1,"sla":98.12,"status":101,"stdout":""}],"team_id":15},{"d":0,"host":"team18.ructf","n":5,"name":"Tower Of Hanoi","round":479,"score":"10273.17","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":166.0,"id":2,"sflags":69,"sla":58.25,"status":103,"stdout":"Put failed\n"},{"flags":0,"fp":0.0,"id":3,"sflags":18,"sla":54.49,"status":104,"stdout":"\nhttp http:\/\/electrohub.team18.ructf\/signup\/ status 500\n"},{"flags":937,"fp":4789.29,"id":4,"sflags":31,"sla":82.67,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.24,"status":101,"stdout":""},{"flags":1344,"fp":6271.77,"id":6,"sflags":109,"sla":98.12,"status":101,"stdout":""},{"flags":0,"fp":10.19,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":18},{"d":0,"host":"team11.ructf","n":6,"name":"LC↯BC","round":479,"score":"9116.97","services":[{"flags":1,"fp":25.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":83,"fp":424.68,"id":2,"sflags":153,"sla":55.95,"status":101,"stdout":""},{"flags":56,"fp":169.42,"id":3,"sflags":16,"sla":68.89,"status":101,"stdout":""},{"flags":501,"fp":2246.97,"id":4,"sflags":23,"sla":86.43,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.23,"status":101,"stdout":""},{"flags":1559,"fp":8179.66,"id":6,"sflags":14,"sla":82.67,"status":101,"stdout":""},{"flags":0,"fp":11.97,"id":7,"sflags":1,"sla":94.99,"status":101,"stdout":""}],"team_id":11},{"d":0,"host":"team5.ructf","n":7,"name":"c00kies@venice","round":479,"score":"8178.20","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":67,"fp":264.93,"id":2,"sflags":212,"sla":89.56,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":85.59,"status":101,"stdout":""},{"flags":403,"fp":2027.61,"id":4,"sflags":15,"sla":56.37,"status":104,"stdout":"Response timed out\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":2049,"fp":11381.57,"id":6,"sflags":8,"sla":58.87,"status":101,"stdout":""},{"flags":0,"fp":13.52,"id":7,"sflags":1,"sla":96.03,"status":104,"stdout":"get \/ failed\n"}],"team_id":5},{"d":0,"host":"team7.ructf","n":8,"name":"ENOFLAG","round":479,"score":"8071.60","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":129,"sla":88.52,"status":101,"stdout":""},{"flags":101,"fp":446.44,"id":3,"sflags":0,"sla":98.33,"status":101,"stdout":""},{"flags":167,"fp":595.61,"id":4,"sflags":381,"sla":84.97,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.49,"status":101,"stdout":""},{"flags":1237,"fp":7062.28,"id":6,"sflags":10,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":14.88,"id":7,"sflags":1,"sla":98.12,"status":101,"stdout":""}],"team_id":7},{"d":0,"host":"team6.ructf","n":9,"name":"[censored]","round":479,"score":"7528.31","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":5,"fp":12.97,"id":2,"sflags":77,"sla":93.74,"status":101,"stdout":""},{"flags":166,"fp":851.26,"id":3,"sflags":0,"sla":78.91,"status":101,"stdout":""},{"flags":263,"fp":862.24,"id":4,"sflags":553,"sla":87.27,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1058,"fp":6062.84,"id":6,"sflags":930,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":16.05,"id":7,"sflags":1,"sla":98.12,"status":101,"stdout":""}],"team_id":6},{"d":0,"host":"team16.ructf","n":10,"name":"TeamSpin","round":479,"score":"6882.89","services":[{"flags":13,"fp":37.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1,"fp":0.0,"id":2,"sflags":181,"sla":88.31,"status":101,"stdout":""},{"flags":17,"fp":148.19,"id":3,"sflags":9,"sla":19.42,"status":103,"stdout":"add order item failed\n"},{"flags":239,"fp":2092.37,"id":4,"sflags":191,"sla":77.87,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.16,"status":101,"stdout":""},{"flags":915,"fp":5157.92,"id":6,"sflags":745,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":17.08,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":16},{"d":0,"host":"team13.ructf","n":11,"name":"saarsec","round":479,"score":"6819.40","services":[{"flags":23,"fp":47.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":180,"sla":97.7,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":8,"sla":86.22,"status":101,"stdout":""},{"flags":352,"fp":2843.71,"id":4,"sflags":105,"sla":88.73,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":88.52,"status":101,"stdout":""},{"flags":1361,"fp":4491.76,"id":6,"sflags":103,"sla":93.74,"status":101,"stdout":""},{"flags":0,"fp":17.97,"id":7,"sflags":1,"sla":97.91,"status":101,"stdout":""}],"team_id":13},{"d":0,"host":"team19.ructf","n":12,"name":"WE_0WN_Y0U","round":479,"score":"4663.80","services":[{"flags":0,"fp":24.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":56,"fp":824.32,"id":2,"sflags":233,"sla":99.79,"status":101,"stdout":""},{"flags":88,"fp":530.78,"id":3,"sflags":22,"sla":74.95,"status":101,"stdout":""},{"flags":177,"fp":833.99,"id":4,"sflags":746,"sla":81.21,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.65,"status":101,"stdout":""},{"flags":480,"fp":2696.55,"id":6,"sflags":644,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.12,"status":101,"stdout":""}],"team_id":19},{"d":0,"host":"team20.ructf","n":13,"name":"Destructive Voice","round":479,"score":"4272.61","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":147,"sla":99.16,"status":101,"stdout":""},{"flags":259,"fp":1304.65,"id":3,"sflags":0,"sla":71.82,"status":101,"stdout":""},{"flags":361,"fp":2364.77,"id":4,"sflags":68,"sla":85.59,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.37,"status":101,"stdout":""},{"flags":278,"fp":1304.81,"id":6,"sflags":868,"sla":94.78,"status":104,"stdout":""},{"flags":0,"fp":19.43,"id":7,"sflags":1,"sla":97.7,"status":101,"stdout":""}],"team_id":20},{"d":0,"host":"team2.ructf","n":14,"name":"Переподвысмотрит","round":479,"score":"3686.24","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":140,"fp":1876.69,"id":2,"sflags":221,"sla":93.95,"status":101,"stdout":""},{"flags":16,"fp":150.98,"id":3,"sflags":20,"sla":78.29,"status":104,"stdout":""},{"flags":148,"fp":129.42,"id":4,"sflags":647,"sla":92.69,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.79,"status":101,"stdout":""},{"flags":2296,"fp":1725.84,"id":6,"sflags":922,"sla":92.9,"status":101,"stdout":""},{"flags":0,"fp":20.02,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":2},{"d":0,"host":"team3.ructf","n":15,"name":"BSUIR","round":479,"score":"3119.82","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":269,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":15,"sla":90.4,"status":101,"stdout":""},{"flags":295,"fp":2679.01,"id":4,"sflags":163,"sla":87.68,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.7,"status":101,"stdout":""},{"flags":116,"fp":917.47,"id":6,"sflags":1477,"sla":75.78,"status":103,"stdout":""},{"flags":0,"fp":20.53,"id":7,"sflags":1,"sla":97.7,"status":101,"stdout":""}],"team_id":3},{"d":0,"host":"team17.ructf","n":16,"name":"VoidHack","round":479,"score":"2202.15","services":[{"flags":11,"fp":35.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":262,"sla":99.58,"status":101,"stdout":""},{"flags":66,"fp":429.5,"id":3,"sflags":23,"sla":73.07,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":933,"sla":51.57,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":170,"fp":2341.69,"id":6,"sflags":225,"sla":77.24,"status":104,"stdout":""},{"flags":0,"fp":20.98,"id":7,"sflags":1,"sla":97.7,"status":101,"stdout":""}],"team_id":17},{"d":0,"host":"team22.ructf","n":17,"name":"Гостевая 2","round":479,"score":"1637.64","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":164,"sla":98.33,"status":103,"stdout":"Bad answer\n"},{"flags":0,"fp":0.0,"id":3,"sflags":113,"sla":26.51,"status":103,"stdout":"add order item failed\n"},{"flags":174,"fp":2029.0,"id":4,"sflags":207,"sla":77.04,"status":103,"stdout":"Couldn't find flag!\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.96,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1856,"sla":94.78,"status":101,"stdout":""},{"flags":0,"fp":21.37,"id":7,"sflags":1,"sla":97.49,"status":101,"stdout":""}],"team_id":22},{"d":0,"host":"team10.ructf","n":18,"name":"keva","round":479,"score":"1610.90","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":137,"sla":73.7,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":73.49,"status":101,"stdout":""},{"flags":102,"fp":1651.75,"id":4,"sflags":54,"sla":91.44,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.12,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1319,"sla":72.23,"status":104,"stdout":""},{"flags":0,"fp":21.71,"id":7,"sflags":1,"sla":98.33,"status":101,"stdout":""}],"team_id":10},{"d":0,"host":"team9.ructf","n":19,"name":"girav","round":479,"score":"1233.17","services":[{"flags":7,"fp":31.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":207,"sla":84.97,"status":104,"stdout":"No connect\n"},{"flags":59,"fp":440.13,"id":3,"sflags":7,"sla":73.07,"status":104,"stdout":""},{"flags":261,"fp":2287.76,"id":4,"sflags":227,"sla":36.53,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.08,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":686,"sla":54.91,"status":104,"stdout":""},{"flags":0,"fp":22.0,"id":7,"sflags":1,"sla":97.49,"status":101,"stdout":""}],"team_id":9},{"d":0,"host":"team23.ructf","n":20,"name":"MSHP SSL: The Elite Firm","round":479,"score":"753.40","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":89,"sla":89.14,"status":101,"stdout":""},{"flags":3,"fp":2.21,"id":3,"sflags":387,"sla":57.41,"status":101,"stdout":""},{"flags":361,"fp":911.92,"id":4,"sflags":793,"sla":73.07,"status":104,"stdout":"Response timed out\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":2055,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":22.26,"id":7,"sflags":1,"sla":97.91,"status":101,"stdout":""}],"team_id":23},{"d":0,"host":"team1.ructf","n":21,"name":"Honeypot","round":479,"score":"724.08","services":[{"flags":5,"fp":29.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":98,"sla":82.25,"status":101,"stdout":""},{"flags":127,"fp":818.38,"id":3,"sflags":0,"sla":79.12,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":47,"sla":91.86,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":422,"sla":40.29,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":98.12,"status":101,"stdout":""}],"team_id":1},{"d":0,"host":"team8.ructf","n":22,"name":"Espacio","round":479,"score":"691.59","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":191,"sla":99.16,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":90.19,"status":101,"stdout":""},{"flags":205,"fp":991.12,"id":4,"sflags":812,"sla":59.08,"status":103,"stdout":"Couldn't find flag!\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.12,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1512,"sla":72.86,"status":104,"stdout":""},{"flags":0,"fp":22.68,"id":7,"sflags":1,"sla":96.24,"status":101,"stdout":""}],"team_id":8},{"d":0,"host":"team21.ructf","n":23,"name":"Гостевая 1","round":479,"score":"549.28","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":206,"sla":99.58,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":293,"sla":38.0,"status":104,"stdout":""},{"flags":421,"fp":920.35,"id":4,"sflags":1053,"sla":50.31,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":95.2,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1145,"sla":70.35,"status":104,"stdout":""},{"flags":0,"fp":22.85,"id":7,"sflags":1,"sla":97.91,"status":101,"stdout":""}],"team_id":21},{"d":0,"host":"team24.ructf","n":24,"name":"Invisible","round":479,"score":"0.00","services":[{"flags":0,"fp":0.0,"id":1,"sflags":250,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":2,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":4,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":6,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":0.0,"status":104,"stdout":""}],"team_id":24}]},
  {"round":480,"scoreboard":[{"d":0,"host":"team4.ructf","n":1,"name":"Bushwhackers","round":480,"score":"17832.91","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":2587,"fp":15656.25,"id":2,"sflags":43,"sla":98.54,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":14,"sla":67.5,"status":104,"stdout":"connection problem\n"},{"flags":509,"fp":1572.23,"id":4,"sflags":97,"sla":70.63,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":251,"fp":996.29,"id":6,"sflags":84,"sla":100.0,"status":101,"stdout":""},{"flags":34,"fp":248.46,"id":7,"sflags":0,"sla":98.33,"status":101,"stdout":""}],"team_id":4},{"d":0,"host":"team14.ructf","n":2,"name":"Shadow Servants","round":480,"score":"11057.78","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":18,"sla":90.83,"status":104,"stdout":"No connect\n"},{"flags":11,"fp":89.86,"id":3,"sflags":24,"sla":67.5,"status":104,"stdout":""},{"flags":222,"fp":865.57,"id":4,"sflags":152,"sla":78.33,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1705,"fp":10792.67,"id":6,"sflags":331,"sla":95.0,"status":101,"stdout":""},{"flags":0,"fp":3.1,"id":7,"sflags":1,"sla":98.75,"status":101,"stdout":""}],"team_id":14},{"d":0,"host":"team12.ructf","n":3,"name":"Lights Out","round":480,"score":"10640.27","services":[{"flags":10,"fp":34.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":441,"fp":6445.55,"id":2,"sflags":1,"sla":98.96,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":80.42,"status":104,"stdout":""},{"flags":116,"fp":1379.16,"id":4,"sflags":93,"sla":78.54,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.46,"status":101,"stdout":""},{"flags":679,"fp":3340.22,"id":6,"sflags":777,"sla":92.71,"status":101,"stdout":""},{"flags":0,"fp":5.79,"id":7,"sflags":1,"sla":95.42,"status":101,"stdout":""}],"team_id":12},{"d":0,"host":"team15.ructf","n":4,"name":"SiBears","round":480,"score":"10316.99","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":147,"sla":97.71,"status":101,"stdout":""},{"flags":1,"fp":25.17,"id":3,"sflags":0,"sla":74.38,"status":104,"stdout":""},{"flags":1179,"fp":7559.02,"id":4,"sflags":2,"sla":91.88,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.33,"status":101,"stdout":""},{"flags":797,"fp":3299.82,"id":6,"sflags":47,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":7,"sflags":2,"sla":98.13,"status":101,"stdout":""}],"team_id":15},{"d":0,"host":"team18.ructf","n":5,"name":"Tower Of Hanoi","round":480,"score":"10264.91","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":64,"fp":166.0,"id":2,"sflags":69,"sla":58.13,"status":103,"stdout":"Put failed\n"},{"flags":0,"fp":0.0,"id":3,"sflags":18,"sla":54.38,"status":104,"stdout":"\nhttp http:\/\/electrohub.team18.ructf\/signup\/ status 500\n"},{"flags":937,"fp":4789.29,"id":4,"sflags":31,"sla":82.71,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":96.25,"status":101,"stdout":""},{"flags":1344,"fp":6271.77,"id":6,"sflags":109,"sla":98.13,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":7,"sflags":2,"sla":98.54,"status":101,"stdout":""}],"team_id":18},{"d":0,"host":"team11.ructf","n":6,"name":"LC↯BC","round":480,"score":"9119.06","services":[{"flags":1,"fp":25.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":85,"fp":419.69,"id":2,"sflags":154,"sla":55.83,"status":102,"stdout":"Flag not found\n"},{"flags":56,"fp":169.42,"id":3,"sflags":16,"sla":68.96,"status":101,"stdout":""},{"flags":501,"fp":2246.97,"id":4,"sflags":23,"sla":86.46,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.25,"status":101,"stdout":""},{"flags":1560,"fp":8181.69,"id":6,"sflags":14,"sla":82.71,"status":101,"stdout":""},{"flags":0,"fp":11.97,"id":7,"sflags":1,"sla":95.0,"status":101,"stdout":""}],"team_id":11},{"d":0,"host":"team5.ructf","n":7,"name":"c00kies@venice","round":480,"score":"8187.58","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":70,"fp":297.66,"id":2,"sflags":212,"sla":89.58,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":85.63,"status":101,"stdout":""},{"flags":403,"fp":2027.61,"id":4,"sflags":15,"sla":56.46,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.38,"status":101,"stdout":""},{"flags":2050,"fp":11385.27,"id":6,"sflags":8,"sla":58.75,"status":104,"stdout":""},{"flags":0,"fp":3.05,"id":7,"sflags":2,"sla":96.04,"status":101,"stdout":""}],"team_id":5},{"d":0,"host":"team7.ructf","n":8,"name":"ENOFLAG","round":480,"score":"8078.05","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":130,"sla":88.54,"status":101,"stdout":""},{"flags":101,"fp":446.44,"id":3,"sflags":0,"sla":98.33,"status":101,"stdout":""},{"flags":167,"fp":595.61,"id":4,"sflags":381,"sla":85.0,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.5,"status":101,"stdout":""},{"flags":1239,"fp":7068.51,"id":6,"sflags":10,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":14.88,"id":7,"sflags":1,"sla":98.13,"status":101,"stdout":""}],"team_id":7},{"d":0,"host":"team6.ructf","n":9,"name":"[censored]","round":480,"score":"7525.85","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":5,"fp":12.97,"id":2,"sflags":77,"sla":93.75,"status":101,"stdout":""},{"flags":166,"fp":851.26,"id":3,"sflags":0,"sla":78.96,"status":101,"stdout":""},{"flags":263,"fp":862.24,"id":4,"sflags":553,"sla":87.29,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1060,"fp":6067.5,"id":6,"sflags":930,"sla":99.17,"status":101,"stdout":""},{"flags":0,"fp":8.11,"id":7,"sflags":2,"sla":98.13,"status":101,"stdout":""}],"team_id":6},{"d":0,"host":"team16.ructf","n":10,"name":"TeamSpin","round":480,"score":"6905.91","services":[{"flags":13,"fp":37.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":1,"fp":0.0,"id":2,"sflags":181,"sla":88.33,"status":101,"stdout":""},{"flags":17,"fp":148.19,"id":3,"sflags":9,"sla":19.38,"status":103,"stdout":"add order item failed\n"},{"flags":239,"fp":2092.37,"id":4,"sflags":191,"sla":77.92,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.17,"status":101,"stdout":""},{"flags":926,"fp":5180.05,"id":6,"sflags":746,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":17.08,"id":7,"sflags":1,"sla":98.54,"status":101,"stdout":""}],"team_id":16},{"d":0,"host":"team13.ructf","n":11,"name":"saarsec","round":480,"score":"6818.23","services":[{"flags":23,"fp":47.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":182,"sla":97.71,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":8,"sla":86.25,"status":101,"stdout":""},{"flags":352,"fp":2843.71,"id":4,"sflags":105,"sla":88.75,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":88.54,"status":101,"stdout":""},{"flags":1364,"fp":4495.46,"id":6,"sflags":104,"sla":93.75,"status":101,"stdout":""},{"flags":0,"fp":11.95,"id":7,"sflags":2,"sla":97.92,"status":101,"stdout":""}],"team_id":13},{"d":0,"host":"team19.ructf","n":12,"name":"WE_0WN_Y0U","round":480,"score":"4653.35","services":[{"flags":0,"fp":24.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":57,"fp":821.25,"id":2,"sflags":235,"sla":99.79,"status":101,"stdout":""},{"flags":88,"fp":530.78,"id":3,"sflags":22,"sla":74.79,"status":104,"stdout":""},{"flags":177,"fp":833.99,"id":4,"sflags":746,"sla":81.04,"status":103,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":91.67,"status":101,"stdout":""},{"flags":480,"fp":2696.55,"id":6,"sflags":644,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":18.75,"id":7,"sflags":1,"sla":98.13,"status":101,"stdout":""}],"team_id":19},{"d":0,"host":"team20.ructf","n":13,"name":"Destructive Voice","round":480,"score":"4278.90","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":147,"sla":99.17,"status":101,"stdout":""},{"flags":259,"fp":1304.65,"id":3,"sflags":0,"sla":71.67,"status":104,"stdout":""},{"flags":361,"fp":2364.77,"id":4,"sflags":68,"sla":85.63,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.38,"status":101,"stdout":""},{"flags":280,"fp":1315.54,"id":6,"sflags":868,"sla":94.58,"status":104,"stdout":""},{"flags":0,"fp":19.43,"id":7,"sflags":1,"sla":97.5,"status":104,"stdout":"get \/ failed\n"}],"team_id":20},{"d":0,"host":"team2.ructf","n":14,"name":"Переподвысмотрит","round":480,"score":"3673.66","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":140,"fp":1866.86,"id":2,"sflags":223,"sla":93.96,"status":101,"stdout":""},{"flags":16,"fp":150.98,"id":3,"sflags":20,"sla":78.33,"status":101,"stdout":""},{"flags":148,"fp":129.42,"id":4,"sflags":647,"sla":92.71,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":99.79,"status":101,"stdout":""},{"flags":2296,"fp":1725.84,"id":6,"sflags":922,"sla":92.92,"status":101,"stdout":""},{"flags":0,"fp":16.04,"id":7,"sflags":2,"sla":98.54,"status":101,"stdout":""}],"team_id":2},{"d":0,"host":"team3.ructf","n":15,"name":"BSUIR","round":480,"score":"3136.98","services":[{"flags":8,"fp":32.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":270,"sla":99.79,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":15,"sla":90.42,"status":101,"stdout":""},{"flags":295,"fp":2679.01,"id":4,"sflags":163,"sla":87.71,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.71,"status":101,"stdout":""},{"flags":118,"fp":941.16,"id":6,"sflags":1477,"sla":75.63,"status":103,"stdout":""},{"flags":0,"fp":20.53,"id":7,"sflags":1,"sla":97.71,"status":101,"stdout":""}],"team_id":3},{"d":0,"host":"team17.ructf","n":16,"name":"VoidHack","round":480,"score":"2195.67","services":[{"flags":11,"fp":35.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":264,"sla":99.58,"status":101,"stdout":""},{"flags":66,"fp":429.5,"id":3,"sflags":23,"sla":73.13,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":933,"sla":51.46,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":170,"fp":2341.69,"id":6,"sflags":225,"sla":77.08,"status":104,"stdout":""},{"flags":0,"fp":17.96,"id":7,"sflags":2,"sla":97.71,"status":101,"stdout":""}],"team_id":17},{"d":0,"host":"team22.ructf","n":17,"name":"Гостевая 2","round":480,"score":"1636.04","services":[{"flags":6,"fp":30.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":164,"sla":98.13,"status":104,"stdout":"No connect\n"},{"flags":0,"fp":0.0,"id":3,"sflags":113,"sla":26.46,"status":103,"stdout":"add order item failed\n"},{"flags":174,"fp":2029.0,"id":4,"sflags":207,"sla":77.08,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.96,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1865,"sla":94.79,"status":101,"stdout":""},{"flags":0,"fp":18.74,"id":7,"sflags":2,"sla":97.5,"status":101,"stdout":""}],"team_id":22},{"d":0,"host":"team10.ructf","n":18,"name":"keva","round":480,"score":"1608.91","services":[{"flags":14,"fp":38.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":137,"sla":73.54,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":73.33,"status":104,"stdout":""},{"flags":102,"fp":1651.75,"id":4,"sflags":54,"sla":91.46,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.13,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1319,"sla":72.08,"status":104,"stdout":""},{"flags":0,"fp":19.42,"id":7,"sflags":2,"sla":98.33,"status":101,"stdout":""}],"team_id":10},{"d":0,"host":"team9.ructf","n":19,"name":"girav","round":480,"score":"1230.76","services":[{"flags":7,"fp":31.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":207,"sla":84.79,"status":104,"stdout":"No connect\n"},{"flags":59,"fp":440.13,"id":3,"sflags":7,"sla":72.92,"status":104,"stdout":""},{"flags":261,"fp":2287.76,"id":4,"sflags":227,"sla":36.46,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":97.08,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":686,"sla":54.79,"status":104,"stdout":""},{"flags":0,"fp":22.0,"id":7,"sflags":1,"sla":97.5,"status":101,"stdout":""}],"team_id":9},{"d":0,"host":"team23.ructf","n":20,"name":"MSHP SSL: The Elite Firm","round":480,"score":"752.21","services":[{"flags":16,"fp":40.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":89,"sla":89.17,"status":101,"stdout":""},{"flags":3,"fp":2.21,"id":3,"sflags":387,"sla":57.29,"status":104,"stdout":"connection problem\n"},{"flags":361,"fp":911.92,"id":4,"sflags":793,"sla":73.13,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":2074,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":20.52,"id":7,"sflags":2,"sla":97.92,"status":101,"stdout":""}],"team_id":23},{"d":0,"host":"team1.ructf","n":21,"name":"Honeypot","round":480,"score":"721.24","services":[{"flags":5,"fp":29.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":98,"sla":82.29,"status":101,"stdout":""},{"flags":127,"fp":818.38,"id":3,"sflags":0,"sla":78.96,"status":104,"stdout":""},{"flags":0,"fp":0.0,"id":4,"sflags":47,"sla":91.88,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":422,"sla":40.21,"status":104,"stdout":""},{"flags":0,"fp":22.49,"id":7,"sflags":1,"sla":98.13,"status":101,"stdout":""}],"team_id":1},{"d":0,"host":"team8.ructf","n":22,"name":"Espacio","round":480,"score":"691.18","services":[{"flags":15,"fp":39.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":193,"sla":99.17,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":90.21,"status":101,"stdout":""},{"flags":205,"fp":991.12,"id":4,"sflags":812,"sla":59.17,"status":101,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":98.13,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1512,"sla":72.71,"status":104,"stdout":""},{"flags":0,"fp":21.36,"id":7,"sflags":2,"sla":96.25,"status":101,"stdout":""}],"team_id":8},{"d":0,"host":"team21.ructf","n":23,"name":"Гостевая 1","round":480,"score":"547.19","services":[{"flags":17,"fp":41.0,"id":1,"sflags":0,"sla":100.0,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":2,"sflags":209,"sla":99.58,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":3,"sflags":294,"sla":37.92,"status":104,"stdout":""},{"flags":421,"fp":920.35,"id":4,"sflags":1053,"sla":50.21,"status":104,"stdout":"Bad command address\n"},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":95.21,"status":101,"stdout":""},{"flags":0,"fp":0.0,"id":6,"sflags":1145,"sla":70.21,"status":104,"stdout":""},{"flags":0,"fp":21.7,"id":7,"sflags":2,"sla":97.92,"status":101,"stdout":""}],"team_id":21},{"d":0,"host":"team24.ructf","n":24,"name":"Invisible","round":480,"score":"0.00","services":[{"flags":0,"fp":0.0,"id":1,"sflags":250,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":2,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":3,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":4,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":5,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":6,"sflags":0,"sla":0.0,"status":104,"stdout":""},{"flags":0,"fp":24.0,"id":7,"sflags":0,"sla":0.0,"status":104,"stdout":""}],"team_id":24}]}
]

start_time = 1492355640.0
flags = [
  {
    "ts": 1492355645.59566,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.60073,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.60391,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.60836,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.89361,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355646.02667,
    "victim_id": 7,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355646.03474,
    "victim_id": 2,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355646.859,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355650.62703,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355651.34727,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355653.54947,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355655.65216,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355656.14673,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355656.21752,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355656.34694,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355660.1727,
    "victim_id": 22,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355675.24517,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355675.41654,
    "victim_id": 5,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355676.50444,
    "victim_id": 7,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355676.53112,
    "victim_id": 7,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355677.46321,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 4
  },
  {
    "ts": 1492355679.60602,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355683.11875,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355683.90285,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355689.99004,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355691.79022,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355704.32467,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355704.56383,
    "victim_id": 3,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355704.56971,
    "victim_id": 7,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355704.80662,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355705.76905,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355705.77355,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355705.77791,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355705.78124,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355706.60954,
    "victim_id": 2,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355706.61558,
    "victim_id": 21,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355709.45599,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355711.08812,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355716.25365,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355718.16189,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355718.16813,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355720.75153,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355722.11672,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355722.12275,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355725.86249,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355727.4079,
    "victim_id": 20,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355728.80866,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355739.28259,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355744.94147,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355747.63438,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355749.16248,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355749.9134,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355750.02098,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.17814,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.25403,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.36779,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.42307,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355755.99018,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355760.10274,
    "victim_id": 5,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355760.85058,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355763.79513,
    "victim_id": 15,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355765.41319,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355766.03151,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355766.03415,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355766.17479,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355766.78347,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355767.37046,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355767.83827,
    "victim_id": 6,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355769.59161,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355771.07041,
    "victim_id": 9,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07503,
    "victim_id": 7,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07688,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07837,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07885,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08284,
    "victim_id": 23,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08524,
    "victim_id": 21,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08838,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08954,
    "victim_id": 12,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09201,
    "victim_id": 6,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09392,
    "victim_id": 15,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09963,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09985,
    "victim_id": 18,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.10581,
    "victim_id": 16,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355772.03081,
    "victim_id": 22,
    "attacker_id": 15,
    "service_id": 6
  },
  {
    "ts": 1492355773.11681,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355774.92285,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355774.92676,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355774.93156,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355776.15438,
    "victim_id": 10,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.15689,
    "victim_id": 5,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.15803,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.16459,
    "victim_id": 20,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.16846,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355779.26164,
    "victim_id": 22,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355786.20308,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355794.89313,
    "victim_id": 19,
    "attacker_id": 20,
    "service_id": 4
  },
  {
    "ts": 1492355794.92968,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355794.93325,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355794.93708,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355794.94436,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355796.29298,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355799.92643,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355801.02756,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355801.03606,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355801.04618,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355802.50487,
    "victim_id": 22,
    "attacker_id": 19,
    "service_id": 6
  },
  {
    "ts": 1492355803.30258,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355803.74883,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 4
  },
  {
    "ts": 1492355805.70755,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355807.34981,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355807.40339,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355807.44497,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355807.49139,
    "victim_id": 23,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355811.24205,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.4736,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.70733,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.8151,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.89125,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355813.60179,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355815.04155,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355815.04235,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355815.42663,
    "victim_id": 4,
    "attacker_id": 18,
    "service_id": 4
  },
  {
    "ts": 1492355820.18086,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355820.49816,
    "victim_id": 23,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355824.77645,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355825.71299,
    "victim_id": 19,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355825.73541,
    "victim_id": 14,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355826.48061,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.49416,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.52334,
    "victim_id": 23,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.52696,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.53449,
    "victim_id": 20,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355831.56472,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355832.78192,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355833.87522,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355836.10745,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355839.11471,
    "victim_id": 7,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355839.61943,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355843.35665,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355843.36288,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355846.00021,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355848.13576,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355848.19866,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355849.38818,
    "victim_id": 21,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355850.65232,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355863.40543,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355863.41092,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355865.54504,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355866.75695,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355870.04874,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355880.80906,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355882.28282,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355882.38308,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355884.37524,
    "victim_id": 7,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355884.56109,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355886.09971,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355886.88952,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.89285,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.89737,
    "victim_id": 20,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.90071,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.90435,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355887.27093,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355888.45383,
    "victim_id": 19,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355889.91699,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355894.74212,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355894.74731,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355896.17037,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355897.26624,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355897.49703,
    "victim_id": 22,
    "attacker_id": 15,
    "service_id": 4
  },
  {
    "ts": 1492355898.57668,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355899.67188,
    "victim_id": 4,
    "attacker_id": 15,
    "service_id": 4
  },
  {
    "ts": 1492355900.63199,
    "victim_id": 22,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355900.63745,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355900.84088,
    "victim_id": 3,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355906.10504,
    "victim_id": 8,
    "attacker_id": 20,
    "service_id": 4
  },
  {
    "ts": 1492355916.13084,
    "victim_id": 5,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355916.77843,
    "victim_id": 8,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355923.47292,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355926.38375,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355930.0527,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355935.16796,
    "victim_id": 22,
    "attacker_id": 19,
    "service_id": 6
  },
  {
    "ts": 1492355937.08938,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355944.81885,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355945.10977,
    "victim_id": 21,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355946.45984,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355947.13996,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.14278,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.14426,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.14846,
    "victim_id": 21,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.1499,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.1572,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.16349,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.16777,
    "victim_id": 2,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355950.36374,
    "victim_id": 19,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355952.19206,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19248,
    "victim_id": 6,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19462,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19732,
    "victim_id": 14,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19918,
    "victim_id": 18,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.20012,
    "victim_id": 23,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.20316,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.20538,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21118,
    "victim_id": 21,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21149,
    "victim_id": 15,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21199,
    "victim_id": 10,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21925,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.2204,
    "victim_id": 1,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355953.14309,
    "victim_id": 15,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355953.50286,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355954.98811,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355954.99432,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355955.32994,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355955.33507,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355957.256,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355957.26105,
    "victim_id": 5,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355957.82813,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355958.17973,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355959.59261,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355961.334,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355962.3008,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355965.24907,
    "victim_id": 21,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355967.32028,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355970.87162,
    "victim_id": 8,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355971.06446,
    "victim_id": 21,
    "attacker_id": 15,
    "service_id": 3
  },
  {
    "ts": 1492355971.16376,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355975.491,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.50017,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.50834,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.51665,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.52421,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.53255,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.53942,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.54689,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.55546,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.56232,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.64781,
    "victim_id": 13,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355975.65142,
    "victim_id": 7,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355978.52762,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355978.53716,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355981.76577,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355981.84075,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355982.28565,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355990.06411,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355996.70448,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  }
]


ROUND_TIME = 2 * 60*1000
service_names = ["pool", "capter", "electrohub", "fooddispenser", "redbutton", "settings", "stargate"]
team_names = ["Honeypot", "Переподвысмотрит", "BSUIR", "Bushwhackers", "c00kies@venice", "[censored]", "ENOFLAG",
              "Espacio", "girav", "keva", "LC↯BC", "Lights Out", "saarsec", "Shadow Servants", "SiBears",
              "TeamSpin", "VoidHack", "Tower Of Hanoi", "WE_0WN_Y0U", "Destructive Voice", "Гостевая 1",
              "Гостевая 2", "MSHP SSL: The Elite Firm", "Invisible"]
flags_i = 0
stat_i = 0



def team_(x): return x + 1
def service_(x): return x + 1

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
                "score": str(scores[team_(t)]) + ".12",
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
    global connected, start, flags_i, stat_i
    connected.add(websocket)
    start = gtime()
    flags_i = 0
    stat_i = 0
    await create_state()
    await create_start()
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
                        default=24)
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

async def create_start():
    event = {
        "type": "start",
    }
    json_str = json.dumps(event)
    await write_to_websocket(json_str)

async def create_attacks():
    global flags, start, flags_i
    step = 10  # ms
    while True:
        while flags_i < len(flags) and flags[flags_i]["ts"] * 1000 - start_time * 1000 < (gtime() - start) / 2:
            event = {
                "type": "attack",
                "value": {
                    "service_id": flags[flags_i]["service_id"],
                    "attacker_id": team_(flags[flags_i]["attacker_id"]),
                    "victim_id": team_(flags[flags_i]["victim_id"])
                }
            }
            json_str = json.dumps(event)
            await write_to_websocket(json_str)
            flags_i += 1
        await asyncio.sleep(step/1000)

async def create_states():
    global stat_i, stat
    step = 10  # ms
    while True:
        if gtime() - start > (stat_i + 1) * ROUND_TIME:
            stat_i += 1
            if stat_i < len(stat):
                await create_state()
        await asyncio.sleep(step / 1000)

async def create_state():
    global stat_i, stat
    container = {
        "type": "state",
        "value": stat[stat_i]
    }
    json_str = json.dumps(container)
    await write_to_websocket(json_str)


if __name__ == '__main__':
    args = parse_args()
    start = gtime()
    events = []
    scores = {team_(i): 0 for i in range(args.teams)}

    thread = threading.Thread(target=websocket_server_run)
    thread.start()

    run(host='0.0.0.0', port=8000, debug=True, reloader=False)
