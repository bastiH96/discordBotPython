import discord
from discord import ui


class ShiftsystemModel(ui.Modal, title="Create new Shiftsystem"):
    name = ui.TextInput(
        label="Name:",
        placeholder="Enter the name of the shiftsystem",
        required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("Name submitted!")
