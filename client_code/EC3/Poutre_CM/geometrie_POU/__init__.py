from ._anvil_designer import geometrie_POUTemplate
from anvil import handle
import anvil.http
import json

class geometrie_POU(geometrie_POUTemplate):
  _VAR_GEO = False
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
      "section": self.ddm_section.selected_value,    # "IPE 80"
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
      print(response["section_properties"])
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

  @handle("txb_b", "change")
  def txb_b_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_h", "change")
  def txb_h_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_e", "change")
  def txb_e_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_A", "change")
  def txb_A_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_Av", "change")
  def txb_Av_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_Iy", "change")
  def txb_Iy_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_Iz", "change")
  def txb_Iz_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_Wy", "change")
  def txb_Wy_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("txb_Wz", "change")
  def txb_Wz_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True

  @handle("text_box_11", "change")
  def text_box_11_change(self, **event_args):
    """This method is called when the text in this component is edited."""
    self._VAR_GEO = True
