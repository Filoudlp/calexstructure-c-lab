from ._anvil_designer import compressionTemplate
from anvil import *
import stripe.checkout
import anvil.server

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go


class compression(compressionTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.card_graph = None
    self.graph_rslt = None
    
    component = []

    # ==========================================================
    # BLOC 1 : DONNÉES D'ENTRÉE
    # ==========================================================
    self.card_data = BlockCard(
      title="Données — Compression",
      header_color="input"  # jaune
    )

    # --- Inputs principaux (toujours visibles) ---
    self.row_ned = RowItem("Ned", value=500, editable=True)
    self.row_fy = RowItem("fy", value=235, editable=True)
    self.row_A = RowItem("A", value=10, editable=True)
    self.card_data.add_input(self.row_ned)
    self.card_data.add_input(self.row_A)
    self.card_data.add_input(self.row_fy)

    # --- Params avancés (cachés par défaut) ---
    self.row_gm0 = RowItem(
      name="γM0", value=1.0, unit="-",
      formula="Coefficient partiel",
      ref="EC3 §6.1",
      editable=True, row_type="param"
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
      title="Vérification compression — EC3 §6.2.4",
      header_color="output"  # bleu
    )
    self.cp.add_component(self.card_results)

    self.card_select = BlockCard(
      title="Selection de section",
      header_color="input"  # bleu
    )

    API_URL = "/section_steel_type"
    response = norme.api_call(API_URL)
    print(response)

    self.row_select_type = RowItemDdm(
      name = "Type de section",
      var = response['liste'],
      on_change=self.on_change_select_type  
    )
    
    self.row_select = RowItemDdm(
      name = "Section",
      on_change=self.on_change_select_sec      
    )

    self.row_checked = RowItemChbx(
      name_lbl = "",
      name_chbx = "Utiliser profilé pour les calculs",
      on_checked=self.on_checked   
    )
    self.card_select.add_input(self.row_select_type)
    self.card_select.add_input(self.row_select)
    self.card_select.add_input(self.row_checked)

    self.cp2 = ColumnPanel()
    self.content_panel.add_component(self.cp2)
    
    self.cp2.add_component(self.card_select)

    self.on_change_select()

    # ==========================================================
    # BOUTON CALCULER
    # ==========================================================
    self.btn_calc = Button(
      text="Calculer",
      background="#1F4E79",
      foreground="#FFFFFF",
      role="primary-color",
      bold=True,                    # Texte en gras → visuellement plus imposant
      font_size=16,                 # Taille de la police
      icon="fa:calculator",         # Optionnel : icône
      spacing_above="medium",
      spacing_below="medium",
    )
    
    # Appliquer un style inline via tag pour forcer la taille
    self.btn_calc.tag.style = "min-width: 200px; padding: 12px 24px; font-size: 16px;"
    self.btn_calc.set_event_handler('click', self.calculer)
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

    self.row_select.update(response['liste'])
    
  
  def on_change_select_sec(self, **event_args):
    self.card_select.clear_param()
    API_URL = "/section_steel_val"
    payload = {
      "section": self.row_select.value,   
    }
    response = norme.api_call(API_URL, payload)#anvil.server.call('api_call', API_URL, payload)

    param = ["b", "h", "e", "A", "Av", "Iy", "Iz", "Wy", "Wz"]
    for val in param:
      if val == "A":
        self.row_sec_A = RowItem(val, value=f"{response['section_properties'][val]:.2f}", editable=False, row_type="param")
        row = self.row_sec_A
      else:
        row = RowItem(val, value=f"{response['section_properties'][val]:.2f}", editable=False, row_type="param")
      self.card_select.add_param(row)
      
    self.on_checked()

  def on_checked(self, **event_args):
    
    if self.row_checked.checked:
        self.row_A.tb_value_enabled = False
        self.row_A.value = self.row_sec_A.value
      
    else:
        self.row_A.tb_value_enabled = True

  def calculer(self, **event_args):
    API_URL = "/api/cm_compression_calc"
    payload = {
      "fy": float(self.row_fy.tb_value.text),
      "gamma_m0": float(self.row_gm0.tb_value.text),
      "A": float(self.row_A.tb_value.text),
      "load": norme.convert_unit(float(self.row_ned.tb_value.text), "kN", "N"),
    }
    response = norme.api_call(API_URL, payload)

    formula = response["nc_rd"]["formula"]
    ned = float(self.row_ned.tb_value.text)
    nrd = norme.convert_unit(response["nc_rd"]["result"], "N", "kN")

    self.card_results.clear_results()
      
    if (ned / nrd)  <= 1.0:
      row_type = "ok"
    else:
      row_type = "nok"
      
    row = RowItem(
      name=response['nc_rd']['name'],
      value=f"{nrd:.2f}",
      unit="kN",
      formula=f"{response['nc_rd']['formula']} \n {response['nc_rd']['formula_values']}",
      ref=response["nc_rd"]["ref"],
      editable=False,
      row_type=row_type
    )
    
    self.card_results.add_result(row)

    if self.card_graph is None:
      self.card_graph = BlockCard(
        title="Graphique Résultat",
        header_color="output"  # bleu
      )
      self.card_graph.toggle_icon_button_1.visible = False
      self.cp2.add_component(self.card_graph)
    else:
      self.card_graph.clear_results()

    self.graph_rslt = RowPlot(val=(ned / nrd))
    self.card_graph.add_result(self.graph_rslt)