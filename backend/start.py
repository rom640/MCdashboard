import subprocess, psycopg2, os, time


#docker and database config
CONTAINER_NAME = "container_3b3france"
DB_NAME = "3b3france"
DB_USER = "postgres"
DB_PASSWORD = "pw"
DUMP_FILE_NAME = "3b3france_dump.psql"


DUMP_FILE = os.path.join(os.path.dirname(__file__), '..', 'database', f'{DUMP_FILE_NAME}')

def run(cmd, **kwargs):
    """run a command in shell"""
    return subprocess.run(cmd, check=True, **kwargs)

#start the container and psycopg2
def start_db():
    """start a new postgresql docker container, restore the dumb and return the host port"""
    print("démarrage du conteneur postgresql...")

    #remove last container if already exists
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    #start postgresql
    run([
        "docker", "run", "--name", CONTAINER_NAME,
        "-e", f"POSTGRES_PASSWORD={DB_PASSWORD}",
        "-e", f"POSTGRES_DB={DB_NAME}",
        "-p", "0:5432",                             #random host port
        "-d", "postgres:16"
    ])

    print("attente 5 secondes que postgresql démarre...")
    time.sleep(5)

    #retrieve host port
    out = subprocess.check_output(
        ["docker", "port", CONTAINER_NAME, "5432/tcp"]
    ).decode().strip()
    port = out.split(":")[-1]
    print(f"postgresql prêt sur le port {port}")

    #start the dumb
    print("restauration du dump...")

    if not os.path.exists(DUMP_FILE):
        raise FileNotFoundError(f"Dump introuvable : {DUMP_FILE}")

    with open(DUMP_FILE, "rb") as f:
        run([
            "docker", "exec", "-i", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", DB_NAME
        ], stdin=f)

    print("db restaurée avec succès") #youpi
    return port

#connecting postgresql
def get_connection(port):
    """create and return a psycopg connection"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host="localhost",
            port=port
        )
        return conn
    except Exception as e:
        print("erreur de connexion postgresql :", e)  #et là c'est le drame

#for testing
if __name__ == "__main__":
    start_db()