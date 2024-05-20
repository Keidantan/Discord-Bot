import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_admin(ctx):
        """Check if the user is an admin."""
        return ctx.author.guild_permissions.administrator

    @commands.command(name='adminonly')
    @commands.check(is_admin)
    async def admin_only(self, ctx):
        """Command restricted to admin users."""
        await ctx.send('This is an admin-only command.')

    @commands.command(name='addrole')
    @commands.check(is_admin)
    async def add_role(self, ctx, role: discord.Role, member: discord.Member):
        """Add a role to a member."""
        await member.add_roles(role)
        await ctx.send(f'Added role {role.name} to {member.name}.')

    @commands.command(name='removerole')
    @commands.check(is_admin)
    async def remove_role(self, ctx, role: discord.Role, member: discord.Member):
        """Remove a role from a member."""
        await member.remove_roles(role)
        await ctx.send(f'Removed role {role.name} from {member.name}.')

    @commands.command(name='loadcog')
    @commands.check(is_admin)
    async def load_cog(self, ctx, extension):
        """Dynamically load a cog."""
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension} cog.')

    @commands.command(name='unloadcog')
    @commands.check(is_admin)
    async def unload_cog(self, ctx, extension):
        """Dynamically unload a cog."""
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension} cog.')

def setup(bot):
    bot.add_cog(Admin(bot))
