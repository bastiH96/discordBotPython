import discord
from discord import ui
from dataAccess.person_data_access import PersonDataAccess
from services.excelCalculator import ExcelService
import os
import time
from services.validation import Validator

comparison_table_infos = {}


class PersonsSelect(ui.Select):
    def __init__(self):
        options = self.load_persons()
        super().__init__(placeholder="Choose persons for comparison table",
                         min_values=1,
                         max_values=len(options) if len(options) <= 5 else 5,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        persons = [PersonDataAccess().get_one_person(int(id)) for id in self.values]
        full_path = ExcelService(persons, comparison_table_infos["year"]).create_excel_comparison_table()
        message = f"Here is your comparison table for {comparison_table_infos['year']}"
        await interaction.response.send_message(content=message, file=discord.File(fp=full_path))
        time.sleep(2)
        os.remove(full_path)

    @staticmethod
    def load_persons():
        persons = PersonDataAccess().get_all_persons()
        options = [discord.SelectOption(label=person.name, value=str(person.id)) for person in persons]
        return options


class PersonsSelectView(ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
        self.add_item(PersonsSelect())


class ComparisonTableModal(ui.Modal, title="Create new comparison table"):
    year = ui.TextInput(label="Year:",
                        placeholder="Enter year for comparison table",
                        required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if not Validator.are_integers([self.year.value]):
            await interaction.response.send_message("You haven't entered a valid year. Please try again.")
        elif not Validator.is_valid_year(self.year.value):
            await interaction.response.send_message("You haven't entered a valid year. It must be +-50 years around "
                                                    "the current year.")
        else:
            comparison_table_infos["year"] = int(self.year.value)
            await interaction.response.send_message(view=PersonsSelectView())
