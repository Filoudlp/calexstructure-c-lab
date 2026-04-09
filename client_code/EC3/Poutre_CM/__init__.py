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
    self.btn_optional_click()
    self.btn_detail_rslt_click()

    # Any code you write here will run before the form opens.

  @handle("btn_calc", "click")
  def btn_calc_click(self, **event_args):
    """This method is called when the component is clicked."""
    #self.layout.fun_show_sidesheet(False)
    pass

  @handle("btn_optional", "click")
  def btn_optional_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optional.icon == "fa:arrow-down":
      self.btn_optional.icon = "fa:arrow-right"
      self.option_avancer_cm_1.visible = False
    else:
      self.btn_optional.icon = "fa:arrow-down"
      self.option_avancer_cm_1.visible = True

  @handle("btn_hide", "click")
  def btn_hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_detail_rslt.icon == "fa:arrow-right":
      self.btn_detail_rslt.icon = "fa:arrow-left"
      self.btn_hide.icon = "fa:arrow-left"
      self.layout.fun_show_sidesheet(False)
    else:
      self.btn_detail_rslt.icon = "fa:arrow-right"
      self.btn_hide.icon = "fa:arrow-right"
      self.layout.fun_show_sidesheet(True)

  @handle("btn_detail_rslt", "click")
  def btn_detail_rslt_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.btn_hide_click()
    
