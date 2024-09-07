import discord
from discord.ext import commands
import sqlite3

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

conn.commit()

# Command: Show all games
@bot.command(name="showgames")
async def show_games(ctx):
    c.execute("SELECT game_name FROM games")
    games = c.fetchall()
    if games:
        game_list = "\n".join([game[0] for game in games])
        await ctx.send(f"Current games:\n{game_list}")
    else:
        await ctx.send("No games are currently being tracked.")

# Command: Add a game
@bot.command(name="addgame")
async def add_game(ctx, *, game_name):
    try:
        c.execute("INSERT INTO games (game_name) VALUES (?)", (game_name,))
        conn.commit()
        await ctx.send(f"Game '{game_name}' has been added.")
    except sqlite3.IntegrityError:
        await ctx.send(f"Game '{game_name}' is already being tracked.")

# Command: Remove a game
@bot.command(name="removegame")
async def remove_game(ctx, *, game_name):
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("DELETE FROM games WHERE id = ?", (game_id,))
        c.execute("DELETE FROM user_games WHERE game_id = ?", (game_id,))
        conn.commit()
        await ctx.send(f"Game '{game_name}' has been removed.")
    else:
        await ctx.send(f"Game '{game_name}' not found.")

# Command: Show users playing a specific game
@bot.command(name="whoplays")
async def who_plays(ctx, *, game_name):
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("SELECT user_name FROM user_games WHERE game_id = ?", (game_id,))
        users = c.fetchall()
        if users:
            user_list = "\n".join([user[0] for user in users])
            await ctx.send(f"Users playing '{game_name}':\n{user_list}")
        else:
            await ctx.send(f"No one is currently signed up to play '{game_name}'.")
    else:
        await ctx.send(f"Game '{game_name}' not found.")

# Command: Add user to a game
@bot.command(name="addme")
async def add_me(ctx, *, game_name):
    user_id = str(ctx.author.id)
    user_name = str(ctx.author)
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("SELECT * FROM user_games WHERE user_id = ? AND game_id = ?", (user_id, game_id))
        if not c.fetchone():
            c.execute("INSERT INTO user_games (user_id, user_name, game_id) VALUES (?, ?, ?)",
                      (user_id, user_name, game_id))
            conn.commit()
            await ctx.send(f"{ctx.author.mention}, you have been added to '{game_name}'.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are already signed up for '{game_name}'.")
    else:
        await ctx.send(f"Game '{game_name}' not found.")

# Command: Remove user from a game
@bot.command(name="removeme")
async def remove_me(ctx, *, game_name):
    user_id = str(ctx.author.id)
    c.execute("SELECT id FROM games WHERE game_name = ?", (game_name,))
    game = c.fetchone()
    if game:
        game_id = game[0]
        c.execute("DELETE FROM user_games WHERE user_id = ? AND game_id = ?", (user_id, game_id))
        conn.commit()
        await ctx.send(f"{ctx.author.mention}, you have been removed from '{game_name}'.")
    else:
        await ctx.send(f"Game '{game_name}' not found.")

# Command: Show games user is added to
@bot.command(name="showme")
async def show_me(ctx):
    user_id = str(ctx.author.id)
    c.execute("SELECT game_name FROM games g JOIN user_games ug ON g.id = ug.game_id WHERE ug.user_id = ?", (user_id,))
    games = c.fetchall()
    if games:
        game_list = "\n".join([game[0] for game in games])
        await ctx.send(f"Games you are playing:\n{game_list}")
    else:
        await ctx.send(f"{ctx.author.mention}, you are not signed up for any games.")

# Command: Show games for a specific user
@bot.command(name="showuser")
async def show_user(ctx, user: discord.Member):
    user_id = str(user.id)
    c.execute("SELECT game_name FROM games g JOIN user_games ug ON g.id = ug.game_id WHERE ug.user_id = ?", (user_id,))
    games = c.fetchall()
    if games:
        game_list = "\n".join([game[0] for game in games])
        await ctx.send(f"Games {user.name} is playing:\n{game_list}")
    else:
        await ctx.send(f"{user.mention} is not signed up for any games.")

# Run the bot with your token
bot.run('YOUR_DISCORD_BOT_TOKEN')
