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
        self.close_connection()

    def check_required_tables(self):
        self.cursor.execute("SHOW TABLES")
        existing_tables = {table[0] for table in self.cursor.fetchall()}
        tables_to_create = {
            "serverlist": self.create_serverlist_table,
            "channels": self.create_channels_table,
        }

        for table_name, create_method in tables_to_create.items():
            if table_name not in existing_tables:
                create_method()
                print(f"{table_name.capitalize()} table created successfully!")

    def create_table(self, create_query):
        self.cursor.execute(create_query)
        self.db.commit()

    def create_serverlist_table(self):
        create_query = """
        CREATE TABLE serverlist (
            JoinID INTEGER PRIMARY KEY AUTO_INCREMENT,
            GuildID BIGINT NOT NULL UNIQUE,
            FirstConnectedDate DATETIME NOT NULL,
            RecentConnectedDate DATETIME NOT NULL
        );
        """
        self.create_table(create_query)

    def create_channels_table(self):
        create_query = """
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
        self.create_table(create_query)

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
        print("Database connection closed.")
