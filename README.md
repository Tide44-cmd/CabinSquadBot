# CabinSquadBot

CabinSquadBot is a Discord bot designed to help achievement hunters organize games they want to play with other users. It allows users to manage a personal list of games for which they are seeking co-op partners. The bot supports adding, removing, and displaying games, as well as managing users' participation in specific games.

## Commands:
- /showgames - Displays a unique list of all the games currently managed by the bot.
- /addgame `"game name"` - Adds a game to the list of managed games.
- /whoplays `"game name"` - Displays a list of users who have added their name to the specified game.
- /addme `"game name"` - Adds the user to the specified game’s list of players.
- /removeme `"game name"` - Removes the user from the specified game’s list of players.
- /showme - Displays a list of all the games the user is added to.
- /showuser `"@user"` - Displays a list of all the games the specified user is added to.
- /mostplayed - Shows the top 5 most popular games.
- /gameinfo `"game name"` - Similar to `/whoplays`, but includes a user count.
- /removegame `"game name"` - Removes a game from the list (Admin Only).

## Database:
The bot uses SQLite to store game and user information in two tables: `games` and `user_games`. This ensures persistent data between bot restarts.

## How to Set Up and Run

### 1. Go to the Discord Developer Portal:
- Visit [Discord Developer Portal](https://discord.com/developers/applications/).
  
### 2. Register a Bot:
- Click on "New Application" and give your bot a name.
- Navigate to the "Bot" section and click "Add Bot".

### 3. Give the Bot Permissions:
- Under the "Bot" section, scroll down to "OAuth2" and select the permissions your bot needs (Send Messages, Use Slash Commands, etc.).

### 4. Get the Bot Token:
- In the "Bot" section, click "Copy" under the "Token" section. **Keep this token secure**.

### 5. Generate a URL:
- Go to the "OAuth2" section, and select "URL Generator".
- Under "Scopes", select `bot`.
- Under "Bot Permissions", select the permissions you need (Send Messages, Manage Messages, Use Slash Commands).
- Copy the generated URL.

### 6. Invite the Bot to Your Discord Server:
- Paste the generated URL into your browser.
- Select the server you want to invite the bot to and authorize it.

### Setting up Environment Variables with `.env`

#### Why Use `.env`?
Using a `.env` file helps keep sensitive information like your bot token out of your codebase. Also when new versions are released your token won't need to be updated.

#### How to Set Up `.env`:
1. Create a `.env` file in the root directory of your bot.
2. Inside the `.env` file, add the following:
   ```env
   DISCORD_BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
Replace `YOUR_DISCORD_BOT_TOKEN` with the token you copied from the Discord Developer Portal.

7. **Host the Bot**:
   - **Locally**:
     - Ensure you have the necessary environment (Python).
     - Run your bot script from your local machine. It will create the SQLite DB in the same section you run it from
   - **On a Raspberry Pi**:
     - Follow the instructions for [here](https://github.com/Tide44-cmd/CabinSquadBot/blob/master/Host%20on%20raspberry%20pi%20zero.md).
