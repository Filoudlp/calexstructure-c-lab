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
import m3.components as m3
from anvil import handle
import anvil.http
import json


class geo_def(geo_defTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.btn_optionnal_click()

    API_URL = "https://alex25071.pythonanywhere.com/section_steel"
    # Appel API
    try:
      response = anvil.http.request(
        url=API_URL,
        method="POST",
        headers={"Content-Type": "application/json"},
        json=True,  # parse automatiquement la réponse JSON
      )
      self.item_list = []
      for row in response["liste"]:
        self.item_list.append(row)
      self.ddm_section.items = self.item_list
      self.ddm_section.selected_value = self.ddm_section.items[0]
      self.ddm_section_change()

    except anvil.http.HttpError as e:
      print(f"Erreur : {e.status}")

  @handle("btn_optionnal", "click")
  def btn_optionnal_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optionnal.icon == "fa:arrow-down":
      self.btn_optionnal.icon = "fa:arrow-right"
      self.box_optional.visible = False
    else:
      self.btn_optionnal.icon = "fa:arrow-down"
      self.box_optional.visible = True

  @handle("ddm_section", "change")
  def ddm_section_change(self, **event_args):
    """This method is called when an item is selected"""
    API_URL = "https://alex25071.pythonanywhere.com/section_steel_val"
    payload = {
      "section": self.ddm_section.selected_value,  # "IPE 80"
    }
    # Appel API
    try:
      response = anvil.http.request(
        url=API_URL,
        method="POST",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        json=True,  # parse automatiquement la réponse JSON
      )
      self.txb_b.text = response["section_properties"]["b"]
      self.txb_h.text = response["section_properties"]["h"]
      self.txb_e.text = response["section_properties"]["e"]
      self.txb_A.text = response["section_properties"]["A"]
      self.txb_Av.text = response["section_properties"]["Av"]
      self.txb_Iy.text = response["section_properties"]["Iy"]
      self.txb_Iz.text = response["section_properties"]["Iz"]
      self.txb_Wy.text = response["section_properties"]["Wy"]
      self.txb_Wz.text = response["section_properties"]["Wz"]

    except anvil.http.HttpError as e:
      print(f"Erreur : {e.status}")
