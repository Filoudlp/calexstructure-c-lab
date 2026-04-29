from ._anvil_designer import SidebarSectionTemplate
from anvil import *


class SidebarSection(SidebarSectionTemplate):
  def __init__(self, title="", icon="", items=None, on_click=None, **properties):
    self.init_components(**properties)

    self._title = title
    self._icon = icon
    self._is_simple_link = not items
    self.is_open = False
    self._sub_links = []
    self._selected_link = None

    if self._is_simple_link:
      # --- Lien simple (Outils, Upgrade, Compte, Log out) ---
      self.header_link.role = "nav-link"
      self.header_link.text = title
      self.header_link.icon = icon
      self.items_panel.visible = False
      if on_click:
        self.header_link.set_event_handler('click', on_click)
    else:
      # --- Section expandable (Eurocode 2, Eurocode 3) ---
      self.header_link.role = "nav-section-header"
      self.header_link.set_event_handler('click', self.header_link_click)
      for label, callback, item_icon in items:
        lk = Link(text=label, icon=item_icon, role="nav-subitem")
        lk.tag.label = label
        lk.tag.callback = callback
        lk.set_event_handler('click', self._on_subitem_click)
        self.items_panel.add_component(lk)
        self._sub_links.append(lk)
      self.expand()

  # --- Gestion clic sur sous-item : applique sélection + callback ---
  def _on_subitem_click(self, sender, **event_args):
    self.select_item(sender)
    sender.tag.callback(sender=sender, **event_args)

  def select_item(self, link):
    """Marque un sous-item comme sélectionné (étoile jaune)."""
    if self._selected_link is not None:
      self._selected_link.role = "nav-subitem"
    link.role = "nav-subitem-selected"
    self._selected_link = link

  # --- Expand / collapse ---
  def header_link_click(self, **event_args):
    if self.is_open:
      self.collapse()
    else:
      self.expand()
      self.raise_event('x-section-opened', sender=self)

  def expand(self):
    if self._is_simple_link: return
    self.items_panel.visible = True
    self.header_link.text = f"▼  {self._title}"
    self.header_link.icon = self._icon
    self.is_open = True

  def collapse(self):
    if self._is_simple_link: return
    self.items_panel.visible = False
    self.header_link.text = f"▶  {self._title}"
    self.header_link.icon = self._icon
    self.is_open = False
