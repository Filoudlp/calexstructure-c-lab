from ._anvil_designer import materiaux_CMTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
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

    # Any code you write here will run before the form opens.

  def __calc_shear_modulus(self):
    """ """
    E = int(self.young_modulus_box.text)
    nu = float(self.nu_box.text)
    self.shear_modulus_box.text = round(E / (2 * (1 + nu)), 2)

    self.shear_modulus_box.italic = True

  @handle("steel_grade_ddm", "change")
  def dropdown_menu_1_change(self, **event_args):
    """This method is called when an item is selected"""
    #if self.dropdown_menu_1.selected_value["MAT"] == self.item_list[1][0]:
    #if self.dropdown_menu_1.selected_value["MAT"] == "S235":
    pass

  @handle("young_modulus_box", "lost_focus")
  def young_modulus_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if self.shear_modulus_box.italic:
      self.__calc_shear_modulus()

  @handle("shear_modulus_box", "change")
  def shear_modulus_box_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.shear_modulus_box.text == "":
      self.shear_modulus_box.italic = True
    else:
      self.shear_modulus_box.italic = False

  @handle("nu_box", "lost_focus")
  def nu_box_lost_focus(self, **event_args):
    """This method is called when the TextBox loses focus"""
    if self.shear_modulus_box.italic:
      self.__calc_shear_modulus()
      

