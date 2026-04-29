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

    upgrade = SidebarSection(
      title="Upgrade",
      icon="fa:arrow_upward",
      on_click=self.open_upgrade,
    )
    self.column_panel_1.add_component(upgrade)

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

    # === Boutons bleus clairs (Tools + Settings) ===
    tools = SidebarSection(
      title="Tools",
      icon="",
      on_click=self.open_tools,
    )
    self.column_panel_1.add_component(tools)

    settings = SidebarSection(
      title="Settings",
      icon="",
      on_click=self.open_settings,
      role="nav-light-button",
    )
    self.column_panel_1.add_component(settings)

    # Ferme les sections expandables sauf la première
    for s in self._sections[1:]:
      s.collapse()

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
    print("→ Outils")
    navigate(path="/tools_list")

  def open_upgrade(self, **event_args):
    for s in self._sections: s.collapse()
    self.stripe_pricing_link_click()

  def open_compte(self, **event_args):
    for s in self._sections: s.collapse()
    print("→ Compte")

  def do_logout(self, **event_args):
    anvil.users.logout()
    print("→ Déconnecté")
    navigate(path="/login")

  # === Callbacks boutons bleus ===
  def open_tools(self, **event_args):
    for s in self._sections: s.collapse()
    navigate(path="/tools_list")

  def open_settings(self, **event_args):
    for s in self._sections: s.collapse()
    print("→ Settings")
  
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