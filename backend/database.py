import pandas as pd
import numpy as np
import sqlite3
import pandas as pd
from collections import namedtuple

class Database:
    def __init__(self, dbname, df):
        self.dbname = dbname
        self.sqliteConnection = None
        self.dframe = df

    def connect(self):
        try:
            self.sqliteConnection = sqlite3.connect(self.dbname)
            cursor = self.sqliteConnection.cursor()
            print("Database created and Successfully Connected to SQLite")
            select_Query = "select sqlite_version();"
            cursor.execute(select_Query)
            record = cursor.fetchall()
            print("SQLite Database Version is: ", record)
        except sqlite3.Error as error:
            print("Error while connecting to sqlite", error)

    def querybuilder(self, ntup):
        string1 = '('
        for i in ntup._fields:
            string1 = string1 + str(i) + ','
        string1 = string1[:-1]  # remove ','
        string1 = string1 + ')'
        string2 = '?,' * (len(ntup) - 1) + '?)'
        query = """INSERT INTO Database""" + string1 + """VALUES (""" + string2
        return query

    def table(self):
        self.connect()
        table_query = '''CREATE TABLE Database (
                            track_id TEXT PRIMARY KEY,
                            track_name TEXT,
                            album_name TEXT,
                            album_popularity FLOAT,
                            release_date TEXT,
                            artist_name TEXT,
                            artist_genres TEXT,
                            acousticness FLOAT,
                            danceability FLOAT,
                            energy FLOAT,
                            instrumentalness FLOAT,
                            liveness FLOAT,
                            loudness FLOAT,
                            mode INTEGER,
                            speechiness FLOAT,
                            tempo FLOAT,
                            valence FLOAT)'''
        try:
            cursor = self.sqliteConnection.cursor()
            cursor.execute(table_query)
            self.sqliteConnection.commit()
            print("SQLite table created")
        except sqlite3.Error as error:
            print("Table exists: ", error)

    def insert(self):
        self.table()
        self.dframe.set_index('track_id', inplace=True, drop=True)
        try:
            cursor = self.sqliteConnection.cursor()
            for row in self.dframe.itertuples():
                data = namedtuple('data',
                                  ['track_id', 'track_name', 'album_name', 'album_popularity', 'release_date', 'artist_name', 'artist_genres', 
                                   'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'mode', 'speechiness',
                                   'tempo', 'valence'])
                #print(*row)
                dt = data(*row)
                que = self.querybuilder(dt)
                cursor.execute(que, row)
                self.sqliteConnection.commit()
            print("Inserted successfully into table")
        except sqlite3.Error as error:
            print("Failed to insert: ", error)
        self.close()

    def readTable(self, column, n):
        self.connect()
        records = None
        try:
            cursor = self.sqliteConnection.cursor()
            sqlite_select_query = """SELECT * from Database ORDER BY """ + column + """ DESC LIMIT """ + str(n)
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            # print("Total rows are:  ", len(records))
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        self.close()
        return records

    def close(self):
        self.sqliteConnection.close()