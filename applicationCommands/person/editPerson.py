from datetime import date
from typing import List

import discord
from discord import ui
from dataAccess.person_data_access import PersonDataAccess
from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
from models.person import Person
from services.validation import Validator


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
        selected_person = PersonDataAccess().get_one_person(int(self.values[0]))
        await interaction.response.send_message(content=f"What do you want to change on {selected_person.name}?",
                                                view=AttributeSelectView(selected_person=selected_person))


class EditPersonSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(EditPersonSelect())


class AttributeSelect(ui.Select):
    def __init__(self, selected_person):
        self.selected_person = selected_person
        options = [discord.SelectOption(label="Name", value="name"),
                   discord.SelectOption(label="Alias", value="alias"),
                   discord.SelectOption(label="Shiftpattern start date", value="shiftpattern_start_date"),
                   discord.SelectOption(label="Shiftsystem", value="shiftsystem")]
        super().__init__(placeholder="Select an attribute", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "name":
            await interaction.response.send_modal(ChangeNameModal(self.selected_person))
        elif self.values[0] == "alias":
            await interaction.response.send_modal(ChangeAliasModal(self.selected_person))
        elif self.values[0] == "shiftpattern_start_date":
            await interaction.response.send_modal(ChangeStartDateModal(self.selected_person))
        elif self.values[0] == "shiftsystem":
            await interaction.response.send_message(view=ShiftsystemSelectView(selected_person=self.selected_person))
        else:
            await interaction.response.send_message("Something went wrong")


class AttributeSelectView(ui.View):
    def __init__(self, *, timeout=180, selected_person):
        super().__init__(timeout=timeout)
        self.add_item(AttributeSelect(selected_person))


class ChangeNameModal(ui.Modal):
    name = ui.TextInput(label="New Name:",
                        placeholder="Enter a name",
                        required=True)

    def __init__(self, selected_person: Person, has_new_alias: bool = False):
        self.has_new_alias = has_new_alias
        self.selected_person = selected_person
        super().__init__(title=f"Change {selected_person.name}'s name")

    async def on_submit(self, interaction: discord.Interaction):
        if self.has_new_alias:
            self.selected_person.name = self.name.value
            PersonDataAccess().update_person(self.selected_person)
            await interaction.response.send_message(f"{self.selected_person.name} successfully updated!")
        else:
            self.selected_person.name = self.name.value
            await interaction.response.send_message(content=f"Name changed to '{self.name.value}'. Do you also want to "
                                                            f"change the alias?",
                                                    view=AskForAliasChangeSelectView(selected_person=self.selected_person))


class ChangeAliasModal(ui.Modal):
    alias = ui.TextInput(label="New Alias:",
                         placeholder="Enter an alias",
                         required=True)

    def __init__(self, selected_person: Person, has_new_name: bool = False):
        self.has_new_name = has_new_name
        self.selected_person = selected_person
        super().__init__(title=f"Change {selected_person.name}'s alias")

    async def on_submit(self, interaction: discord.Interaction):
        if self.has_new_name:
            self.selected_person.alias = self.alias.value
            PersonDataAccess().update_person(self.selected_person)
            await interaction.response.send_message(f"{self.selected_person.name} successfully updated!")
        else:
            self.selected_person.alias = self.alias.value
            await interaction.response.send_message(content=f"Alias changed to '{self.alias.value}'. Do you also want "
                                                            f"to change the name?",
                                                    view=AskForNameChangeSelectView(selected_person=self.selected_person))


class ChangeStartDateModal(ui.Modal):
    def __init__(self, selected_person: Person):
        self.selected_person = selected_person
        super().__init__(title=f"Change {selected_person.name}'s start date for the pattern")

        self.day = ui.TextInput(label="Day:",
                                placeholder=f"old: {selected_person.shiftpattern_start_date.day}",
                                required=True)
        self.month = ui.TextInput(label="Month:",
                                  placeholder=f"old: {selected_person.shiftpattern_start_date.month}",
                                  required=True)
        self.year = ui.TextInput(label="Year:",
                                 placeholder=f"old: {selected_person.shiftpattern_start_date.year}",
                                 required=True)
        self.add_item(self.day)
        self.add_item(self.month)
        self.add_item(self.year)

    async def on_submit(self, interaction: discord.Interaction):
        if not Validator.are_integers([self.year.value, self.month.value, self.day.value]):
            message = "At least one of the fields hasn't contained a number!"
        elif not Validator.is_valid_date(int(self.year.value), int(self.month.value), int(self.day.value)):
            message = "Your entered date wasn't valid. Please check the date and try again."
        else:
            self.selected_person.shiftpattern_start_date = date(int(self.year.value),
                                                                int(self.month.value),
                                                                int(self.day.value))
            PersonDataAccess().update_person(self.selected_person)
            message = "Person has been successfully updated!"
        await interaction.response.send_message(message)


class ShiftsystemSelect(ui.Select):
    def __init__(self, selected_person: Person):
        self.selected_person = selected_person
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
        self.selected_person.shiftsystem_id = self.values[0]
        PersonDataAccess().update_person(self.selected_person)
        await interaction.response.send_message(f"Shiftsystem for {self.selected_person.name} has been updated "
                                                f"successfully")


class ShiftsystemSelectView(ui.View):
    def __init__(self, *, timeout=180, selected_person: Person):
        super().__init__(timeout=timeout)
        self.add_item(ShiftsystemSelect(selected_person))


class AskForAliasChangeSelect(ui.Select):
    def __init__(self, selected_person):
        self.selected_person = selected_person
        options = [discord.SelectOption(label="Yes", value="yes"),
                   discord.SelectOption(label="No", value="no")]
        super().__init__(placeholder="Select an answer", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "no":
            PersonDataAccess().update_person(self.selected_person)
            await interaction.response.send_message("Name changed successfully!")
        elif self.values[0] == "yes":
            await interaction.response.send_modal(ChangeAliasModal(selected_person=self.selected_person,
                                                                   has_new_name=True))


class AskForAliasChangeSelectView(ui.View):
    def __init__(self, *, timeout=180, selected_person: Person):
        super().__init__(timeout=timeout)
        self.add_item(AskForAliasChangeSelect(selected_person))


class AskForNameChangeSelect(ui.Select):
    def __init__(self, selected_person: Person):
        self.selected_person = selected_person
        options = [discord.SelectOption(label="Yes", value="yes"),
                   discord.SelectOption(label="No", value="no")]
        super().__init__(placeholder="Select an answer", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "no":
            PersonDataAccess().update_person(self.selected_person)
            await interaction.response.send_message("Alias changed successfully!")
        elif self.values[0] == "yes":
            await interaction.response.send_modal(ChangeNameModal(selected_person=self.selected_person,
                                                                  has_new_alias=True))


class AskForNameChangeSelectView(ui.View):
    def __init__(self, *, timeout=180, selected_person: Person):
        super().__init__(timeout=timeout)
        self.add_item(AskForNameChangeSelect(selected_person))
