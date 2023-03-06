from pathlib import Path
import sqlite3
import logging


class Database:
    """ SmartFarm Database client

    Database client to handle and save data into a local SQLite database
    """

    def __init__(self, db_path: str):
        if not Path(db_path).exists():
            Path(db_path).touch()

        self.con = sqlite3.connect(db_path)
        self.cur = self.con.cursor()
        self.__create_tables()

    def __create_tables(self) -> None:
        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='user'")
        if res.fetchone() is None:
            self.cur.execute(
                """CREATE TABLE 'user' (
                'username' VARCHAR(255) NOT NULL, 
                'refresh_token' VARCHAR(255) NOT NULL)"""
            )
            logging.info('Created table `user')

        res = self.cur.execute("SELECT name FROM sqlite_master WHERE name='device'")
        if res.fetchone() is None:
            self.cur.execute(
                """CREATE TABLE 'device' (
                'id' INTEGER NOT NULL,
                'device_id' VARCHAR(100) NOT NULL,
                'name' VARCHAR(255) NOT NULL,
                PRIMARY KEY ('id'))"""
            )
            logging.info('Created table `device')

    def get_refresh_token(self, username: str) -> str | None:
        params = (username,)
        token = self.cur.execute("SELECT refresh_token FROM user WHERE username=?", params).fetchone()

        if token is not None:
            return token[0]

        return None

    def save_refresh_token(self, username: str, refresh_token: str):
        params = (username,)
        token = self.cur.execute("SELECT refresh_token FROM user WHERE username=?", params).fetchone()

        if token is not None:
            sql = "UPDATE user SET refresh_token = :refresh_token WHERE username = :username"
        else:
            sql = "INSERT INTO user VALUES (:username, :refresh_token)"

        params = {"username": username, "refresh_token": refresh_token}
        self.cur.execute(sql, params)
        self.con.commit()

    def save_device(self, device: dict) -> None:
        params = (device["device_id"],)
        existing_device = self.cur.execute("SELECT id FROM device WHERE device_id=?", params).fetchone()

        if existing_device is not None:
            sql = "UPDATE device SET name = :device_name WHERE device_id = :device_id"
        else:
            sql = "INSERT INTO device VALUES (null, :device_id, :device_name)"

        params = {"device_id": device["device_id"], "device_name": device["name"]}

        self.cur.execute(sql, params)
        self.con.commit()
