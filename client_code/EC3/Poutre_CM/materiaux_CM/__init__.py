from ._anvil_designer import materiaux_CMTemplate
from anvil import handle
from anvil.tables import app_tables

class materiaux_CM(materiaux_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item_list = []
    for row in app_tables.cm_mat_class.search():
      self.item_list.append((row["MAT"], row))
    self.steel_grade_ddm.items = self.item_list
    self.steel_grade_ddm.selected_value = self.steel_grade_ddm.items[0][1]
    self.__calc_shear_modulus()
    self.btn_optionnal_click()

    # Any code you write here will run before the form opens.

  def __calc_shear_modulus(self):
    """ """
    E = int(self.tbx_young_modulus.text)
    nu = float(self.tbx_nu.text)
    self.tbx_shear_modulus.text = round(E / (2 * (1 + nu)), 2)

    self.tbx_shear_modulus.italic = True

  @handle("steel_grade_ddm", "change")
  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    #if self.dropdown_menu_1.selected_value["MAT"] == self.item_list[1][0]:
    #if self.dropdown_menu_1.selected_value["MAT"] == "S235":
    pass

  @handle("tbx_young_modulus", "lost_focus")
  def young_modulus_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if self.tbx_shear_modulus.italic:
      self.__calc_shear_modulus()

  @handle("tbx_shear_modulus", "change")
  def tbx_shear_modulus_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.tbx_shear_modulus.text == "":
      self.tbx_shear_modulus.italic = True
    else:
      self.tbx_shear_modulus.italic = False

  @handle("tbx_nu", "lost_focus")
  def tbx_nu_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if self.tbx_shear_modulus.italic:
      self.__calc_shear_modulus()

  @handle("btn_optionnal", "click")
  def btn_optionnal_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optionnal.icon == "fa:arrow-down":
      self.btn_optionnal.icon = "fa:arrow-right"
      self.box_optional.visible = False
    else:
      self.btn_optionnal.icon = "fa:arrow-down"
      self.box_optional.visible = True
      

