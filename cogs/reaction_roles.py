import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_message_id = self.bot.config['reaction_message_id']  # Replace with your message ID

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Assign roles based on reactions."""
        if payload.message_id != self.reaction_message_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if payload.emoji.name == '👍':
            role = discord.utils.get(guild.roles, name='ThumbsUpRole')  # Replace with your role name
            await member.add_roles(role)
            await member.send(f'You have been given the {role.name} role.')

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """Remove roles based on reactions."""
        if payload.message_id != self.reaction_message_id:
            return
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if payload.emoji.name == '👍':
            role = discord.utils.get(guild.roles, name='ThumbsUpRole')  # Replace with your role name
            await member.remove_roles(role)
            await member.send(f'The {role.name} role has been removed.')

def setup(bot):
    bot.add_cog(ReactionRoles(bot))
