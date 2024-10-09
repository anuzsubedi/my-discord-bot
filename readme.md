Here's the draft for your updated `README.md` file based on your latest changes:

---

# My Discord Bot

I initially created this bot for personal use, but I decided to open-source it to benefit others as well. Over time, the bot has evolved to support multiple servers and use a MySQL database for configuration, making it more scalable and flexible.

## Key Changes Since v1.0.0-alpha

The previous version (v1.0.0-alpha), available [here](https://github.com/anuzsubedi/my-discord-bot/releases/tag/v1.0.0-alpha), used a `config.yaml` file to configure various features like announcement channels, mod-roles, and logging. That version was focused on a single server configuration.

However, since then, the bot has evolved, and all recent commits are aimed at making the bot **multi-server friendly**. The bot now supports multiple servers using a **MySQL database** to store configurations like roles, channels, and logs for each server, rather than relying on a single YAML file.

## Updated Configuration

The `config.yaml` file has been simplified to only require essential information for the bot to run and connect to the database:

```yaml
discord:
  token: "YOUR_DISCORD_BOT_TOKEN"
  prefix: "!"  # Prefix for text-based commands (if needed)

# Database configuration for MySQL
mysql:
  host: "YOUR_MYSQL_HOST"
  user: "YOUR_MYSQL_USER"
  password: "YOUR_MYSQL_PASSWORD"
  database: "YOUR_MYSQL_DATABASE"
  port: 3306  # Default MySQL port, can be changed if needed
```

### What’s New?
- **Multi-Server Support**: The bot can now manage configurations for multiple servers (e.g., announcement channels, mod-roles, etc.) using the MySQL database.
- **MySQL Database**: All configurations (mod-roles, announcement channels, log channels) are stored in a database rather than in the `config.yaml` file.
  
### Previous Configuration File (`v1.0.0-alpha`)
In version [v1.0.0-alpha](https://github.com/anuzsubedi/my-discord-bot/releases/tag/v1.0.0-alpha), the `config.yaml` looked like this:

```yaml
discord:
  token: "YOUR_DISCORD_BOT_TOKEN"
  prefix: "!"

configuration:
  mod-roles:
    - Moderator
    - Admin
  announcement-channel: YOUR_ANNOUNCEMENT_CHANNEL_ID
  log-channel: YOUR_LOG_CHANNEL_ID
  join-leave-channel: YOUR_JOIN_LEAVE_CHANNEL_ID
  member-detail-log-channel: YOUR_MEMBER_DETAIL_LOG_CHANNEL_ID
```

In contrast, all such configurations are now managed through the MySQL database, and only basic bot setup is required in the `config.yaml` file.

## Getting Started

To get started with the bot, follow these instructions:

### 1. Clone the Repository
```bash
git clone https://github.com/anuzsubedi/my-discord-bot.git
```

### 2. Install Dependencies
Navigate to the bot’s directory and install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Create `config.yaml`
In the root folder of the bot, create a `config.yaml` file with the following format:
```yaml
discord:
  token: "YOUR_DISCORD_BOT_TOKEN"
  prefix: "!"  # Prefix for text-based commands

mysql:
  host: "YOUR_MYSQL_HOST"
  user: "YOUR_MYSQL_USER"
  password: "YOUR_MYSQL_PASSWORD"
  database: "YOUR_MYSQL_DATABASE"
  port: 3306  # Default MySQL port
```

### 4. Configure MySQL Database
Make sure your MySQL database is running and properly. The required tables are created automatically when the bot starts.

### 5. Run the Bot
```bash
python bot.py
```

Ensure the `config.yaml` file is present in the root directory, and the bot will automatically connect to Discord and the MySQL database.

## Contributing

Feel free to open issues or submit pull requests if you would like to contribute to the bot's development. All feedback and suggestions are welcome!

---

Let me know if you need any changes or additions!