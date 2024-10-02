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

    def check_migration(self):
        self.connect_to_mysql()
        self.check_required_tables()

    def check_required_tables(self):
        self.cursor.execute("SHOW TABLES")
        tables = {table[0] for table in self.cursor.fetchall()}

        if "serverlist" not in tables:
            self.create_serverlist_table()
            print("Serverlist table created successfully!")

        if "channels" not in tables:
            self.create_channels_table()
            print("Channels table created successfully!")

    def create_serverlist_table(self):
        create_table_query = """
        CREATE TABLE serverlist (
            JoinID INTEGER PRIMARY KEY AUTO_INCREMENT,
            GuildID BIGINT NOT NULL UNIQUE,
            FirstConnectedDate DATETIME NOT NULL,
            RecentConnectedDate DATETIME NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.db.commit()

    def create_channels_table(self):
        create_table_query = """
        CREATE TABLE channels (
            GuildID BIGINT PRIMARY KEY,
            AdminRoleID BIGINT NOT NULL,
            ModeratorRoleID BIGINT NOT NULL,
            ChangeLogChannelID BIGINT NOT NULL,
            AnnouncementChannelID BIGINT NOT NULL,
            LeaveJoinChannelID BIGINT NOT NULL,
            AdvancedLeaveJoinChannelID BIGINT NOT NULL,
            FOREIGN KEY (GuildID) REFERENCES serverlist (GuildID)
        );
        """
        self.cursor.execute(create_table_query)
        self.db.commit()

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        print("Database connection closed.")
