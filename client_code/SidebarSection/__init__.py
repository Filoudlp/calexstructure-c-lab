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
  def __init__(self, title="", items=None, icon="fa:book", **properties):
    self._title = title
    self._items = items or []   # liste de tuples (name, callback, icon)
    self._icon = icon
    self.is_open = True

    self.init_components(**properties)

    self.header_link.set_event_handler('click', self.header_link_click)
    self._build()
    self._update_header()

  def _build(self):
    for item in self._items:
      # Support tuple (name, callback) OU (name, callback, icon)
      if len(item) == 3:
        name, callback, icon = item
      else:
        name, callback = item
        icon = "fa:angle-right"

      link = Link(text=name, icon=icon, role="section-item")
      link.set_event_handler('click', callback)
      self.items_panel.add_component(link)

  def _update_header(self):
    arrow = "fa:chevron-down" if self.is_open else "fa:chevron-right"
    self.header_link.text = self._title
    self.header_link.icon = self._icon   # icône principale
    self.items_panel.visible = self.is_open

  def expand(self):
    self.is_open = True
    self._update_header()

  def collapse(self):
    self.is_open = False
    self._update_header()

  def header_link_click(self, **event_args):
    if self.is_open:
      self.collapse()
    else:
      self.expand()
      self.raise_event('x-section-opened', sender=self)   # ← ajouter sender