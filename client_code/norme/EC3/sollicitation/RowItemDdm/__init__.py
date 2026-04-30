from ._anvil_designer import RowItemDdmTemplate
from anvil import *
import anvil.server

from ..... import norme


class RowItemDdm(RowItemDdmTemplate):
  def __init__(
    self,
    name,
    var,
    on_change,
    **kwargs,
  ):
    self.init_components(**kwargs)

    self.lbl_name.text = name
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

  @property
  def value(self):
    return self.ddm_section.selected_value