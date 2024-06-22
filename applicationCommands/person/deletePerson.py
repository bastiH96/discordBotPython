from typing import List

import discord
from discord import ui
from dataAccess.person_data_access import PersonDataAccess

global selected_person


class DeletePersonSelect(ui.Select):
    def __init__(self):
        options = self.load_options()
        super().__init__(placeholder="Select a person to delete", min_values=1, max_values=1, options=options)

    @staticmethod
    def load_options() -> List:
        options = []
        for person in PersonDataAccess().get_all_persons():
            options.append(discord.SelectOption(label=person.name, value=str(person.id)))
        return options

    async def callback(self, interaction: discord.Interaction):
        global selected_person
        selected_person = PersonDataAccess().get_one_person(int(self.values[0]))
        await interaction.response.send_message(content=f"Do you really want to delete {selected_person.name}?",
                                                view=ConfirmPersonSelectView())


class DeletePersonSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(DeletePersonSelect())


class ConfirmSelect(ui.Select):
    def __init__(self):
        options = [discord.SelectOption(label="YES", value="yes"),
                   discord.SelectOption(label="NO", value="no")]
        super().__init__(placeholder="Select a person to delete", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "yes":
            PersonDataAccess().delete_person(selected_person.id)
            message = f"{selected_person.name} was deleted successfully!"
        else:
            message = f"Aborted deletion of {selected_person.name}!"
        await interaction.response.send_message(message)


class ConfirmPersonSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ConfirmSelect())
