from ._anvil_designer import Form2Template
from anvil import *

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go


class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
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
    self.row_b = RowItem("b", value=200, editable=True)
    self.row_h = RowItem("h", value=500, editable=True)
    self.row_fck = RowItem("fck", value=30, editable=True)
    self.row_fyk = RowItem("fyk", value=500, editable=True)
    self.row_med = RowItem("Med", value=10, editable=True)
    
    self.card_data.add_input(self.row_b)
    self.card_data.add_input(self.row_h)
    self.card_data.add_input(self.row_fck)
    self.card_data.add_input(self.row_fyk)
    self.card_data.add_input(self.row_med)

    # --- Params avancés (cachés par défaut) ---
    self.row_gc = RowItem(
      name="γc",
      editable=True,
      row_type = "param"
    )

    self.row_gs = RowItem(
      name="γs",
      editable=True,
      row_type = "param"
    )

    component.append(self.row_gc)
    component.append(self.row_gs)

    for row in component:
      self.card_data.add_param(row)
