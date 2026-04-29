from ._anvil_designer import tools_rdmTemplate
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

from routing.router import navigate

class tools_rdm(tools_rdmTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  @handle("tgicbtn_solicitation", "click")
  def tgicbtn_solicitation_click(self, **event_args):
    if self.tgicbtn_solicitation.icon == "mi:arrow_circle_right":
      self.tgicbtn_solicitation.icon = "mi:arrow_circle_down"
      self.tgicbtn_solicitation.selected = True
      self.otld_soliciation.visible = True
    else:
      self.tgicbtn_solicitation.icon = "mi:arrow_circle_right"
      self.tgicbtn_solicitation.selected = False
      self.otld_soliciation.visible = False

  @handle("tgicbtn_lmt", "click")
  def tgicbtn_lmt_click(self, **event_args):
    if self.tgicbtn_lmt.icon == "mi:arrow_circle_right":
      self.tgicbtn_lmt.icon = "mi:arrow_circle_down"
      self.tgicbtn_lmt.selected = True
      self.otld_lmt.visible = True
    else:
      self.tgicbtn_lmt.icon = "mi:arrow_circle_right"
      self.tgicbtn_lmt.selected = False
      self.otld_lmt.visible = False

  @handle("btn_deflection", "click")
  def btn_deflection_click(self, **event_args):
    """This method is called when the button is clicked"""
    navigate(path="/deflection")
