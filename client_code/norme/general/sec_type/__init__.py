from ._anvil_designer import sec_typeTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class sec_type(sec_typeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_list = []
    response = ["Acier", "Béton", "Bois"]
    for row in response:
      self.item_list.append(row)
    self.ddm_sec_type.items = self.item_list
    self.ddm_sec_type.selected_value = self.ddm_sec_type.items[0]
    self.ddm_sec_type_change()

    # Any code you write here will run before the form opens.

  @handle("ddm_sec_type", "change")
  def ddm_sec_type_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.ddm_sec_type.selected_value == "Acier":
      self.tbx_E.text = 210000
    elif self.ddm_sec_type.selected_value == "Béton":
      self.tbx_E.text = 33000
