import discord
from discord.ext import commands
import settings
from createPerson import PersonModal
from createShiftsystem import ShiftsystemModel


class MyClient(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self):
        await super().load_extension("testCommands")
        print(f"Login successfully with user: {self.user}")

        super().tree.copy_global_to(guild=settings.GUILD_ID)
        await super().tree.sync(guild=settings.GUILD_ID)


bot = MyClient()


@bot.tree.command(description="create a new shiftsystem", name="create_shiftsystem")
async def shiftsystem_modal(interaction: discord.Interaction):
    modal = ShiftsystemModel()
    await interaction.response.send_modal(modal)


@bot.tree.command(description="create a new person", name="create_person")
async def person_modal(interaction: discord.Interaction):
    modal = PersonModal()
    await interaction.response.send_modal(modal)


bot.run(settings.TOKEN)
