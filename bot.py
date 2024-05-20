<<<<<<< HEAD
import discord
from discord.ext import commands
import random
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Create a new bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Load balances from JSON file
def load_balances():
    try:
        with open('balances.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    except FileNotFoundError:
        return {}

# Save balances to JSON file
def save_balances(balances):
    with open('balances.json', 'w') as file:
        json.dump(balances, file)

# Load leaderboard from JSON file
def load_leaderboard():
    try:
        with open('leaderboard.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    except FileNotFoundError:
        return {}

# Save leaderboard to JSON file
def save_leaderboard(leaderboard):
    with open('leaderboard.json', 'w') as file:
        json.dump(leaderboard, file)

# Create or load balances dictionary
balances = load_balances()

# Create or load leaderboard dictionary
leaderboard = load_leaderboard()

# Event: Bot is ready and connected to Discord
@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print(f"Logged in as {bot.user.name}")
    print("Bot is ready to go!")

# Custom check for case-insensitive command matching
def case_insensitive_check(ctx, command):
    return ctx.command.name.lower() == command.lower()

# Command: Ping
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Command: Say
@bot.command()
async def say(ctx, *, message):
    await ctx.send(message)

# Command: Coinflip
@bot.command()
async def coinflip(ctx, bet_amount: int, user_choice: str):
    user_id = str(ctx.author.id)

    if bet_amount <= 0:
        await ctx.send("Bet amount must be a positive number.")
        return

    if user_id not in balances:
        balances[user_id] = 1000

    if balances[user_id] < bet_amount:
        await ctx.send("Insufficient balance.")
        return

    # Perform coinflip
    choices = ['Heads', 'Tails']
    bot_choice = random.choice(choices)

    if user_choice.lower() == bot_choice.lower():
        result = "You won!"
        balances[user_id] += bet_amount
    else:
        result = "You lost!"
        balances[user_id] -= bet_amount

    # Update leaderboard with user balance
    update_leaderboard(user_id)

    # Save updated balances to JSON file
    save_balances(balances)

    await ctx.send(f"Bot's choice: {bot_choice}\nYour choice: {user_choice}\n{result} Your balance: {balances[user_id]}")

# Command: Work
@bot.command()
async def work(ctx):
    user_id = str(ctx.author.id)

    if user_id not in balances:
        balances[user_id] = 0

    earnings = random.randint(50, 200)
    balances[user_id] += earnings

    # Update leaderboard with user balance
    update_leaderboard(user_id)

    # Save updated balances to JSON file
    save_balances(balances)

    await ctx.send(f"You worked and earned {earnings}! Your balance: {balances[user_id]}")

# Command: Balance
@bot.command(aliases=["bal"])
async def balance(ctx):
    user_id = str(ctx.author.id)

    if user_id not in balances:
        balances[user_id] = 0

    current_balance = balances[user_id]
    await ctx.send(f"Your current balance: {current_balance}")

# Command: Show leaderboard
@bot.command()
async def show_leaderboard(ctx):
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)

    if not sorted_leaderboard:
        await ctx.send("The leaderboard is empty.")
        return

    leaderboard_text = "Leaderboard:\n"
    for index, (user_id, balance) in enumerate(sorted_leaderboard):
        member = ctx.guild.get_member(int(user_id))
        if member:
            leaderboard_text += f"{index+1}. {member.display_name}: {balance}\n"
        else:
            leaderboard_text += f"{index+1}. Unknown User ({user_id}): {balance}\n"

    await ctx.send(leaderboard_text)

# Update leaderboard with user balance
def update_leaderboard(user_id):
    if user_id in balances:
        leaderboard[user_id] = balances[user_id]
        save_leaderboard(leaderboard)

# Event: Message is received
@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Process commands first




# Run the bot with your bot token
bot.run("INSERT BOT TOKEN HERE")
=======
import discord
from discord.ext import commands, tasks
import logging
from datetime import datetime, timedelta
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Set up logging
logging.basicConfig(level=logging.INFO, filename='bot.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Initialize the bot with a command prefix from config
bot = commands.Bot(command_prefix=config['prefix'])

# Set up SQLAlchemy
Base = declarative_base()
engine = create_engine('sqlite:///bot_database.db')
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    join_date = Column(DateTime)
    messages_sent = Column(Integer, default=0)

class Role(Base):
    __tablename__ = 'roles'
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String)

Base.metadata.create_all(engine)

# Load cogs
initial_extensions = ['cogs.general', 'cogs.admin', 'cogs.moderation', 'cogs.reaction_roles', 'cogs.music', 'cogs.reminders']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

# Background task that changes the bot's status every 10 seconds
@tasks.loop(seconds=10)
async def activity():
    await bot.change_presence(activity=discord.Game(name='with Python'))

# Scheduled task example: send a message every day at noon
@tasks.loop(hours=24)
async def daily_message():
    now = datetime.utcnow()
    next_noon = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1, hours=12)
    await discord.utils.sleep_until(next_noon)
    channel = bot.get_channel(config['channel_id'])
    await channel.send('Daily reminder message!')

# Start tasks when the bot is ready
@bot.event
async def on_ready():
    logging.info(f'Bot is ready. Logged in as {bot.user}')
    activity.start()
    daily_message.start()

# Enhanced error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Command not found. Please use a valid command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Missing required argument. Please provide all necessary arguments.')
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'This command is on cooldown. Please try again after {round(error.retry_after, 2)} seconds.')
    else:
        await ctx.send(f'An error occurred: {error}')
    logging.error(f'Error: {error}')
    admin = bot.get_user(config['admin_id'])
    if admin:
        await admin.send(f'Error occurred: {error}')

# Run the bot with the token
bot.run(config['token'])
>>>>>>> master
