from backend.start import get_connection, start_db
from backend.query import *
import pandas as pd
from datetime import timedelta

port = start_db()
conn = get_connection(port)
cur = conn.cursor()

def get_average_deaths() -> int:
    cur.execute(average_deaths_query())
    results = cur.fetchall()
    return int(results[0][0])

def get_top_message_senders(limit: int = 10) -> pd.DataFrame:
    cur.execute(top_message_senders_query(limit))
    results = cur.fetchall()
    return results

def get_total_players() -> int:
    cur.execute(total_players_query())
    results = cur.fetchall()
    return results[0][0]

def get_total_message() -> int:
    cur.execute(total_message_query())
    results = cur.fetchall()
    return results[0][0]

def get_uptime():
    cur.execute(server_status_query())
    rows = cur.fetchall()

    total_uptime = timedelta()

    for i in range(len(rows) - 1):
        ping, current_time = rows[i]
        _, next_time = rows[i + 1]   #take next row

        #if server was up during this interval
        if ping >= 0:       #ping = -1 -> down time
            total_uptime += (next_time - current_time)

    jours = total_uptime.days
    heures = total_uptime.seconds // 3600
    minutes = (total_uptime.seconds % 3600) // 60

    return f"{jours} days, {heures} hours, {minutes} minutes"

def get_total_deaths() -> int:
    cur.execute(total_deaths_query())
    results = cur.fetchall()
    return results[0][0]

def get_deaths_by_type() -> tuple:
    """return tuple with (player, mob, environment)"""
    cur.execute(deaths_by_type_query())
    df = pd.DataFrame(cur.fetchall(), columns=["killer"])

    player, mob, environment = 0, 0, 0

    for killer in df["killer"]:
        killer = str(killer).strip()      #-> str

        if killer == "":
            environment += 1

        elif killer.endswith("(mob)"):    #if "(mob)" at the end
            mob += 1

        else:
            player += 1

    return player, mob, environment

def get_death_distribution(limit:int=7) -> pd.DataFrame:
    cur.execute(death_distribution_query(limit))
    df = pd.DataFrame(cur.fetchall(), columns=["type", "nombre"])
    return df

def get_top_chatters(limit:int=10) -> pd.DataFrame:
    cur.execute(top_chatters_query(limit))
    df = pd.DataFrame(cur.fetchall(), columns=["joueur","messages"])
    return df

def get_playercount_over_time() -> pd.DataFrame:
    cur.execute(playercount_over_time_query())
    df = pd.DataFrame(cur.fetchall(), columns=["nombre de joueurs","temps"])
    return df

def get_ping_over_time() -> pd.DataFrame:
    cur.execute(ping_over_time_query())
    df = pd.DataFrame(cur.fetchall(), columns=["ping","temps"])
    return df

def get_message_over_time() -> pd.DataFrame:
    cur.execute(messages_over_time_query())
    df = pd.DataFrame(cur.fetchall(), columns=["message","temps"])
    return df

def get_info_player(player: str) -> pd.DataFrame:
    cur.execute(player_info_query(player))
    df = pd.DataFrame(cur.fetchall(), columns=["player","kill","death","messages","total session","total playtime (in sec)"])
    return df

def get_list_player_query() -> list:
    cur.execute(list_player_query())
    results = [t[0] for t in cur.fetchall()]
    return results

def get_last_chat_lines():
    cur.execute(last_chat_lines_query())
    df = pd.DataFrame(cur.fetchall(), columns=["player", "message", "timestamp"])
    return df
#print(get_last_chat_lines())



def proof_update(table: str, primary_key: int, **columns) -> None:
    if proof_update_query(table, primary_key, **columns) is None:
        print("erreur")
    else:
        cur.execute(proof_update_query(table, primary_key, **columns))
        conn.commit()

def proof_insert(table: str, **columns) -> None:
    if proof_insert_query(table, **columns) is None:
        print("erreur")
    else:
        cur.execute(proof_update_query(table,  **columns))
        conn.commit()

def proof_delete(table: str, primary_key: int) -> None:
    cur.execute(proof_delete_query(table, primary_key))
    conn.commit()