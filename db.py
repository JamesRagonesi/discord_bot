import os

import sqlite3
from sqlite3 import Error

DB_PATH = os.getenv('DB_PATH')

def create_connection():
    connection = None
    try:
        connection = sqlite3.connect(DB_PATH)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def init():
    conn = create_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS TRIGGER_WORDS (
            KEYWORD TEXT              NOT NULL,
            VALUE   TEXT              NOT NULL
        );
    ''')
    conn.close()

    return fetchAll()


def insert(key, val):
    conn = create_connection()

    conn.execute(f"INSERT INTO TRIGGER_WORDS (KEYWORD, VALUE) VALUES ('{key}', '{val}' )");

    conn.commit()
    conn.close()

def fetchAll():
    conn = create_connection()
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from TRIGGER_WORDS')

    trigger_dict = {}

    for row in c.fetchall():
        trigger_dict[row[0]] = row[1]

    return trigger_dict