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
    var=None,
    **kwargs,
  ):
    self.init_components(**kwargs)

    # Mode 1 : depuis le catalogue VARS
    if isinstance(var, str):
      var = norme.get_rowitem_input(var)
    if var:
      name = var.name
      unit = unit or var.unit
      formula = formula or var.formula or ""
      ref = ref or var.ref
    else:
      name = kwargs.get("name", "")

    self.lbl_name.text = name
    self.lbl_unit.text = unit
    self.lbl_formula.text = formula
    self.lbl_ref.text = ref

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

    # Event sur changement

  #  self.tb_value.set_event_handler('change', self._on_change)

  def _on_change(self, **event_args):
    self.raise_event("x-value-changed")

  @property
  def value(self):
    if self.tb_value.visible:
      try:
        return float(self.tb_value.text)
      except (ValueError, TypeError):
        return 0.0
    return self.lbl_value.text
