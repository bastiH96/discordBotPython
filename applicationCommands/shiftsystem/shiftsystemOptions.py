from discord import ui
import discord

from applicationCommands.shiftsystem.createShiftsystem import ShiftsystemModal
from applicationCommands.shiftsystem.deleteShiftsystem import DeleteShiftsystemSelectView
from applicationCommands.shiftsystem.editShiftsystem import EditShiftsystemSelectView


class CreateShiftsystemButton(ui.Button):
    def __init__(self):
        super().__init__(label="Create Shiftsystem")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(ShiftsystemModal())


class DeleteShiftsystemButton(ui.Button):
    def __init__(self):
        super().__init__(label="Delete Shiftsystem")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=DeleteShiftsystemSelectView())


class EditShiftsystemButton(ui.Button):
    def __init__(self):
        super().__init__(label="Edit Shiftsystem")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=EditShiftsystemSelectView())


class ShiftsystemButtonsView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(CreateShiftsystemButton())
        self.add_item(DeleteShiftsystemButton())
        self.add_item(EditShiftsystemButton())
