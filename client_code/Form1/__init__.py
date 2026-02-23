from ._anvil_designer import Form1Template
from anvil import *
import anvil.server

class Form1(Form1Template):
  def __init__(self, **properties):
    self.init_components(**properties)

    # Récupération des éléments HTML via anvil-name
    self.dom_nodes = anvil.js.get_dom_node(self)

  # --- RÉCUPÉRER LES VALEURS ---
  def get_inputs(self):
    return {
      'section': self.dd_section.value if hasattr(self, 'dd_section') else 'Rectangulaire',
      'b': float(self.tb_largeur_b.value or 30),
      'h': float(self.tb_hauteur_h.value or 50),
      'fyk': float(self.tb_fyk.value or 500),
      'ned': float(self.tb_ned.value or 1000),
      'es': float(self.tb_es.value or 200000),
      'nuance': self.dd_nuance.value if hasattr(self, 'dd_nuance') else 'B',
      'eud': float(self.tb_eud.value or 0.01),
      'gamma_s': float(self.tb_gamma_s.value or 1.15),
    }

  # --- BOUTON CALCULER ---
  def btn_calculer_click(self, **event_args):
    inputs = self.get_inputs()

    # Appel serveur
    result = anvil.server.call('calculer_section', inputs)

    # Afficher résultats
    alert(f"Résultat : {result}")

  # --- CHECKBOX OPTIONS AVANCÉES ---
  def cb_options_avancees_change(self, **event_args):
    show = self.cb_options_avancees.checked
    self.pnl_advanced.visible = show
