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

from ..SidebarSection import SidebarSection

from anvil import designer

class NavMenu(NavMenuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.check_upgrade_nav_link()
    # Any code you write here will run before the form opens.
    self.nvl_tool.item = {"1" : "test1", "bou": "test2"}

    self._sections = []

    tool = SidebarSection(
      title="Outil",
      icon="fa:arrow")
    ec2 = SidebarSection(
      title="Eurocode 2 - Concrete",
      icon="fa:square",                            # 🧱 béton
      items=[
        ("Flexion",    self.open_flexion,    "fa:long-arrow-down"),
        ("Shear",      self.open_shear,      "fa:scissors"),
        ("Deflection", self.open_deflection, "fa:arrows-v"),
        ("Cracking",   self.open_cracking,   "fa:bolt"),
      ]
    )
    self._register_section(ec2)

    ec3 = SidebarSection(
      title="Eurocode 3 - Steel",
      icon="fa:cogs",                          # 🔧 acier
      items=[
        ("Tension",     self.open_tension,     "fa:arrows-h"),
        ("Compression", self.open_compression, "fa:compress"),
        ("Bending",     self.open_bending,     "fa:exchange"),
        ("Buckling",    self.open_buckling,    "fa:random"),
      ]
    )
    self._register_section(ec3)

    # Ferme toutes sauf la première
    for s in self._sections[1:]:
      s.collapse()

  def _register_section(self, section):
    section.set_event_handler('x-section-opened', self._on_section_opened)
    self.column_panel_1.add_component(section)
    self._sections.append(section)
  
  def _on_section_opened(self, **event_args):
    opened = event_args.get('sender')   # ← Anvil passe automatiquement le sender
    for s in self._sections:
      if s is not opened:
        s.collapse()

  # EC2
  def open_flexion(self, **event_args):    print("Flexion")
  def open_shear(self, **event_args):      print("Shear")
  def open_deflection(self, **event_args): print("Deflection")
  def open_cracking(self, **event_args):   print("Cracking")

  # EC3
  def open_tension(self, **event_args):     print("Tension")
  def open_compression(self, **event_args): print("Compression")
  def open_bending(self, **event_args):     print("Bending")
  def open_buckling(self, **event_args):    print("Buckling")
  
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

    # ⚠️ Ces méthodes DOIVENT exister
  def open_flexion(self, **event_args):
    self.content_area.clear()
    # self.content_area.add_component(FlexionForm())
    print("Ouverture Flexion")

  def open_shear(self, **event_args):
    print("Ouverture Shear")

  def open_deflection(self, **event_args):
    print("Ouverture Deflection")

  def open_cracking(self, **event_args):
    print("Ouverture Cracking")