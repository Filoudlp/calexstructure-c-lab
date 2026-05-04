from ._anvil_designer import bending_cmTemplate
from anvil import *

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go


class bending_cm(bending_cmTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    component = []

    # ==========================================================
    # BLOC 1 : DONNÉES D'ENTRÉE
    # ==========================================================
    self.card_data = BlockCard(
      title="Données — Flexion",
      header_color="input",  # jaune
    )

    # --- Inputs principaux (toujours visibles) ---
    self.row_med = RowItem("Med", value=500, editable=True)
    self.row_fy = RowItem("fy", value=235, editable=True)
    self.row_Wy = RowItem("Wy", value=10, editable=True)
    self.row_Wz = RowItem("Wz", value=10, editable=True)
    self.card_data.add_input(self.row_med)
    self.card_data.add_input(self.row_Wy)
    self.card_data.add_input(self.row_Wz)
    self.card_data.add_input(self.row_fy)

    # --- Params avancés (cachés par défaut) ---
    self.row_gm0 = RowItem(
      name="γM0",
      value=1.0,
      unit="-",
      formula="Coefficient partiel",
      ref="EC3 §6.1",
      editable=True,
      row_type="param",
    )

    component.append(self.row_gm0)

    for row in component:
      self.card_data.add_param(row)

    self.cp = ColumnPanel()
    self.content_panel.add_component(self.cp)
    self.cp.add_component(self.card_data)

    # ==========================================================
    # BLOC 2 : RÉSULTATS
    # ==========================================================
    self.card_results = BlockCard(
      title="Vérification Flexion — EC3 §6.2.5",
      header_color="output",  # bleu
    )
    self.cp.add_component(self.card_results)

    self.card_select = BlockCard(
      title="Selection de section",
      header_color="input",  # bleu
    )

    API_URL = "/section_steel_type"
    response = norme.api_call(API_URL)

    self.row_select_type = RowItemDdm(
      name="Type de section",
      var=response["liste"],
      on_change=self.on_change_select_type,
    )

    self.row_select = RowItemDdm(name="Section", on_change=self.on_change_select_sec)

    self.row_checked = RowItemChbx(
      name_lbl="",
      name_chbx="Utiliser profilé pour les calculs",
      on_checked=self.on_checked,
    )
    self.card_select.add_input(self.row_select_type)
    self.card_select.add_input(self.row_select)
    self.card_select.add_input(self.row_checked)

    self.cp2 = ColumnPanel()
    self.content_panel.add_component(self.cp2)

    self.cp2.add_component(self.card_select)

    self.on_change_select_type()
    self.on_change_select_sec()

    # ==========================================================
    # BOUTON CALCULER
    # ==========================================================
    self.btn_calc = Button(
      text="Calculer",
      background="#1F4E79",
      foreground="#FFFFFF",
      role="primary-color",
      bold=True,  # Texte en gras → visuellement plus imposant
      font_size=16,  # Taille de la police
      icon="fa:calculator",  # Optionnel : icône
      spacing_above="medium",
      spacing_below="medium",
    )

    # Appliquer un style inline via tag pour forcer la taille
    self.btn_calc.tag.style = "min-width: 200px; padding: 12px 24px; font-size: 16px;"
    self.btn_calc.set_event_handler("click", self.calculer)
    self.cp.add_component(self.btn_calc)

    # ==============================================================
    # CALCUL
    # ==============================================================

  def on_change_select_type(self, **event_args):
    API_URL = "/section_steel"
    payload = {
      "sec": self.row_select_type.value,
    }

    response = norme.api_call(API_URL, payload)

    self.row_select.update(response["liste"])
    self.on_change_select_sec()

  def on_change_select_sec(self, **event_args):
    self.card_select.clear_param()
    API_URL = "/section_steel_val"
    payload = {
      "type": self.row_select_type.value,
      "section": self.row_select.value,
    }
    response = norme.api_call(API_URL, payload)
    param = ["b", "h", "e", "A", "Av", "Iy", "Iz", "Wy", "Wz"]
    for val in param:
      if response["section_properties"][val] is None:
        value = None
      else:
        value = f"{response['section_properties'][val]:.2f}"

      if val == "Wy":
        self.row_sec_Wy = RowItem(val, value=value, editable=False, row_type="param")
        row = self.row_sec_Wy
      elif val == "Wz":
        self.row_sec_Wz = RowItem(val, value=value, editable=False, row_type="param")
        row = self.row_sec_Wz
      else:
        row = RowItem(val, value=value, editable=False, row_type="param")
      self.card_select.add_param(row)

    self.on_checked()

  def on_checked(self, **event_args):
    if self.row_checked.checked:
      self.row_Wy.tb_value_enabled = False
      self.row_Wy.value = self.row_sec_Wy.value

      self.row_Wz.tb_value_enabled = False
      self.row_Wz.value = self.row_sec_Wz.value

    else:
      self.row_Wy.tb_value_enabled = True
      self.row_Wz.tb_value_enabled = True

  def calculer(self, **event_args):
    API_URL = "/api/cm_bending_calc"
    payload = {
      "fy": float(self.row_fy.tb_value.text),
      "gamma_m0": float(self.row_gm0.tb_value.text),
      "Wy": float(self.row_Wy.tb_value.text),
      "Wz": float(self.row_Wz.tb_value.text),
      "load": norme.convert_unit(float(self.row_med.tb_value.text), "kN", "N"),
    }
    response = norme.api_call(API_URL, payload)

    formula = response["my_rd"]["formula"]
    med = float(self.row_ned.tb_value.text)
    mrd = norme.convert_unit(response["my_rd"]["result"], "N", "kN")

    self.card_results.clear_results()

    if (med / mrd) <= 1.0:
      row_type = "ok"
    else:
      row_type = "nok"

    row_y = RowItem(
      name=response["my_rd"]["name"],
      value=f"{mrd:.2f}",
      unit="kN",
      formula=f"{response['my_rd']['formula']} \n {response['my_rd']['formula_values']}",
      ref=response["my_rd"]["ref"],
      editable=False,
      row_type=row_type,
    )

    row_z = RowItem(
      name=response["mz_rd"]["name"],
      value=f"{mrd:.2f}",
      unit="kN",
      formula=f"{response['mz_rd']['formula']} \n {response['mz_rd']['formula_values']}",
      ref=response["mz_rd"]["ref"],
      editable=False,
      row_type=row_type,
    )

    self.card_results.add_result(row_y)
    self.card_results.add_result(row_z)

    if self.card_graph is None:
      self.card_graph = BlockCard(
        title="Graphique Résultat",
        header_color="output",  # bleu
      )
      self.card_graph.toggle_icon_button_1.visible = False
      self.cp2.add_component(self.card_graph)
    else:
      self.card_graph.clear_results()

    self.graph_rslt = RowPlot(val=(med / mrd))
    self.card_graph.add_result(self.graph_rslt)
