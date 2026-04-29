from ._anvil_designer import CompressionForm_copyTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil.js import get_dom_node

from ..BlockCard import BlockCard
from ..RowItem import RowItem


class CompressionForm_copy(CompressionForm_copyTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

    # ==========================================================
    # BLOC 1 : DONNÉES D'ENTRÉE
    # ==========================================================
    self.card_data = BlockCard(
      title="Données — Compression",
      header_color="#FFF2CC"  # jaune
    )

    # --- Inputs principaux (toujours visibles) ---
    self.row_ned = RowItem(
      name="Ned", value=500, unit="kN",
      formula="Effort de compression",
      ref="EC3 §6.2.4",
      editable=True, row_type="input"
    )
    self.card_data.inputs_panel.add_component(self.row_ned)

    # --- Params avancés (cachés par défaut) ---
    self.row_fy = RowItem(
      name="fy", value=235, unit="MPa",
      formula="Limite élastique",
      ref="EC3 §3.2.1",
      editable=True, row_type="param"
    )
    self.row_A = RowItem(
      name="A", value=5380, unit="mm²",
      formula="Aire brute de la section",
      ref="-",
      editable=True, row_type="param"
    )
    self.row_gm0 = RowItem(
      name="γM0", value=1.0, unit="-",
      formula="Coefficient partiel",
      ref="EC3 §6.1",
      editable=True, row_type="param"
    )

    for row in [self.row_fy, self.row_A, self.row_gm0]:
      self.card_data.params_panel.add_component(row)

    self.cp = ColumnPanel()
    self.content_panel.add_component(self.cp)
    self.cp.add_component(self.card_data)

    # ==========================================================
    # BLOC 2 : RÉSULTATS
    # ==========================================================
    self.card_results = BlockCard(
      title="Vérification compression — EC3 §6.2.4",
      header_color="#DEEBF7"  # bleu
    )
    self.cp.add_component(self.card_results)

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

    # Calcul initial
    self.calculer()

    # ==============================================================
    # CALCUL
    # ==============================================================
  def calculer(self, **event_args):
    """Récupère les inputs, appelle le serveur, affiche les résultats."""

    # 1. Récupérer les valeurs
    inputs = {
      "Ned": self.row_ned.value * 1000,  # kN -> N
      "fy": self.row_fy.value,
      "A": self.row_A.value,
      "gamma_m0": self.row_gm0.value,
    }

    # 2. Appel serveur
    try:
      result = anvil.server.call('calc_compression', inputs)
    except Exception as e:
      alert(f"Erreur de calcul : {e}")
      return

      # 3. Affichage
    self.afficher_resultats(result)

  def afficher_resultats(self, result: dict):
    """Reconstruit le panneau résultats depuis le dict serveur."""
    self.card_results.results_panel.clear()

    for formula in result['formulas']:
      # Déterminer la couleur de ligne
      if formula.get('is_check'):
        row_type = "ok" if formula['result'] <= 1.0 else "nok"
      else:
        row_type = "result"

        # Valeur formatée
      val = formula['result']
      if formula['unit'] == "N":
        val_str = f"{val/1000:.2f}"
        unit = "kN"
      else:
        val_str = f"{val:.4f}"
        unit = formula['unit']

      row = RowItem(
        name=formula['name'],
        value=val_str,
        unit=unit,
        formula=formula['formula'],
        ref=formula['ref'],
        editable=False,
        row_type=row_type
      )
      self.card_results.results_panel.add_component(row)