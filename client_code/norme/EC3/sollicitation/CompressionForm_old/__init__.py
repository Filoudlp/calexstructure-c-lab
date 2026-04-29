from ._anvil_designer import CompressionForm_oldTemplate
from anvil import *
import anvil.server
import anvil.designer

from ..BlockCard import BlockCard
from ..RowItem import RowItem


class CompressionForm_old(CompressionForm_oldTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    self.content_panel.role = "page-container"
    # ============== BLOC DONNÉES ==============
    self.card_data = BlockCard(
      title="Compression — Données",
      header_color="#yellow"
    )

    self.card_data2 = BlockCard(
      title="autre — Données",
      header_color="#yellow"
    )

    # Input principal
    self.row_ned = RowItem(
      name="Ned", value=500, unit="kN",
      formula="Effort de compression",
      ref="EC3 §6.2.4",
      editable=True, row_type="input"
    )
    self.row_ned.add_event_handler('x-value-changed', self.calculer)
    self.card_data.add_input(self.row_ned)

    # Params avancés (cachés)
    self.row_fy = RowItem(
      name="fy", value=235, unit="MPa",
      formula="Limite élastique",
      ref="EC3 §3.2.1",
      editable=True, row_type="param"
    )
    self.row_A = RowItem(
      name="A", value=5380, unit="mm²",
      formula="Aire brute",
      ref="-",
      editable=True, row_type="param"
    )
    self.row_gm0 = RowItem(
      name="γM0", value=1.0, unit="-",
      formula="Coef. partiel",
      ref="EC3 §6.1",
      editable=True, row_type="param"
    )

    for row in [self.row_fy, self.row_A, self.row_gm0]:
      row.add_event_handler('x-value-changed', self.calculer)
      self.card_data.add_param(row)

    cp = ColumnPanel()
    #cp.add_component(self.card_data)

    # ============== BLOC RÉSULTATS ==============
    self.card_results = BlockCard(
      title="Vérification — EC3 §6.2.4",
      header_color="blue"
    )
    self.card_results2 = BlockCard(
      title="Vérification — EC3 §6.2.4",
      header_color="blue"
    )
    cp.add_component(self.card_results)
    self.flow_panel_1.add_component(self.card_data)

    cp2 = ColumnPanel()
    #cp2.add_component(self.card_data2)
    #cp2.add_component(self.card_results2)
    self.flow_panel_1.add_component(self.card_data2)
    

    # Calcul initial
    self.calculer()

  def calculer(self, **event_args):
    inputs = {
      "Ned": self.row_ned.value * 1000,  # kN -> N
      "fy": self.row_fy.value,
      "A": self.row_A.value,
      "gamma_m0": self.row_gm0.value,
    }

    try:
      result = anvil.server.call('calc_compression', inputs)
    except Exception as e:
      alert(f"Erreur : {e}")
      return

    self._afficher(result)

  def _afficher(self, result):
    self.card_results.clear_results()

    for f in result['formulas']:
      if f.get('is_check'):
        rtype = "ok" if f['result'] <= 1.0 else "nok"
      else:
        rtype = "result"

        # Conversion unité si N -> kN
      val = f['result']
      unit = f['unit']
      if unit == "N":
        val = val / 1000
        unit = "kN"
      val_str = f"{val:.3f}"

      row = RowItem(
        name=f['name'],
        value=val_str,
        unit=unit,
        formula=f['formula'],
        ref=f['ref'],
        editable=False,
        row_type=rtype
      )
      self.card_results.add_result(row)
