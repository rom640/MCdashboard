import subprocess, psycopg2, os, time


#config
CONTAINER_NAME = "pg_3b3france"
DB_NAME = "3b3france"
DB_USER = "postgres"
DB_PASSWORD = "pw"
DUMP_FILE = os.path.join("3b3france_dump.psql")


def run(cmd, **kwargs):
    """exécute une commande shell"""
    return subprocess.run(cmd, check=True, **kwargs)

#démarrage du conteneur docker et restauration de la db
def start_db():
    """lance psycopg2 et return le port"""
    print("démarrage du conteneur postgresql...")

    #supprimer l'ancien conteneur s'il existe
    subprocess.run(["docker", "rm", "-f", CONTAINER_NAME],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    #lancer PostgreSQL
    run([
        "docker", "run", "--name", CONTAINER_NAME,
        "-e", f"POSTGRES_PASSWORD={DB_PASSWORD}",
        "-e", f"POSTGRES_DB={DB_NAME}",
        "-p", "0:5432",  # port aléatoire côté hôte
        "-d", "postgres:16"
    ])

    print("attente 5 secondes que postgresql démarre...")
    time.sleep(5)

    #récupérer le port
    out = subprocess.check_output(
        ["docker", "port", CONTAINER_NAME, "5432/tcp"]
    ).decode().strip()
    port = out.split(":")[-1]
    print(f"postgresql prêt sur le port {port}")

    #restaurer le dump
    print("restauration du dump...")
    with open(DUMP_FILE, "rb") as f:
        run([
            "docker", "exec", "-i", CONTAINER_NAME,
            "psql", "-U", DB_USER, "-d", DB_NAME
        ], stdin=f)

    print("db restaurée avec succès") #youpi
    return port

# connexion PostgreSQL
def get_connection(port):
    """retourn une connexion psycopg2"""
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

if __name__ == "__main__":
    start_db()