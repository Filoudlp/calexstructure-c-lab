from ._anvil_designer import tools_concreteTemplate
from anvil import *

from routing.router import navigate

class tools_concrete(tools_concreteTemplate):
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

  @handle("btn_bending", "click")
  def btn_bending_click(self, **event_args):
    """This method is called when the button is clicked"""
    navigate(path="/deflection")
