import discord
from discord.ext import commands
from settings import settings
from applicationCommands.person.options import PersonButtonsView
from applicationCommands.createShiftsystem import ShiftsystemModal
from applicationCommands.createComparisonTable import ComparisonTableModal
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
    modal = ShiftsystemModal()
    await interaction.response.send_modal(modal)


@bot.tree.command(description="create a new comparison table", name="create_comparison_table")
async def comparison_table_modal(interaction: discord.Interaction):
    modal = ComparisonTableModal()
    await interaction.response.send_modal(modal)


@bot.tree.command(description="Enables you to create, delete or edit a person", name="person")
async def person_options(interaction: discord.Interaction):
    await interaction.response.send_message(view=PersonButtonsView())


bot.run(settings.TOKEN)
