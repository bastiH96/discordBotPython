from typing import Any

import discord
from discord import ui, Interaction
from discord._types import ClientT

from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
from dataAccess.person_data_access import PersonDataAccess
from models.person import Person
from datetime import date
from services.validation import Validator

person_infos = {}


# -----------
# SELECT OPTION MENU
# -----------
class CreatePersonButton(ui.Button):
    def __init__(self):
        super().__init__(label="Create Person")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(PersonModal())


class DeletePersonButton(ui.Button):
    def __init__(self):
        super().__init__(label="Delete Person")


class EditPersonButton(ui.Button):
    def __init__(self):
        super().__init__(label="Edit Person")


class PersonButtonsView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(CreatePersonButton())
        self.add_item(DeletePersonButton())
        self.add_item(EditPersonButton())


# -----------
# CREATE PERSON
# -----------
class StartDateModal(ui.Modal, title="Enter one start date for the pattern"):
    day = ui.TextInput(label="Day:",
                       placeholder="5",
                       required=True)
    month = ui.TextInput(label="Month:",
                         placeholder="9",
                         required=True)
    year = ui.TextInput(label="Year:",
                        placeholder="2024",
                        required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if not Validator.are_integers([self.year.value, self.month.value, self.day.value]):
            message = "You haven't enter an integer!"
        elif not Validator.is_valid_date(int(self.year.value), int(self.month.value), int(self.day.value)):
            message = "Your entered date wasn't valid. Please try again."
        else:
            person_infos["shiftpattern_start_date"] = date(int(self.year.value),
                                                           int(self.month.value),
                                                           int(self.day.value))
            PersonDataAccess().insert_person(Person(name=person_infos["name"],
                                                    alias=person_infos["alias"],
                                                    shiftpattern_start_date=person_infos["shiftpattern_start_date"],
                                                    shiftsystem_id=person_infos["shiftsystem_id"]))
            message = "Person created successfully!"
        await interaction.response.send_message(message)


class ShiftsystemSelect(ui.Select):
    def __init__(self):
        options = self.load_shiftsystems()
        super().__init__(placeholder="Select a shiftsystem", max_values=1, min_values=1, options=options)

    @staticmethod
    def load_shiftsystems():
        shiftsystems = ShiftsystemDataAccess().get_all_shiftsystems()
        options = []
        for shiftsystem in shiftsystems:
            options.append(discord.SelectOption(label=shiftsystem.name, value=shiftsystem.id))
        return options

    async def callback(self, interaction: discord.Interaction):
        shiftsystem = ShiftsystemDataAccess().get_one_shiftsystem(int(self.values[0]))
        person_infos["shiftsystem_id"] = shiftsystem.id
        await interaction.response.send_modal(StartDateModal())


class SelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ShiftsystemSelect())


class PersonModal(ui.Modal, title="Create a Person (Name & Alias)"):
    name = ui.TextInput(label="Name:",
                        placeholder="Enter the name of the person",
                        required=True)
    alias = ui.TextInput(label="Alias:",
                         placeholder="Enter the persons alias",
                         max_length=5,
                         required=True)

    async def on_submit(self, interaction: discord.Interaction):
        person_infos["name"] = self.name.value
        person_infos["alias"] = self.alias.value
        await interaction.response.send_message(embed=self.create_shiftsystem_embed(), view=SelectView())

    @staticmethod
    def create_shiftsystem_embed() -> discord.Embed:
        embed = discord.Embed(title="Choose one of those shiftsystems", color=discord.Color.dark_embed())

        for shiftsystem in ShiftsystemDataAccess().get_all_shiftsystems():
            shiftsystem_name = f"{shiftsystem.name}: "
            shiftpattern = ""

            for x in range(len(shiftsystem.shiftpattern)):
                if x == len(shiftsystem.shiftpattern) - 1:
                    shiftpattern += f"| {shiftsystem.shiftpattern[x]} |"
                else:
                    shiftpattern += f"| {shiftsystem.shiftpattern[x]} "

            embed.add_field(name=shiftsystem_name, value=shiftpattern, inline=False)
        return embed
