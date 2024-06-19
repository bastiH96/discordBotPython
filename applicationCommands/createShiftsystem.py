import discord
from discord import ui
from models.shiftsystem import Shiftsystem
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess


class ShiftsystemModel(ui.Modal, title="Create new Shiftsystem"):
    name = ui.TextInput(
        label="Name:",
        placeholder="Enter the name of the shiftsystem",
        required=True)
    pattern = ui.TextInput(
        label="Shiftpattern: (F12,N12,F,S,N,SN,-)",
        placeholder="Example:\nF12\nN12\n-\nF12\nN12\n-\n-\n-",
        style=discord.TextStyle.paragraph,
        required=True)

    async def on_submit(self, interaction: discord.Interaction):
        shiftpattern = self.pattern.value.split("\n")
        shiftsystem = Shiftsystem(self.name.value, shiftpattern)
        ShiftsystemDataAccess().insert_shiftsystem(shiftsystem)

        await interaction.response.send_message("Shiftsystem was created successfully!")
