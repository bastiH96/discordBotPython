import discord
from discord import ui, Interaction
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
import json
from models.person import Person
from models.shiftsystem import Shiftsystem
from datetime import date


person_infos = {}


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
        person_infos["shiftsystem"] = shiftsystem
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
        await interaction.response.send_message(view=SelectView())


class StartDateModal(ui.Modal, title="Enter the Start date"):
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
        person_infos["shiftpattern_start_date"] = date(int(self.year.value), int(self.month.value), int(self.day.value))
        await interaction.response.send_message("Person created successfully!")
