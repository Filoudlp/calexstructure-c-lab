from ._anvil_designer import geo_defTemplate
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from routing import router
import stripe.checkout
from anvil import handle
import anvil.http
import json

from .... import norme


class geo_def(geo_defTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.btn_optionnal_click()
    self.instance_steel()


  @handle("btn_optionnal", "click")
  def btn_optionnal_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optionnal.icon == "fa:arrow-down":
      self.btn_optionnal.icon = "fa:arrow-right"
      self.box_optional.visible = False
    else:
      self.btn_optionnal.icon = "fa:arrow-down"
      self.box_optional.visible = True

  def instance_steel(self):
    API_URL = "/section_steel"
    response = norme.api_call(API_URL)
    
    self.item_list = []
    for row in response["liste"]:
      self.item_list.append(row)
    self.ddm_section.items = self.item_list
    self.ddm_section.selected_value = self.ddm_section.items[0]
    self.ddm_section_change()

  @handle("ddm_section", "change")
  def ddm_section_change(self, **event_args):
    """This method is called when an item is selected"""

    API_URL = "/section_steel_val"
    payload = {
      "section": self.ddm_section.selected_value,  # "IPE 80"
    }
    response = norme.api_call(API_URL, payload)
    
    self.txb_b.text = response["section_properties"]["b"]
    self.txb_h.text = response["section_properties"]["h"]
    self.txb_Iy.text = response["section_properties"]["Iy"]
    self.txb_Iz.text = response["section_properties"]["Iz"]