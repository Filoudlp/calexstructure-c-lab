from ._anvil_designer import compressionTemplate
from anvil import *
import stripe.checkout
import anvil.server

from ..BlockCard import BlockCard
from ..RowItem import RowItem
from ..RowItemSec import RowItemSec
from ..PlotRslt import PlotRslt

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
    self.card_data.inputs_panel.add_component(self.row_ned)
    self.card_data.inputs_panel.add_component(self.row_A)
    self.card_data.inputs_panel.add_component(self.row_fy)

    # --- Params avancés (cachés par défaut) ---
    self.row_gm0 = RowItem(
      name="γM0", value=1.0, unit="-",
      formula="Coefficient partiel",
      ref="EC3 §6.1",
      editable=True, row_type="param"
    )

    component.append(self.row_gm0)

    for row in component:
      self.card_data.params_panel.add_component(row)

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
    self.card_results.toggle_icon_button_1.visible = False
    self.cp.add_component(self.card_results)

    self.card_select = BlockCard(
      title="Selection de section",
      header_color="input"  # bleu
    )

    API_URL = "/section_steel"
    response = norme.api_call(API_URL)

    self.row_select = RowItemSec(
      component = response["liste"],
      on_change=self.on_change_select      
    )

    self.card_select.add_component(self.row_select)
    self.car

    # ==========================================================
    # BOUTON CALCULER
    # ==========================================================
    self.btn_calc = Button(
      text="Calculer",
      background="#1F4E79",
      foreground="#FFFFFF",
      role="primary-color"
    )
    self.btn_calc.set_event_handler('click', self.calculer)
    self.cp.add_component(self.btn_calc)

    # ==============================================================
    # CALCUL
    # ==============================================================
  def on_change_select(self, **event_args):
    print(42)

  def calculer(self, **event_args):
    API_URL = "/api/cm_compression_calc"
    payload = {
      "fy": float(self.row_fy.tb_value.text),
      "gamma_m0": float(self.row_gm0.tb_value.text),
      "A": float(self.row_A.tb_value.text),
      "load": norme.convert_unit(float(self.row_ned.tb_value.text), "kN", "N"),
    }
    response = norme.api_call(API_URL, payload)
    print(response)
    
    formula = response["nc_rd"]["formula"]
    ned = float(self.row_ned.tb_value.text)
    nrd = norme.convert_unit(response["nc_rd"]["result"], "N", "kN")

    self.card_results.rslt_panel.clear()
      
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
    
    self.card_results.rslt_panel.add_component(row)

    if self.card_graph is None:
      self.card_graph = BlockCard(
        title="Graphique Résultat",
        header_color="output"  # bleu
      )
      self.card_graph.toggle_icon_button_1.visible = False
      self.content_panel.add_component(self.card_graph)
    else:
      self.card_graph.rslt_panel.clear()

    self.graph_rslt = PlotRslt(val=(ned / nrd))
    self.card_graph.rslt_panel.add_component(self.graph_rslt)