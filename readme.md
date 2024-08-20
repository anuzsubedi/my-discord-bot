# My Discord Bot

I initially created this bot for my personal use, but I have decided to open source it for others to benefit from as well.

Please note that there are more planned features still in progress, so stay tuned for updates!

## Getting Started

To get started with the bot, follow these instructions:

1. Clone the repository to your local machine.

2. In the root folder of the bot, create a `config.yml` file with the following format:

```yaml
discord:
  token: "YOUR_DISCORD_BOT_TOKEN"
  prefix: "!" # Prefix for text-based commands (if you still want to use them)

configuration:
  mod-roles:
    - Moderator
    - Moderators
    # Roles that can use moderation commands
  announcement-channel: YOUR_ANNOUNCEMENT_CHANNEL_ID # Channel id of channel to send announcements
  log-channel: YOUR_LOG_CHANNEL_ID # Channel to log moderation actions
  join-leave-channel: YOUR_JOIN_LEAVE_CHANNEL_ID # Channel to log member leave-join events.
  member-detail-log-channel: YOUR_MEMBER_DETAIL_LOG_CHANNEL_ID # Channel to log member details (more details on members who just joined)
```

3. Replace `YOUR_DISCORD_BOT_TOKEN`, `YOUR_ANNOUNCEMENT_CHANNEL_ID`, `YOUR_LOG_CHANNEL_ID`, `YOUR_JOIN_LEAVE_CHANNEL_ID`, and `YOUR_MEMBER_DETAIL_LOG_CHANNEL_ID` with the appropriate values. Make sure to keep the quotes around the token.

   To obtain a Discord bot token, follow these steps:

   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application.
   - Navigate to the "Bot" tab.
   - Click on "Add Bot" to create a bot for your application.
   - Under the "Token" section, click on "Copy" to copy your bot token.
   - Paste the copied token into the `YOUR_DISCORD_BOT_TOKEN` field in the `config.yml` file.

4. Save the `config.yml` file.

5. Run the bot using your preferred method. Make sure the `config.yml` file is in the root folder of the bot.

That's it! Your bot should now be up and running.
