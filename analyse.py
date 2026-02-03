from start import get_connection, start_db
from query import *
from datetime import datetime
import pandas as pd  #c'est dans tout les tuto ce 'pd'

port = start_db()
conn = get_connection(port)
cur = conn.cursor()

def delta_temps(timestamp1: str, timestamp2: str) -> float:
    """retourne la durée entre les deux timestamps en secondes:float"""
    format_timestamp = "%Y-%m-%d %H:%M:%S.%f"      #le nom "format" est déjà pris par un autre truc
    delta = datetime.strptime(timestamp2, format_timestamp) - datetime.strptime(timestamp1, format_timestamp)
    return delta.total_seconds()

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

def get_event_duration():
    cur.execute(event_duration_query())
    t_start, t_end = cur.fetchall()[0]
    delta = t_end - t_start

    jours = delta.days
    heures = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60

    return f"{jours} jour, {heures} heure, {minutes} minute"

def get_total_deaths() -> int:
    cur.execute(total_deaths_query())
    results = cur.fetchall()
    return results[0][0]

def get_playercount_over_time() -> pd.DataFrame:
    cur.execute(playercount_over_time_query())
    df = pd.DataFrame(cur.fetchall(), columns=["nombre de joueurs"])
    df.index.name = "temps"
    return df

def server_ping_over_time_query() -> pd.DataFrame:
    cur.execute(playercount_over_time_query())
    df = pd.DataFrame(cur.fetchall(), columns=["ping"])
    df.index.name = "time"
    return df

def get_message_over_time() -> pd.DataFrame:
    cur.execute(messages_over_time_query())
    df = pd.DataFrame(cur.fetchall(), columns=["message","temps"])
    return df

def get_info_player(player: str) -> pd.DataFrame:
    cur.execute(player_info_query(player))
    df = pd.DataFrame(cur.fetchall(), columns=["player","kill","death","messages","total session","total playtime (in sec)"])
    df.index.name = "id"
    return df

def get_list_player_query() -> list:
    cur.execute(list_player_query())
    results = [t[0] for t in cur.fetchall()]
    return results

















def proof_update(table: str, primary_key: int, **columns) -> None:
    if proof_update_query(table, primary_key, **columns) is None:
        print("erreur")
    else:
        cur.execute(proof_update_query(table, primary_key, **columns))
        conn.commit()    #pour apliquer le query sur la db
        cur.close()
        conn.close()

def proof_insert(table: str, **columns) -> None:
    if proof_insert_query(table, **columns) is None:
        print("erreur")
    else:
        cur.execute(proof_update_query(table,  **columns))
        conn.commit()
        cur.close()
        conn.close()

def proof_delete(table: str, primary_key: int) -> None:
    cur.execute(proof_delete_query(table, primary_key))
    conn.commit()
    cur.close()
    conn.close()