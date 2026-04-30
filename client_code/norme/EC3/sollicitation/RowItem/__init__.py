from ._anvil_designer import RowItemTemplate
from anvil import *

from ..... import norme
class RowItem(RowItemTemplate):
  def __init__(self, var=None, value=None, formula=None, ref=None, 
               unit=None, editable=False, row_type="input", **kwargs):
    self.init_components(**kwargs)

    # Mode 1 : depuis le catalogue VARS
    if isinstance(var, str):
      var = norme.get_rowitem_input(var)
    if var:
      name    = var.name
      unit    = unit    or var.unit
      formula = formula or var.formula or ""
      ref     = ref     or var.ref
    else:
      name = kwargs.get("name", "")

    self.lbl_name.text = name
    self.lbl_unit.text = unit
    self.lbl_formula.text = formula
    self.lbl_ref.text = ref

    self.editable = editable

    if editable:
      self.tb_value.text = str(value)
      self.tb_value.visible = True
      self.lbl_value.visible = False
      self.tb_value.background = "#FCE4D6"  # orange Excel
    else:
      self.lbl_value.text = str(value)
      self.tb_value.visible = False
      self.lbl_value.visible = True

      # Couleur de fond selon type
    colors = {
      "input": "#FFFFFF",
      "param": "#DDEBF7",
      "result": "#FFFFFF",
      "ok": "#C6EFCE",
      "nok": "#FFC7CE",
    }
    self.background = colors.get(row_type, "#FFFFFF")

  @property
  def tb_value_enabled(self):
    return self.tb_value.enabled

  @tb_value_enabled.setter
  def tb_value_enabled(self, val):
    self.tb_value.enabled = val

  @property
  def value(self):
    if self.editable:
      return self.tb_value.text
    else:
      return self.lbl_value.text

  @value.setter
  def value(self, val):
    if self.editable:
      self.tb_value.text = val
    else:
      self.lbl_value.text = val