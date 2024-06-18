from discord.ext import commands
import discord


class TestCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send(f"Hello, {ctx.author}")


async def setup(bot):
    await bot.add_cog(TestCommands(bot))
