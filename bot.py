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