from ._anvil_designer import SidebarSectionTemplate
from anvil import *
import anvil.server
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class SidebarSection(SidebarSectionTemplate):
  def __init__(self, title="", icon="", items=None, on_click=None, **properties):
    self.init_components(**properties)

    self._title = title
    self._icon = icon
    self._is_simple_link = not items
    self.is_open = False

    self.header_link.role = "section-header"

    if self._is_simple_link:
      # --- Mode lien simple ---
      self.header_link.text = title
      self.header_link.icon = icon
      self.items_panel.visible = False
      if on_click:
        self.header_link.set_event_handler('click', on_click)
    else:
      # --- Mode section expandable ---
      self.header_link.set_event_handler('click', self.header_link_click)
      for label, callback, item_icon in items:
        lk = Link(text=label, icon=item_icon, role="section-item")
        lk.set_event_handler('click', callback)
        self.items_panel.add_component(lk)
      self.expand()

  def header_link_click(self, **event_args):
    if self.is_open:
      self.collapse()
    else:
      self.expand()
      self.raise_event('x-section-opened', sender=self)

  def expand(self):
    if self._is_simple_link: return
    self.items_panel.visible = True
    self.header_link.text = f"▼ {self._title}"
    self.header_link.icon = self._icon
    self.is_open = True

  def collapse(self):
    if self._is_simple_link: return
    self.items_panel.visible = False
    self.header_link.text = f"▶ {self._title}"
    self.header_link.icon = self._icon
    self.is_open = False