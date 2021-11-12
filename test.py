import os
from dotenv import load_dotenv
from fabric import Connection


load_dotenv()

try:
    print("Connecting to server")
    conn = Connection(
        host=os.getenv('HOST'),
        connect_kwargs={
            "key_filename": os.getcwd() + "/" + os.getenv('SSH_KEY'),
        }
    )
    print("Successfully connected")
    print(conn.run("whoami"))
    print("Deployment was successful")
except Exception as e:
    print("Deployment was unsuccessful.\nError:\n")
    print(e)