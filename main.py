import discord
from discord.ext import commands
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

# Bot configuration
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

# SQLite Database setup
conn = sqlite3.connect('games.db')
c = conn.cursor()

# Create tables for games and users if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                game_name TEXT UNIQUE
            )''')

c.execute('''CREATE TABLE IF NOT EXISTS user_games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                user_name TEXT,
                game_id INTEGER,
                FOREIGN KEY (game_id) REFERENCES games(id)
            )''')
c.execute('''CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    command TEXT NOT NULL,
    game_name TEXT
)''')

conn.commit()
# Sync slash commands with Discord
@bot.event
async def on_ready():
    # Register the bot's slash commands globally (across all servers) or for specific guilds
    await bot.tree.sync()  # Global sync
    print(f"Logged in as {bot.user}!")


# Command: Add a game
@bot.tree.command(name="addgame", description="Add a game to the list")
async def add_game(interaction: discord.Interaction, game_name: str):
    try:
        c.execute("INSERT INTO games (game_name) VALUES (?)", (game_name,))
        conn.commit()
        c.execute("INSERT INTO logs (user, command, game_name) VALUES (?, ?, ?)", (str(interaction.user), "addgame", game_name))
        conn.commit()
        await interaction.response.send_message(f"Game '{game_name}' has been added.")
    except sqlite3.IntegrityError:
        await interaction.response.send_message(f"Game '{game_name}' is already being tracked.")


# Command: Show all games in alphabetical order
@bot.tree.command(name="showgames", description="Show all games currently being managed")
async def show_games(interaction: discord.Interaction):
    # Modify the SQL query to sort the results alphabetically
    c.execute("SELECT game_name FROM games ORDER BY game_name ASC")
    games = c.fetchall()
    if games:
        game_list = "\n".join([game[0] for game in games])
        await interaction.response.send_message(f"Current games (alphabetical order):\n{game_list}")
    else:
        await interaction.response.send_message("No games are currently being tracked.")


# Command: Remove a game
@bot.tree.command(name="removegame", description="Remove a game from the list")
@commands.has_permissions(administrator=True)
async def remove_game(interaction: discord.Interaction, game_name: str):
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("DELETE FROM games WHERE id = ?", (game_id,))
        c.execute("DELETE FROM user_games WHERE game_id = ?", (game_id,))
        conn.commit()
        c.execute("INSERT INTO logs (user, command, game_name) VALUES (?, ?, ?)", (str(interaction.user), "removegame", game_name))
        conn.commit()
        await interaction.response.send_message(f"Game '{game_name}' has been removed.")
    else:
        await interaction.response.send_message(f"Game '{game_name}' not found.")


# Command: Show users playing a specific game
@bot.tree.command(name="whoplays", description="Show users who are playing a specific game")
async def who_plays(interaction: discord.Interaction, game_name: str):
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("SELECT user_name FROM user_games WHERE game_id = ?", (game_id,))
        users = c.fetchall()
        if users:
            user_list = "\n".join([user[0] for user in users])
            await interaction.response.send_message(f"Users playing '{game_name}':\n{user_list}")
        else:
            await interaction.response.send_message(f"No one is currently signed up to play '{game_name}'.")
    else:
        await interaction.response.send_message(f"Game '{game_name}' not found.")


# Command: Add user to a game
@bot.tree.command(name="addme", description="Add yourself to a game")
async def add_me(interaction: discord.Interaction, game_name: str):
    user_id = str(interaction.user.id)
    user_name = str(interaction.user)
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("SELECT * FROM user_games WHERE user_id = ? AND game_id = ?", (user_id, game_id))
        if not c.fetchone():
            c.execute("INSERT INTO user_games (user_id, user_name, game_id) VALUES (?, ?, ?)", (user_id, user_name, game_id))
            conn.commit()
            await interaction.response.send_message(f"{interaction.user.mention}, you have been added to '{game_name}'.")
        else:
            await interaction.response.send_message(f"{interaction.user.mention}, you are already signed up for '{game_name}'.")
    else:
        await interaction.response.send_message(f"Game '{game_name}' not found.")


# Command: Remove user from a game
@bot.tree.command(name="removeme", description="Remove yourself from a game")
async def remove_me(interaction: discord.Interaction, game_name: str):
    user_id = str(interaction.user.id)
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("DELETE FROM user_games WHERE user_id = ? AND game_id = ?", (user_id, game_id))
        conn.commit()
        await interaction.response.send_message(f"{interaction.user.mention}, you have been removed from '{game_name}'.")
    else:
        await interaction.response.send_message(f"Game '{game_name}' not found.")


# Command: Show games the user is added to
@bot.tree.command(name="showme", description="Show all games you are added to")
async def show_me(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    c.execute("SELECT game_name FROM games g JOIN user_games ug ON g.id = ug.game_id WHERE ug.user_id = ?", (user_id,))
    games = c.fetchall()
    if games:
        game_list = "\n".join([game[0] for game in games])
        await interaction.response.send_message(f"Games you are playing:\n{game_list}")
    else:
        await interaction.response.send_message(f"{interaction.user.mention}, you are not signed up for any games.")


# Command: Show games a specific user is added to
@bot.tree.command(name="showuser", description="Show all games a specific user is added to")
async def show_user(interaction: discord.Interaction, user: discord.User):
    user_id = str(user.id)
    c.execute("SELECT game_name FROM games g JOIN user_games ug ON g.id = ug.game_id WHERE ug.user_id = ?", (user_id,))
    games = c.fetchall()
    if games:
        game_list = "\n".join([game[0] for game in games])
        await interaction.response.send_message(f"Games {user.name} is playing:\n{game_list}")
    else:
        await interaction.response.send_message(f"{user.mention} is not signed up for any games.")


# Command: Show the most popular games by player count
@bot.tree.command(name="mostplayed", description="Show the top 5 most popular games")
async def popular_games(interaction: discord.Interaction):
    c.execute('''SELECT g.game_name, COUNT(ug.user_id) as player_count
                 FROM games g
                 JOIN user_games ug ON g.id = ug.game_id
                 GROUP BY g.game_name
                 ORDER BY player_count DESC
                 LIMIT 5''')
    games = c.fetchall()
    if games:
        game_list = "\n".join([f"{game[0]} - {game[1]} players" for game in games])
        await interaction.response.send_message(f"Top 5 most popular games:\n{game_list}")
    else:
        await interaction.response.send_message("No games have any players signed up.")


# Command: Show detailed information about a specific game
@bot.tree.command(name="gameinfo", description="Get information about a specific game")
async def game_info(interaction: discord.Interaction, game_name: str):
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("SELECT user_name FROM user_games WHERE game_id = ?", (game_id,))
        users = c.fetchall()
        user_list = "\n".join([user[0] for user in users]) if users else "No players yet."
        player_count = len(users)
        await interaction.response.send_message(f"Game: {game_name}\nPlayers: {player_count}\nUser List:\n{user_list}")
    else:
        await interaction.response.send_message(f"Game '{game_name}' not found.")


# Command: Show a list of all available commands
@bot.tree.command(name="help", description="Show all available bot commands")
async def help_command(interaction: discord.Interaction):
    help_text = """
    **Available Commands:**
    /addgame "game name" - Add a game to the list
    /showgames - Show all games currently being managed
    /whoplays "game name" - Show who is playing a specific game
    /addme "game name" - Add yourself to a game's player list
    /removeme "game name" - Remove yourself from a game's player list
    /showme - Show all games you are added to
    /showuser "@user" - Show all games a user is added to
    /mostplayed - Show the top 5 most popular games
    /gameinfo "game name" - Similar to whoplays but includes a user count
    /removegame "game name" - Remove a game from the list (Admin Only)
    """
    await interaction.response.send_message(help_text)
    
# Command: Show bot version and information
@bot.tree.command(name="botversion", description="Show bot version and additional information")
async def bot_version(interaction: discord.Interaction):
    version_info = """
    **Bot Version:** 1.1
    **Created by:** Tide44
    **GitHub:** [CabinSquadBot](https://github.com/Tide44-cmd/CabinSquadBot)
    """
    await interaction.response.send_message(version_info)
  
# Rename a game in the database (Admin only)
@bot.tree.command(name="renamegame", description="Rename a game in the database (Admin only)")
@commands.has_permissions(administrator=True)
async def rename_game(interaction: discord.Interaction, game_name: str, new_name: str):
    c.execute("UPDATE games SET game_name = ? WHERE game_name = ?", (new_name, game_name))
    conn.commit()
    c.execute("INSERT INTO logs (user, command, game_name) VALUES (?, ?, ?)", (str(interaction.user), "renamegame", f"{game_name} -> {new_name}"))
    conn.commit()
    await interaction.response.send_message(f"Game '{game_name}' has been renamed to '{new_name}'.")
  
# Check who added a specific game (Admin only)  
@bot.tree.command(name="whoadded", description="Check who added a specific game (Admin only)")
@commands.has_permissions(administrator=True)
async def who_added(interaction: discord.Interaction, game_name: str):
    c.execute("SELECT user FROM logs WHERE command = 'addgame' AND game_name = ?", (game_name,))
    users = c.fetchall()
    if users:
        user_list = "\n".join([user[0] for user in users])
        await interaction.response.send_message(f"Users who added '{game_name}':\n{user_list}")
    else:
        await interaction.response.send_message(f"No records found for the game '{game_name}'.")
        
        
# Remove a user from all games (Admin only)        
@bot.tree.command(name="removeuser", description="Remove a user from all games (Admin only)")
@commands.has_permissions(administrator=True)
async def remove_user(interaction: discord.Interaction, user: discord.User):
    user_id = str(user.id)
    
    # Remove the user from all games
    c.execute("DELETE FROM user_games WHERE user_id = ?", (user_id,))
    conn.commit()

    # Log the action
    c.execute("INSERT INTO logs (user, command, game_name) VALUES (?, ?, ?)", (str(interaction.user), "removeuser", f"Removed {user} from all games"))
    conn.commit()

    await interaction.response.send_message(f"User '{user}' has been removed from all games.")

token = os.getenv('DISCORD_TOKEN')
bot.run(token)
