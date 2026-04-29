from ._anvil_designer import BlockCardTemplate
from anvil import *
import anvil.server
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class BlockCard(BlockCardTemplate):
  def __init__(self, title="Bloc", header_color="yellow", **properties):
    self.init_components(**properties)

    # Header
    self.lbl_title.text = title
    # Au lieu de header_color en hex, utilise des roles
    #if header_color == "blue":
    #  self.flow_panel_1.role = "block-header-blue"
    #else:
    #  self.flow_panel_1.role = "block-header"
    self.flow_panel_1.background = header_color

    self.params_panel.visible = False

    # Params cachés par défaut
    self.params_panel.visible = False

    # Vider les contenus statiques (text_2, etc. — à supprimer du designer)
    self.inputs_panel.clear()
    self.rslt_panel.clear()

    # Toggle params
    self.toggle_icon_button_1.set_event_handler(
      'click', self.toggle_params
    )

  def toggle_params(self, **event_args):
    self.params_panel.visible = not self.params_panel.visible
    self.toggle_icon_button_1.icon = "mi:arrow_circle_up" \
    if self.toggle_icon_button_1.selected else "mi:arrow_circle_down"

# ----- API publique pour ajouter des lignes -----

  def add_input(self, row_component):
    """Ajoute une ligne dans inputs_panel."""
    self.inputs_panel.add_component(row_component)
  
  def add_param(self, row_component):
    """Ajoute une ligne dans params_panel."""
    self.params_panel.add_component(row_component)

    def add_result(self, row_component):
      """Ajoute une ligne dans rslt_panel."""
      self.rslt_panel.add_component(row_component)
  
  def clear_results(self):
    """Vide rslt_panel avant un recalcul."""
    self.rslt_panel.clear()

    # Any code you write here will run before the form opens.
    
    
