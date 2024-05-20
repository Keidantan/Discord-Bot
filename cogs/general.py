import discord
from discord.ext import commands
import requests
from sqlalchemy.orm import sessionmaker
from bot import engine, User

Session = sessionmaker(bind=engine)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joindate')
    async def joindate(self, ctx, member: discord.Member):
        """Fetch and display user join date from the database."""
        session = Session()
        user = session.query(User).filter_by(user_id=member.id).first()
        if user:
            await ctx.send(f'{member.name} joined on {user.join_date}')
        else:
            await ctx.send('User not found in the database.')

    @commands.command(name='joke')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def joke(self, ctx):
        """Make an API call to get a random joke."""
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        joke_data = response.json()
        await ctx.send(f'{joke_data["setup"]} - {joke_data["punchline"]}')

    @commands.command(name='weather')
    async def weather(self, ctx, *, city: str):
        """Get the current weather for a city."""
        api_key = self.bot.config['openweathermap_api_key']
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
        response = requests.get(url)
        weather_data = response.json()
        if weather_data.get('cod') != 200:
            await ctx.send('City not found.')
            return
        description = weather_data['weather'][0]['description']
        temp = weather_data['main']['temp']
        await ctx.send(f'The weather in {city} is {description} with a temperature of {temp}°C.')

    @commands.command(name='news')
    async def news(self, ctx):
        """Get the latest news headlines."""
        api_key = self.bot.config['newsapi_api_key']
        url = f'https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}'
        response = requests.get(url)
        news_data = response.json()
        headlines = [article['title'] for article in news_data['articles'][:5]]
        news_message = '\n'.join(headlines)
        await ctx.send(f'Latest News Headlines:\n{news_message}')

def setup(bot):
    bot.add_cog(General(bot))
