import yaml

import mysql.connector


class DatabaseManager:
    def __init__(self, config_path="./config.yaml"):
        self.config_path = config_path
        self.db = None
        self.cursor = None

    def load_config(self):
        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def connect_to_mysql(self):
        config = self.load_config()
        try:
            self.db = mysql.connector.connect(
                host=config["mysql"]["host"],
                user=config["mysql"]["user"],
                password=config["mysql"]["password"],
                database=config["mysql"]["database"],
            )
            self.cursor = self.db.cursor()
            print("Connected to MySQL database successfully!")
        except mysql.connector.Error as error:
            print("Error connecting to MySQL database:", error)
