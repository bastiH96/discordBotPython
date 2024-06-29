import discord
from discord.ext import commands
from settings import settings

from dataAccess.person_data_access import PersonDataAccess
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess

from applicationCommands.person.personOptions import PersonButtonsView
from applicationCommands.shiftsystem.shiftsystemOptions import ShiftsystemButtonsView
from applicationCommands.createComparisonTable import ComparisonTableModal


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


@bot.tree.command(description="Enables you to create, delete or edit shiftsystems", name="shiftsystem")
async def shiftsystem_modal(interaction: discord.Interaction):
    await interaction.response.send_message(view=ShiftsystemButtonsView())


@bot.tree.command(description="Enables you to create, delete or edit persons", name="person")
async def person_options(interaction: discord.Interaction):
    await interaction.response.send_message(view=PersonButtonsView())


@bot.tree.command(description="create a new comparison table", name="create_comparison_table")
async def comparison_table_modal(interaction: discord.Interaction):
    modal = ComparisonTableModal()
    await interaction.response.send_modal(modal)

bot.run(settings.TOKEN)
