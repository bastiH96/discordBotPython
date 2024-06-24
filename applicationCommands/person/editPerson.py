import datetime
from typing import List

import discord
from discord import ui
from dataAccess.person_data_access import PersonDataAccess
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
from models.person import Person

# needs to be defined for the interpreter otherwise -> TracebackError
selected_person = Person("filler", "filler", datetime.date.today())
updated_person_info = {}


class EditPersonSelect(ui.Select):
    def __init__(self):
        options = self.load_options()
        super().__init__(placeholder="Select a person to edit", min_values=1, max_values=1, options=options)

    @staticmethod
    def load_options() -> List:
        options = []
        for person in PersonDataAccess().get_all_persons():
            options.append(discord.SelectOption(label=person.name, value=str(person.id)))
        return options

    async def callback(self, interaction: discord.Interaction):
        global selected_person
        selected_person = PersonDataAccess().get_one_person(int(self.values[0]))
        await interaction.response.send_message(content=f"What do you want to change on {selected_person.name}?",
                                                view=AttributeSelectView())


class EditPersonSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(EditPersonSelect())


class AttributeSelect(ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="Name", value="name"),
                   discord.SelectOption(label="Alias", value="alias"),
                   discord.SelectOption(label="Shiftpattern start date", value="shiftpattern_start_date"),
                   discord.SelectOption(label="Shiftsystem", value="shiftsystem")]
        super().__init__(placeholder="Select an attribute", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "name":
            await interaction.response.send_modal(ChangeNameModal())
        elif self.values[0] == "alias":
            await interaction.response.send_modal(ChangeAliasModal())
        elif self.values[0] == "shiftpattern_start_date":
            await interaction.response.send_modal(ChangeStartDateModal())
        elif self.values[0] == "shiftsystem":
            await interaction.response.send_message(view=ShiftsystemSelectView())
        else:
            await interaction.response.send_message("Something went wrong")


class AttributeSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(AttributeSelect())


class ChangeNameModal(ui.Modal, title=f"Change {selected_person.name}'s name"):
    name = ui.TextInput(label="New Name:",
                        placeholder="Enter a name",
                        required=True)

    async def on_submit(self, interaction: discord.Interaction):
        updated_person_info["name"] = self.name.value

        await interaction.response.send_message(content=f"Name changed to '{self.name.value}'. Do you also want to "
                                                        f"change the alias?")


class ChangeAliasModal(ui.Modal, title=f"Change {selected_person.name}'s alias"):
    alias = ui.TextInput(label="New Alias:",
                         placeholder="Enter an alias",
                         required=True)

    async def on_submit(self, interaction: discord.Interaction):
        updated_person_info["alias"] = self.alias.value
        await interaction.response.send_message(content=f"Alias changed to '{self.alias.value}'. Do you also want to "
                                                        f"change the alias?")


class ChangeStartDateModal(ui.Modal, title=f"Change {selected_person.name}'s start date for the pattern"):
    day = ui.TextInput(label="Day:",
                       placeholder=f"old: {selected_person.shiftpattern_start_date.day}",
                       required=True)
    month = ui.TextInput(label="Month:",
                         placeholder=f"old: {selected_person.shiftpattern_start_date.month}",
                         required=True)
    year = ui.TextInput(label="Year:",
                        placeholder=f"old: {selected_person.shiftpattern_start_date.year}",
                        required=True)


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


class ShiftsystemSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ShiftsystemSelect())


# needs to be changed to two selects! one for alias and one for name!
class ChangeAlsoAliasOrNameSelect(ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="YES", value="yes"),
                   discord.SelectOption(label="NO", value="no")]
        super().__init__(placeholder="Select an answer", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "no":
            if "name" in updated_person_info:
                selected_person.name = updated_person_info["name"]
            elif "alias" in updated_person_info:
                selected_person.alias = updated_person_info["alias"]
            PersonDataAccess().update_person(selected_person)
        elif self.values[0] == "yes":
            if "name" in updated_person_info:
                await interaction.response.send_modal(ChangeAliasModal())
            elif "alias" in updated_person_info:
                await interaction.response.send_modal(ChangeNameModal())


class ChangeAlsoAliasOrNameSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ChangeAlsoAliasOrNameSelect())
