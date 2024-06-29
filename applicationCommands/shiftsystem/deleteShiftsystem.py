import discord
from discord import ui, Interaction

from dataAccess.shiftsystem_data_access import ShiftsystemDataAccess
from models.shiftsystem import Shiftsystem


class DeleteShiftsystemSelect(ui.Select):
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
        selected_shiftsystem: Shiftsystem = ShiftsystemDataAccess().get_one_shiftsystem(int(self.values[0]))
        await interaction.response.send_message(content=f"Do you really want to delete '{selected_shiftsystem.name}'",
                                                view=ConfirmSelectView(selected_shiftsystem=selected_shiftsystem))


class DeleteShiftsystemSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(DeleteShiftsystemSelect())


class ConfirmSelect(ui.Select):
    def __init__(self, selected_shiftsystem: Shiftsystem):
        self.selected_shiftsystem = selected_shiftsystem
        options = [discord.SelectOption(label="YES", value="yes"),
                   discord.SelectOption(label="NO", value="no")]
        super().__init__(placeholder="Select an option", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        if self.values[0] == "yes":
            if ShiftsystemDataAccess().delete_shiftsystem(self.selected_shiftsystem.id):
                message = f"{self.selected_shiftsystem.name} was deleted successfully!"
            else:
                message = f"Deletion failed because some person is still using the shiftsystem."
        else:
            message = f"Deletion aborted!"
        await interaction.response.send_message(message)


class ConfirmSelectView(ui.View):
    def __init__(self, *, timeout=180, selected_shiftsystem: Shiftsystem):
        super().__init__(timeout=timeout)
        self.add_item(ConfirmSelect(selected_shiftsystem))
