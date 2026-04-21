from ._anvil_designer import NavMenuTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

from routing.router import navigate

from ..StripePricing import StripePricing

from anvil import designer

class NavMenu(NavMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_upgrade_nav_link()
    # Any code you write here will run before the form opens.
    self.nvl_tool.item = {"1" : "test1", "bou": "test2"}
    

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
    navigate(path="/tools_list")

  @handle("nvl_logout", "click")
  def nvl_logout_click(self, **event_args):
    """This method is called when the component is clicked"""
    anvil.users.logout()
    open_form('Landing_LoginPage')

  @handle("navigation_link_1", "click")
  def navigation_link_1_click(self, **event_args):
    """This method is called when the component is clicked"""
    navigate(path="/poutre_cm")
