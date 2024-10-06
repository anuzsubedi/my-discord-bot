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

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
            print("Database connection closed.")

    def check_migration(self):
        self.connect_to_mysql()
        self.check_required_tables()
        self.close_connection()

    def check_required_tables(self):
        self.cursor.execute("SHOW TABLES")
        existing_tables = {table[0] for table in self.cursor.fetchall()}
        for table_name, create_method in {
            "serverlist": self.create_serverlist_table,
            "channels": self.create_channels_table,
        }.items():
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
            AdminRoleID BIGINT,
            ModeratorRoleID BIGINT,
            ChangeLogChannelID BIGINT,
            AnnouncementChannelID BIGINT,
            LeaveJoinChannelID BIGINTL,
            AdvancedLeaveJoinChannelID BIGINT,
            FOREIGN KEY (GuildID) REFERENCES serverlist (GuildID)
        );
        """
        self.create_table(create_query)

    def check_server(self, guild_id):
        self.cursor.execute(
            "SELECT GuildID FROM serverlist WHERE GuildID = %s", (guild_id,)
        )
        result = self.cursor.fetchone()
        return result is not None

    def insert_server(self, guild_id):
        self.connect_to_mysql()
        if self.check_server(guild_id):
            insert_query = """
            UPDATE serverlist 
            SET RecentConnectedDate = NOW()
            WHERE GuildID = %s
            """
            self.cursor.execute(insert_query, (guild_id,))
        else:
            insert_query = """
            INSERT INTO serverlist (GuildID, FirstConnectedDate, RecentConnectedDate)
            VALUES (%s, NOW(), NOW())
            """
            self.cursor.execute(insert_query, (guild_id,))
        self.db.commit()
        self.close_connection()

    def set_announcement_channel(self, guild_id, channel_id):
        self.connect_to_mysql()
        insert_query = """
        INSERT INTO channels (GuildID, AnnouncementChannelID)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE AnnouncementChannelID = %s
        """
        self.cursor.execute(insert_query, (guild_id, channel_id, channel_id))
        self.db.commit()
        self.close_connection()
