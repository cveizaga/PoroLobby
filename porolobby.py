#! python3
import random
from lcu_driver import Connector

#list of available bots
bot_list = [12, 32, 1, 22, 53, 63, 51, 69, 31, 122, 119, 36, 81, 9, 3, 86, 104,
            24, 30, 10, 96, 89, 236, 99, 54, 11, 21, 62, 25, 75, 76, 33, 58, 13,
            98, 102, 15, 16, 44, 18, 48, 77, 45, 8, 19, 115, 26, 143]

connector = Connector()

# Creates 5v5 Practice Tool
async def createLobby(connection):
    data = {
        "customGameLobby": {
            "configuration": {
                "gameMode": "PRACTICETOOL",
                "gameMutator": "",
                "gameServerRegion": "",
                "mapId": 11,
                "mutators": {
                    "id": 1
                },
                "spectatorPolicy": "AllAllowed",
                "teamSize": 5,
            },
            "lobbyName": "League of Poro's Practice Tool",
            "lobbyPassword": ""
        },
        "isCustom": True,
    }
    # make the request to switch the lobby
    lobby = await connection.request('post', '/lol-lobby/v2/lobby', data=data)

    # if HTTP status code is 200 the lobby was created successfully
    if lobby.status == 200:
        print('The lobby was created correctly')
    else:
        print('Whops, Yasuo died again.')


# Contacts LCU API to add bots
async def executeAddBot(connection, data):
    res = await connection.request('post', '/lol-lobby/v1/lobby/custom/bots', data=data)
    if res.status == 204:
        print('Bot added')
    else:
        print('Whops, Yasuo died again.')

# Selects which bots to add and adds them to an existing lobby
async def addBots(connection):
    ids_Player_Team = random.choices(bot_list, k=4)
    ids_Enemy_Team = random.choices(bot_list, k=5)
    # add bots to the player's team
    for id in ids_Player_Team:
        data = {
            "botDifficulty": "EASY",
            "championId": id,
            "teamId": "100"
        }
        await executeAddBot(connection, data)

    # add bots to the opposite team
    for id in ids_Enemy_Team:
        data = {
            "botDifficulty": "MEDIUM",
            "championId": id,
            "teamId": "200"
        }
        await executeAddBot(connection, data)


# fired when LCU API is ready to be used
@connector.ready
async def connect(connection):
    print('LCU API is ready to be used.')

    # check if the user is already logged into his account
    summoner = await connection.request('get', '/lol-summoner/v1/current-summoner')
    if summoner.status != 200:
        print('Please login into your account.')
    else:
        print('Switching the lobby type.')
        await createLobby(connection)
        await addBots(connection)


# fired when League Client is closed (or disconnected from websocket)
@connector.close
async def disconnect(_):
    print('The client have been closed!')

# starts the connector
connector.start()
