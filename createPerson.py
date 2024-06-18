import discord
from discord import ui, Interaction


class ShiftsystemSelect(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Hello"),
            discord.SelectOption(label="You")
            ]
        super().__init__(placeholder="Select a shiftsystem", max_values=1, min_values=1, options=options)


class SelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(ShiftsystemSelect())


class PersonModal(ui.Modal, title="Create a Person"):
    name = ui.TextInput(label="Name:",
                        placeholder="Enter the name of the person",
                        required=True)
    alias = ui.TextInput(label="Alias:",
                         placeholder="Enter the persons alias",
                         max_length=5,
                         required=True)
    # shiftsystem = ShiftsystemSelect()

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(view=SelectView())


