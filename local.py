import os
from dotenv import load_dotenv
from fabric import Connection
from invoke import Responder


load_dotenv()

try:
    print("Connecting to server")
    conn = Connection('user')
    # print("Successfully connected")
    passing = Responder(
                    pattern = 'Do you want to continue?',
                    response = 'n \n'
                )
    print(conn.local("sudo apt remove python3-pip", watchers=[passing]))
    print("Deployment was successful")
except Exception as e:
    print("Deployment was unsuccessful.\nError:\n")
    print(e)