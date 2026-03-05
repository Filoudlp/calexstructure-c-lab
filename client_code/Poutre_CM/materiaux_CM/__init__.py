from ._anvil_designer import materiaux_CMTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class materiaux_CM(materiaux_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_list = []
    for row in app_tables.cm_mat_class.search():
      self.item_list.append((row["MAT"], row))
    self.dropdown_menu_1.items = self.item_list
    self.dropdown_menu_1.selected_value = self.dropdown_menu_1.items[0][1]

    # Any code you write here will run before the form opens.

  @handle("dropdown_menu_1", "change")
  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    #if self.dropdown_menu_1.selected_value["MAT"] == self.item_list[1][0]:
    #if self.dropdown_menu_1.selected_value["MAT"] == "S235":
    pass