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
