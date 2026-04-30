from ._anvil_designer import RowItemSecTemplate
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

from ..... import norme


class RowItemSec(RowItemSecTemplate):
  def __init__(
    self,
    var,
    on_change,
    **kwargs,
  ):
    self.init_components(**kwargs)

    self.item_list = []
    for row in var:
      self.item_list.append(row)
    self.ddm_section.items = self.item_list
    self.ddm_section.selected_value = self.ddm_section.items[0]
    self.ddm_section.set_event_handler('change', on_change)
  #  self.ddm_section_change()

  def update(self, var):
    self.item_list = []
    for row in var:
      self.item_list.append(row)
    self.ddm_section.items = self.item_list
    self.ddm_section.selected_value = self.ddm_section.items[0]