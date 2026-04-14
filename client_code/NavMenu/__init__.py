from ._anvil_designer import NavMenuTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

from ..StripePricing import StripePricing

from anvil import designer

class NavMenu(NavMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_upgrade_nav_link()
    # Any code you write here will run before the form opens.

  def check_upgrade_nav_link(self):
    self.user = anvil.users.get_user()
    if self.user:
      if self.user["subscription"] == "Free" or not self.user["subscription"]:
        self.upgrade_navigation_link.visible = True
      else:
        self.upgrade_navigation_link.visible = False
    else:
      self.upgrade_navigation_link.visible = False

  def logout_navigation_link_click(self, **event_args):
    """This method is called when the component is clicked"""
    anvil.users.logout()

  def stripe_pricing_link_click(self, **event_args):
    """This method is called when the component is clicked"""
    alert(StripePricing(), large=True)
    self.check_upgrade_nav_link()

  @handle("nvl_tool", "click")
  def nvl_tool_click(self, **event_args):
    """This method is called when the component is clicked"""
    open_form('norme.EC3.Xlmt.Poutre_CM')

