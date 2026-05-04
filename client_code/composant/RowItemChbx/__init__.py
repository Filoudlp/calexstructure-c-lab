from ._anvil_designer import RowItemChbxTemplate
from anvil import *

from ... import norme


class RowItemChbx(RowItemChbxTemplate):
  def __init__(
    self,
    name_lbl,
    name_chbx,
    on_checked,
    **kwargs,
  ):
    self.init_components(**kwargs)

    self.lbl_name.text = name_lbl
    self.chbx.text = name_chbx
    self.chbx.set_event_handler("change", on_checked)

  @property
  def checked(self):
    return self.chbx.checked

  @property
  def chkbx_value(self):
    return self.chbx.text

  @checked.setter
  def chkbx_value(self, val):
    self.chbx.text = val