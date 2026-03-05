from ._anvil_designer import Poutre_CMTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ..Layout_Calculation import Layout_Calculation


class Poutre_CM(Poutre_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("button_1", "click")
  def button_1_click(self, **event_args):
    """This method is called when the component is clicked."""
    self.layout.fun_show_sidesheet()

  @handle("outlined_button_1", "click")
  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.outlined_button_1.icon == "fa:arrow-down":
      self.outlined_button_1.icon = "fa:arrow-right"
      self.option_avancer_cm_1.visible = False
    else:
      self.outlined_button_1.icon = "fa:arrow-down"
      self.option_avancer_cm_1.visible = True

    
