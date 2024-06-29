import discord
from discord import ui

from typing import List
from models.shiftsystem import Shiftsystem

from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
from services.validation import Validator


class EditShiftsystemSelect(ui.Select):
    def __init__(self):
        options = self.load_options()
        super().__init__(placeholder="Select a shiftsystem", min_values=1, max_values=1, options=options)

    @staticmethod
    def load_options():
        options = []
        for shiftsystem in ShiftsystemDataAccess().get_all_shiftsystems():
            options.append(discord.SelectOption(label=shiftsystem.name, value=str(shiftsystem.id)))
        return options

    async def callback(self, interaction: discord.Interaction):
        shiftsystem = ShiftsystemDataAccess().get_one_shiftsystem(int(self.values[0]))
        await interaction.response.send_message(content=f"What do you want to change on {shiftsystem.name}?",
                                                view=AttributeSelectView(selected_shiftsystem=shiftsystem))


class EditShiftsystemSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(EditShiftsystemSelect())


class AttributeSelect(ui.Select):
    def __init__(self, selected_shiftsystem: Shiftsystem):
        self.selected_shiftsystem = selected_shiftsystem
        options = [discord.SelectOption(label="Name", value="name"),
                   discord.SelectOption(label="Shiftpattern", value="shiftpattern")]
        super().__init__(placeholder="Select an attribute", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "name":
            await interaction.response.send_model(ChangeNameModal(self.selected_shiftsystem))
        elif self.values[0] == "shiftpattern":
            await interaction.response.send_modal(ChangeShiftpatternModal(self.selected_shiftsystem))
        else:
            await interaction.response.send_message("Something went wrong!")


class AttributeSelectView(ui.View):
    def __init__(self, *, timeout=180, selected_shiftsystem: Shiftsystem):
        super().__init__(timeout=timeout)
        self.add_item(AttributeSelect(selected_shiftsystem))


class ChangeNameModal(ui.Modal):
    def __init__(self, selected_shiftsystem: Shiftsystem):
        self.selected_shiftsystem = selected_shiftsystem
        super().__init__(title=f"Change the name of the shiftsystem")
        self.name = ui.TextInput(label="New Name: ",
                                 placeholder=f"{selected_shiftsystem.name}",
                                 required=True)
        self.add_item(self.name)

    async def on_submit(self, interaction: discord.Interaction):
        self.selected_shiftsystem.name = self.name.value
        ShiftsystemDataAccess().update_shiftsystem(self.selected_shiftsystem)
        await interaction.response.send_message("Name of the shiftsystem has been updated successfully!")


# TODO: shiftpattern still accepts empty inputs after , or \n. This needs to be fixed
class ChangeShiftpatternModal(ui.Modal):
    def __init__(self, selected_shiftsystem: Shiftsystem):
        self.selected_shiftsystem = selected_shiftsystem
        pattern = self.load_pattern()
        super().__init__(title=f"Change the shiftpattern of the shiftsystem")
        self.shiftpattern = ui.TextInput(label="Shiftpattern",
                                         default=pattern,
                                         required=True)
        self.add_item(self.shiftpattern)

    def load_pattern(self) -> str:
        pattern = ""
        shiftpattern_len = len(self.selected_shiftsystem.shiftpattern)
        for x in range(shiftpattern_len):
            if x == shiftpattern_len - 1:
                pattern += f"{self.selected_shiftsystem.shiftpattern[x]}"
            else:
                pattern += f"{self.selected_shiftsystem.shiftpattern[x]}, "
        return pattern

    async def on_submit(self, interaction: discord.Interaction):
        if not Validator.is_valid_shiftpattern(self.shiftpattern.value):
            message = "Your pattern was invalid!"
        else:
            self.selected_shiftsystem.shiftpattern = self.get_shiftpattern_from_string(self.shiftpattern.value)
            ShiftsystemDataAccess().update_shiftsystem(self.selected_shiftsystem)
            message = "Shiftpattern of the shiftsystem has been updated successfully!"
        await interaction.response.send_message(message)

    @staticmethod
    def get_shiftpattern_from_string(shift_pattern: str) -> List[str]:
        if "," in shift_pattern and "\n" not in shift_pattern:
            return shift_pattern.replace(" ", "").split(",")
        elif "\n" in shift_pattern and "," not in shift_pattern:
            return shift_pattern.replace(" ", "").split("\n")



