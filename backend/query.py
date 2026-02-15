def total_players_query() -> str:
    return """SELECT count(DISTINCT players) 
              FROM players;
              """

def total_message_query() -> str:
    return """SELECT COUNT(DISTINCT messages)
              FROM messages;
              """

def server_status_query() -> str:
    return """
        SELECT ping, "timestamp"
        FROM server
        ORDER BY "timestamp" ASC;
    """

def total_deaths_query() -> str:
    return """SELECT count(DISTINCT primary_key) 
              FROM death;
              """

def deaths_by_type_query() -> str:
    return """SELECT killer   
              FROM death;
              """


def average_deaths_query() -> str:
    """avec sous-quary; somme de tout les mort(*1.0 pour int -> float) diviser pas le nombre de joueurs"""
    return f"""SELECT 
               (SELECT SUM(death) FROM players) * 1.0
               /
               (SELECT COUNT(primary_key) FROM players);
               """

def list_player_query() -> str:
    return f"""SELECT player
               FROM players
               ORDER BY totalplaytime DESC;
               """

def top_message_senders_query(limit:int=10)->str:
    return f"""SELECT player, messages 
               FROM players 
               ORDER BY messages DESC
               LIMIT {limit};
               """

def death_distribution_query(limit:int=7) -> str:
    return f"""SELECT type, COUNT(type)
               FROM death  
               GROUP BY type
               ORDER BY COUNT(type) DESC
               LIMIT {limit}; 
               """

def top_chatters_query(limit:int=10) -> str:
    return f"""SELECT player,messages
               FROM players
               ORDER BY messages DESC
               LIMIT {limit};
               """

def playercount_over_time_query() -> str:
    return """SELECT playercount, "timestamp" 
              FROM server 
              ORDER BY "timestamp";   
              """

def ping_over_time_query() -> str:
    return """SELECT ping, "timestamp" 
            FROM server 
            ORDER BY "timestamp";
            """

def messages_over_time_query() -> str:
    return """SELECT messages, "timestamp" 
              FROM server 
              ORDER BY "timestamp";
              """


def player_info_query(player:str) -> str :
    return f"""SELECT player, kill, death, messages, total_session, totalplaytime
               FROM players
               WHERE player = '{player}'
               ORDER BY totalplaytime DESC;
               """

def last_chat_lines_query() -> str:
    return f"""SELECT timestamp, player, message
               FROM messages
               ORDER BY timestamp DESC;
               """








def proof_update_query(table: str, primary_key: int, **columns) -> str | None:
    """return None si il a pas d'update a faire"""
    # **columns fais un dict
    if columns is None:
        print("aucune columns a update")
        return None

    set_parts = []

    for key in columns:
        value = columns[key]

        if value is None:
            continue  # ignorer si None

        if type(value) == str:
            part = f"{key} = '{value}'"
        else:
            part = f"{key} = {value}"

        set_parts.append(part)

    if not set_parts:
        print("rien a update")
        return None

    set_clause = ", ".join(set_parts) #same que build d'un objet d'une class

    return f"""UPDATE {table}
               SET {set_clause}
               WHERE primary_key = {primary_key};
               """

def proof_insert_query(table: str, **columns) -> str | None:
    """similair a update"""
    if not columns:
        print("aucune columns a insert")
        return None

    col_names = []
    col_values = []

    for key in columns:
        value = columns[key]
        if value is None:
            continue  # ignorer si None

        col_names.append(key)
        if type(value) == str:
            col_values.append(f"'{value}'")
        else:
            col_values.append(str(value))

    if not col_names:
        print("rien a update")
        return None

    columns_clause = ", ".join(col_names)
    values_clause = ", ".join(col_values)

    #INSERT INTO Livre (titre , editeur , annee , isbn) VALUES ('Manuel de NSI Terminale', 'Mr le prof',2023, '12345678910110')
    return f"INSERT INTO {table} ({columns_clause}) VALUES ({values_clause});"

def proof_delete_query(table: str, primary_key: int) -> str:
    return f"""DELETE FROM {table} 
               WHERE primary_key = {primary_key};
               """

