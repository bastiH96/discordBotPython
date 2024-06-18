import discord
from discord.ext import commands
from settings import settings
from applicationCommands.createPerson import PersonModal
from applicationCommands.createShiftsystem import ShiftsystemModel
from dataAccess.person_data_access import PersonDataAccess
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess


class MyClient(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all())

    async def on_ready(self):
        # create database
        ShiftsystemDataAccess().create_shiftsystem_table()
        PersonDataAccess().create_person_table()

        # load normal commands
        await super().load_extension("testCommands")

        # load command tree
        super().tree.copy_global_to(guild=settings.GUILD_ID)
        await super().tree.sync(guild=settings.GUILD_ID)

        print(f"Login successful with user: {self.user}")


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
