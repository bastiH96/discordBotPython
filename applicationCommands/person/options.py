from discord import ui
import discord
from applicationCommands.person.createPerson import PersonModal
from applicationCommands.person.deletePerson import DeletePersonSelectView


class CreatePersonButton(ui.Button):
    def __init__(self):
        super().__init__(label="Create Person")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(PersonModal())


class DeletePersonButton(ui.Button):
    def __init__(self):
        super().__init__(label="Delete Person")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=DeletePersonSelectView())


class EditPersonButton(ui.Button):
    def __init__(self):
        super().__init__(label="Edit Person")


class PersonButtonsView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(CreatePersonButton())
        self.add_item(DeletePersonButton())
        self.add_item(EditPersonButton())
