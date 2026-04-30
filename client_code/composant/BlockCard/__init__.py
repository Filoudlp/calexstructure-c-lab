from ._anvil_designer import BlockCardTemplate
from anvil import *

class BlockCard(BlockCardTemplate):
  def __init__(self, title="Bloc", header_color="input", **properties):
    self.init_components(**properties)

    # Header
    self.lbl_title.text = title
    if header_color == "input":
      self.flow_panel_1.role = "block-header"
    elif header_color == "output":
      self.flow_panel_1.role = "block-header-blue"
      self.toggle_icon_button_1.visible = False

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

  def clear_param(self):
    """Vide rslt_panel avant un recalcul."""
    self.params_panel.clear()

  def add_result(self, row_component):
    """Ajoute une ligne dans rslt_panel."""
    self.rslt_panel.add_component(row_component)
  
  def clear_results(self):
    """Vide rslt_panel avant un recalcul."""
    self.rslt_panel.clear()

    # Any code you write here will run before the form opens.
    
    
