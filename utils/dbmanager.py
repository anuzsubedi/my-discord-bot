import yaml
import mysql.connector


class DatabaseManager:
    def __init__(self, config_path="./config.yaml"):
        self.config_path = config_path
        self.db = None
        self.cursor = None
        self.config = self.load_config()

    def load_config(self):
        """Load the database configuration from a YAML file."""
        try:
            with open(self.config_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Configuration file {self.config_path} not found.")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            return None

    def connect_to_mysql(self):
        """Establish a connection to the MySQL database."""
        if not self.config:
            print("Missing configuration, cannot connect to database.")
            return
        try:
            self.db = mysql.connector.connect(
                host=self.config["mysql"]["host"],
                user=self.config["mysql"]["user"],
                password=self.config["mysql"]["password"],
                database=self.config["mysql"]["database"],
            )
            self.cursor = self.db.cursor()
            print("Connected to MySQL database successfully!")
        except mysql.connector.Error as error:
            print("Error connecting to MySQL database:", error)

    def close_connection(self):
        """Close the MySQL database connection."""
        if self.cursor:
            self.cursor.close()
        if self.db:
            self.db.close()
            print("Database connection closed.")

    def check_migration(self):
        """Check if necessary tables exist and migrate if they don't."""
        self.connect_to_mysql()
        if self.db and self.cursor:
            self.check_required_tables()
        self.close_connection()

    def check_required_tables(self):
        """Ensure required tables exist, create them if they don't."""
        try:
            self.cursor.execute("SHOW TABLES")
            existing_tables = {table[0] for table in self.cursor.fetchall()}
            required_tables = {
                "serverlist": self.create_serverlist_table,
                "channels": self.create_channels_table,
                "modroles": self.create_mod_roles_table  # Updated table for storing mod roles as integers
            }
            for table_name, create_method in required_tables.items():
                if table_name not in existing_tables:
                    create_method()
                    print(f"{table_name.capitalize()} table created successfully!")
        except mysql.connector.Error as error:
            print(f"Error checking or creating tables: {error}")

    def create_table(self, create_query):
        """Create a new table in the database."""
        try:
            self.cursor.execute(create_query)
            self.db.commit()
        except mysql.connector.Error as error:
            print(f"Error creating table: {error}")

    def create_serverlist_table(self):
        """Create the 'serverlist' table."""
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
        """Create the 'channels' table."""
        create_query = """
        CREATE TABLE channels (
            GuildID BIGINT PRIMARY KEY,
            AdminRoleID BIGINT,
            ModeratorRoleID BIGINT,
            ChangeLogChannelID BIGINT,
            AnnouncementChannelID BIGINT,
            LeaveJoinChannelID BIGINT,
            LogChannelID BIGINT,
            MemberDetailChannelID BIGINT,
            FOREIGN KEY (GuildID) REFERENCES serverlist (GuildID)
        );
        """
        self.create_table(create_query)

    def create_mod_roles_table(self):
        """Create the 'modroles' table with RoleID as an integer."""
        create_query = """
        CREATE TABLE modroles (
            GuildID BIGINT NOT NULL,
            RoleID BIGINT NOT NULL,  -- Store role IDs as BIGINT
            PRIMARY KEY (GuildID, RoleID),
            FOREIGN KEY (GuildID) REFERENCES serverlist (GuildID)
        );
        """
        self.create_table(create_query)

    def check_server(self, guild_id):
        """Check if a server exists in the 'serverlist' table."""
        try:
            self.cursor.execute("SELECT GuildID FROM serverlist WHERE GuildID = %s", (guild_id,))
            result = self.cursor.fetchone()
            return result is not None
        except mysql.connector.Error as error:
            print(f"Error checking server existence: {error}")
            return False

    def insert_server(self, guild_id):
        """Insert a new server or update the recent connection date if it exists."""
        self.connect_to_mysql()
        if self.db and self.cursor:
            try:
                if self.check_server(guild_id):
                    query = """
                    UPDATE serverlist 
                    SET RecentConnectedDate = NOW()
                    WHERE GuildID = %s
                    """
                else:
                    query = """
                    INSERT INTO serverlist (GuildID, FirstConnectedDate, RecentConnectedDate)
                    VALUES (%s, NOW(), NOW())
                    """
                self.cursor.execute(query, (guild_id,))
                self.db.commit()
            except mysql.connector.Error as error:
                print(f"Error inserting/updating server: {error}")
        self.close_connection()

    def set_mod_roles(self, guild_id, role_ids):
        """Set the moderator roles for a server, storing role IDs as integers."""
        self.connect_to_mysql()
        if self.db and self.cursor:
            try:
                # Delete existing mod roles for this guild
                delete_query = "DELETE FROM modroles WHERE GuildID = %s"
                self.cursor.execute(delete_query, (guild_id,))
                
                # Insert new mod roles with integer role IDs
                insert_query = "INSERT INTO modroles (GuildID, RoleID) VALUES (%s, %s)"
                for role_id in role_ids:
                    self.cursor.execute(insert_query, (guild_id, role_id))
                self.db.commit()
            except mysql.connector.Error as error:
                print(f"Error setting mod roles: {error}")
        self.close_connection()

    def get_mod_roles(self, guild_id):
        """Retrieve the moderator roles for a server as a list of integers (role IDs)."""
        self.connect_to_mysql()
        if self.db and self.cursor:
            try:
                query = "SELECT RoleID FROM modroles WHERE GuildID = %s"
                self.cursor.execute(query, (guild_id,))
                result = self.cursor.fetchall()
                return [int(row[0]) for row in result] if result else None  # Return list of role IDs as integers
            except mysql.connector.Error as error:
                print(f"Error retrieving mod roles: {error}")
        self.close_connection()
        return None

    # Channel-related methods (existing code)
    def set_announcement_channel(self, guild_id, channel_id):
        """Set or update the announcement channel for a server."""
        self._set_channel(guild_id, channel_id, 'AnnouncementChannelID')

    def set_join_leave_channel(self, guild_id, channel_id):
        """Set or update the join-leave channel for a server."""
        self._set_channel(guild_id, channel_id, 'LeaveJoinChannelID')

    def set_log_channel(self, guild_id, channel_id):
        """Set or update the log channel for a server."""
        self._set_channel(guild_id, channel_id, 'LogChannelID')

    def set_member_detail_channel(self, guild_id, channel_id):
        """Set or update the member detail channel for a server."""
        self._set_channel(guild_id, channel_id, 'AdvancedLeaveJoinChannelID')

    def _set_channel(self, guild_id, channel_id, column_name):
        """Generic method to set or update a channel in the 'channels' table."""
        self.connect_to_mysql()
        if self.db and self.cursor:
            try:
                query = f"""
                INSERT INTO channels (GuildID, {column_name})
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE {column_name} = %s
                """
                self.cursor.execute(query, (guild_id, channel_id, channel_id))
                self.db.commit()
            except mysql.connector.Error as error:
                print(f"Error setting {column_name}: {error}")
        self.close_connection()

    def get_announcement_channel(self, guild_id):
        """Retrieve the announcement channel for a server."""
        return self._get_channel(guild_id, 'AnnouncementChannelID')

    def get_join_leave_channel(self, guild_id):
        """Retrieve the join-leave channel for a server."""
        return self._get_channel(guild_id, 'LeaveJoinChannelID')

    def get_log_channel(self, guild_id):
        """Retrieve the log channel for a server."""
        return self._get_channel(guild_id, 'LogChannelID')

    def get_member_detail_channel(self, guild_id):
        """Retrieve the member detail channel for a server."""
        return self._get_channel(guild_id, 'AdvancedLeaveJoinChannelID')

    def _get_channel(self, guild_id, column_name):
        """Generic method to retrieve a channel from the 'channels' table."""
        self.connect_to_mysql()
        if self.db and self.cursor:
            try:
                query = f"SELECT {column_name} FROM channels WHERE GuildID = %s"
                self.cursor.execute(query, (guild_id,))
                result = self.cursor.fetchone()
                return result[0] if result else None
            except mysql.connector.Error as error:
                print(f"Error retrieving {column_name}: {error}")
        self.close_connection()
        return None
