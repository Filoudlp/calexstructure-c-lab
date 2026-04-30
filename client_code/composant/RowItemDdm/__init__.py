from ._anvil_designer import RowItemDdmTemplate
from anvil import *

from ... import norme


class RowItemDdm(RowItemDdmTemplate):
  def __init__(
    self,
    name,
    on_change,
    var=None,
    **kwargs,
  ):
    self.init_components(**kwargs)

    self.lbl_name.text = name

    if var is not None:
      self.update(var)

  def update(self, var):
    self.item_list = []
    for row in var:
      self.item_list.append(row)
    self.ddm_section.items = self.item_list
    self.ddm_section.selected_value = self.ddm_section.items[0]

  @property
  def value(self):
    return self.ddm_section.selected_value