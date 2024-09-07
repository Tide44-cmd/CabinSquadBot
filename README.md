# CabinSquadBot
Discord bot designed to help achievement hunters organize games they want to play with other users. It allows users to manage a personal list of games for which they are seeking co-op partners. The bot supports adding, removing, and displaying games, as well as managing users' participation in specific games.

### Commands:

- **/showgames** - Displays a unique list of all the games currently managed by the bot.
- **/addgame "game name"** - Adds a game to the list of managed games.
- **/removegame "game name"** - Removes a game from the list of managed games.
- **/whoplays "game name"** - Displays a list of users who have added their name to the specified game.
- **/addme "game name"** - Adds the user to the specified game’s list of players.
- **/removeme "game name"** - Removes the user from the specified game’s list of players.
- **/showme** - Displays a list of all the games the user is added to.
- **/showuser "@user"** - Displays a list of all the games the specified user is added to.

### Database:

The bot uses SQLite to store game and user information in two tables: `games` and `user_games`. This ensures persistent data between bot restarts.
