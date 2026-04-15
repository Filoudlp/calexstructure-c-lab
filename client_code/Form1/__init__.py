#from ._anvil_designer import Form1Template
#from anvil import *
#import anvil.server
#import anvil.google.auth, anvil.google.drive
#from anvil.google.drive import app_files
#import anvil.users
#import anvil.tables as tables
#import anvil.tables.query as q
#from anvil.tables import app_tables

#class Form1(Form1Template):
#  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
#    self.init_components(**properties)

    # Any code you write here will run before the form opens.
from ._anvil_designer import Form1Template
from anvil import *
import stripe.checkout
import m3.components as m3
import anvil.server
import plotly.graph_objects as go
import json

class Form1(Form1Template):
  def __init__(self, **properties):
    # Initialisation de l'UI
    self.init_components(**properties)

    # Remplir les listes déroulantes (statique pour le MVP, via Data Tables plus tard)
    self.dd_profile.items = ["IPE 200", "IPE 300", "HEA 200"]
    self.dd_profile.selected_value = self.dd_profile.items[0]
    self.dd_steel.items = [("S235", "S235"), ("S355", "S355")]
    self.dd_steel.selected_value = self.dd_steel.items[0][1]
    #self.loading_icon.visible = False # Spinner caché par défaut

  @handle("btn_calculate", "click")
  def btn_calculate_click(self, **event_args):
    """This method is called when the primary button is clicked"""

    # 1. Validation de base des inputs
    inputs = [float(self.tb_span.text), float(self.tb_gk.text), float(self.tb_qk.text)]
    if any(x is None or x <= 0 for x in inputs):
      alert("Veuillez saisir des valeurs numériques positives pour la géométrie et les charges.")
      return

    # 2. Activation de l'état de chargement
    self.btn_calculate.enabled = False
    self.btn_calculate.text = "Calcul en cours..."
    #self.loading_icon.visible = True

    # 3. Préparation du JSON Request (payload)
    request_payload = {
      "geometry": {
        "profile_designation": self.dd_profile.selected_value,
        "span_m": float(self.tb_span.text)
      },
      "material": {
        "steel_grade": self.dd_steel.selected_value
      },
      "loads": {
        "gk_knm": float(self.tb_gk.text),
        "qk_knm": float(self.tb_qk.text)
      }
    }

    # 4. Appel asynchrone au Server Module d'Anvil
    try:
      # anvil.server.call retourne le dictionnaire de réponse JSON
      api_response = anvil.server.call('call_calculation_api', request_payload)

      if "error" in api_response:
        alert(f"Erreur technique : {api_response['error']}")
      else:
        # 5. Dispatch des résultats vers l'UI
        self.update_ui_results(api_response)

    except Exception as e:
      alert(f"Erreur inattendue lors de l'appel : {str(e)}")

    finally:
      # 6. Restauration de l'état du bouton
      self.btn_calculate.enabled = True
      self.btn_calculate.text = "Lancer le Calcul (EC3)"
      #self.loading_icon.visible = False

  def update_ui_results(self, data):
    """Met à jour les labels et Plotly avec le JSON de réponse API"""

    # Résultats numériques et statut
    status = data['status']
    self.lbl_status.text = f"État : {status['overall_status']}"
    self.lbl_ratio_flexion.text = f"Taux M : {status['critical_ratio_percent']}%"

    # Couleur du statut (Rigueur visuelle)
    self.lbl_status.foreground = "#28a745" if status['overall_status'] == "PASSED" else "#dc3545"

    # Résultats ULS détaillée
    uls = data['uls_results']
    # Tu peux ajouter ici des labels cachés pour afficher M_Ed vs M_Rd

    # --- Mise à jour de Plotly avec les données API ---
    plotly_data = data['plotly_data']
    x = plotly_data['x_axis_m']
    moment = plotly_data['moment_diagram_knm']
    m_rd = uls['m_rd_knm']

    # Configuration du graphique du Moment (type "Poche" de ferraillage)
    # Scatter plot rempli jusqu'à zéro
    scatter_m_ed = go.Scatter(
      x=x, y=moment,
      fill='tozeroy', # Remplissage sous la parabole
      name='Moment sollicitant M_Ed',
      line=dict(color='#007bff', width=2) # Bleu technique
    )

    # Ligne pointillée rouge pour la résistance
    line_m_rd = go.Scatter(
      x=[x[0], x[-1]], y=[m_rd, m_rd],
      mode='lines',
      name='Résistance plastique M_Rd',
      line=dict(color='#dc3545', dash='dash', width=2)
    )

    self.plot_moment.data = [scatter_m_ed, line_m_rd]
    self.plot_moment.layout.title = "Diagramme du Moment Fléchissant (kNm)"
    # Tu peux configurer le layout sombre ici pour matcher la maquette