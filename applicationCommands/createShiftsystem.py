import discord
from discord import ui
from models.shiftsystem import Shiftsystem
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
from services.validation import Validator
from typing import List


class ShiftsystemModal(ui.Modal, title="Create new Shiftsystem"):
    name = ui.TextInput(
        label="Name:",
        placeholder="Enter the name of the shiftsystem",
        required=True)
    pattern = ui.TextInput(
        label="Shiftpattern: (F12,N12,F,S,N,SN,-)",
        placeholder="Example:\nF12\nN12\n-\nF12\nN12\n-\n-\n-\n\nor\n\nF12,N12,-,F12,N12,-,-,-",
        style=discord.TextStyle.paragraph,
        required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if not Validator.is_valid_shiftpattern(self.pattern.value):
            message = "invalid pattern!"
        else:
            shiftpattern = self.get_shiftpattern_from_string(self.pattern.value)
            shiftsystem = Shiftsystem(self.name.value, shiftpattern)
            ShiftsystemDataAccess().insert_shiftsystem(shiftsystem)
            message = "valid pattern!"

        await interaction.response.send_message(message)

    @staticmethod
    def get_shiftpattern_from_string(shift_pattern: str) -> List[str]:
        if "," in shift_pattern and "\n" not in shift_pattern:
            return shift_pattern.replace(" ", "").split(",")
        elif "\n" in shift_pattern and "," not in shift_pattern:
            return shift_pattern.replace(" ", "").split("\n")
