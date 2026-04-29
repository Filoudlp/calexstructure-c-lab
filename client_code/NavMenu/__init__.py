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
       
    self._sections = []

    # === Sections Eurocode (expandables) ===
    ec2 = SidebarSection(
      title="Eurocode 2 - Concrete",
      icon="",
      items=[
        ("Flexion", self.open_flexion, "fa:arrow-down"),
        ("Shear",   self.open_shear,   "fa:cut"),
      ]
    )
    self._register_section(ec2)

    ec3 = SidebarSection(
      title="Eurocode 3 - Steel",
      icon="",
      items=[
        ("Tension",     self.open_tension,     "fa:arrows-h"),
        ("Compression", self.open_compression, "fa:compress"),
      ]
    )
    self._register_section(ec3)

    # === Liens simples (style "plat" gris) ===
    outils = SidebarSection(
      title="Outils",
      icon="fa:stars",
      on_click=self.open_outils,
    )
    self.column_panel_1.add_component(outils)

    self.upgrade = SidebarSection(
      title="Upgrade",
      icon="fa:arrow_upward",
      on_click=self.open_upgrade,
    )
    self.column_panel_1.add_component(self.upgrade)
    
    compte = SidebarSection(
      title="Compte",
      icon="fa:person",
      on_click=self.open_compte,
    )
    self.column_panel_1.add_component(compte)

    logout = SidebarSection(
      title="Log out",
      icon="fa:logout",
      on_click=self.do_logout,
    )
    self.column_panel_1.add_component(logout)

    # Ferme les sections expandables sauf la première
    for s in self._sections[1:]:
      s.collapse()

    self.check_upgrade_nav_link()

  # ------------------------------------------------------------------
  def _register_section(self, section):
    section.set_event_handler('x-section-opened', self._on_section_opened)
    self.column_panel_1.add_component(section)
    self._sections.append(section)

  def _on_section_opened(self, sender, **event_args):
    for s in self._sections:
      if s is not sender:
        s.collapse()

  # === Callbacks Eurocode ===
  def open_flexion(self, **event_args):     print("Flexion")
  def open_shear(self, **event_args):       print("Shear")
  def open_tension(self, **event_args):     print("Tension")
  def open_compression(self, **event_args): print("Compression")

  # === Callbacks liens plats ===
  def open_outils(self, **event_args):
    for s in self._sections: s.collapse()
    navigate(path="/tools_list")

  def open_upgrade(self, **event_args):
    for s in self._sections: s.collapse()
    self.stripe_pricing_link_click()

  def open_compte(self, **event_args):
    for s in self._sections: s.collapse()
    navigate(path="/Account")

  def do_logout(self, **event_args):
    anvil.users.logout()
    navigate(path="/")

  # === Callbacks boutons bleus ===
  def open_tools(self, **event_args):
    for s in self._sections: s.collapse()
    navigate(path="/tools_list")

  def open_settings(self, **event_args):
    for s in self._sections: s.collapse()
    print("→ Settings")
  
  def stripe_pricing_link_click(self, **event_args):
    """This method is called when the component is clicked"""
    alert(StripePricing(), large=True)
    self.check_upgrade_nav_link()

  def check_upgrade_nav_link(self):
    self.user = anvil.users.get_user()
    if self.user:
      if self.user["subscription"] == "Free" or not self.user["subscription"]:
        self.upgrade.visible = True
      else:
        self.upgrade.visible = False