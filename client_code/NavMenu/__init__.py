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
    
    # Section avec items
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
    
    # ✅ Lien simple — pas d'items, juste un on_click
    tools = SidebarSection(
      title="Tools",
      icon="",
      on_click=self.open_tools          # ← pas d'items=
    )
    self.add_component(tools)
    # ⚠️ NE PAS l'ajouter à _sections (pour ne pas le collapse)
    
    settings = SidebarSection(
      title="Settings",
      icon="",
      on_click=self.open_settings
    )
    self.add_component(settings)
    
    # Ferme les sections expandables sauf la première
    for s in self._sections[1:]:
      s.collapse()

  def _register_section(self, section):
    section.set_event_handler('x-section-opened', self._on_section_opened)
    self.column_panel_1.add_component(section)
    self._sections.append(section)

  def _on_section_opened(self, sender, **event_args):
    for s in self._sections:
      if s is not sender:
        s.collapse()

  # === Callbacks ===
  def open_flexion(self, **event_args):  print("Flexion")
  def open_shear(self, **event_args):    print("Shear")
  def open_tension(self, **event_args):  print("Tension")
  def open_compression(self, **event_args): print("Compression")

  def open_tools(self, **event_args):
    # Ferme toutes les sections expandables pour la clarté
    for s in self._sections:
      s.collapse()
    print("→ open_tools déclenché")
    navigate(path="/tools_list")
    print("perfect")

  def open_settings(self, **event_args):
    for s in self._sections:
      s.collapse()
    print("→ Page Settings")
  
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