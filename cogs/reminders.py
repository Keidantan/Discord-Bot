import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []

    @commands.command(name='remind', help='Set a reminder (format: !remind "message" in X minutes)')
    async def remind(self, ctx, time: int, *, message: str):
        reminder_time = datetime.utcnow() + timedelta(minutes=time)
        self.reminders.append((ctx.author.id, reminder_time, message))
        await ctx.send(f'Reminder set for {time} minutes from now.')

    @tasks.loop(seconds=60)
    async def check_reminders(self):
        now = datetime.utcnow()
        for reminder in self.reminders[:]:
            user_id, reminder_time, message = reminder
            if now >= reminder_time:
                user = self.bot.get_user(user_id)
                if user:
                    await user.send(f'Reminder: {message}')
                self.reminders.remove(reminder)

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_reminders.start()

def setup(bot):
    bot.add_cog(Reminder(bot))
