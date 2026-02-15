import subprocess

def main():
    try:
        subprocess.run("streamlit run dashboard.py", shell=True)
    except:
        print("lire la documentation utilisateur du REDME")

if __name__ == '__main__':
    main()