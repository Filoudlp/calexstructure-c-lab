from ._anvil_designer import beam_cmTemplate
from anvil import *

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go

class beam_cm(beam_cmTemplate):
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
      # Charge
    self.row_ned = RowItem("Ned", editable=True)
    self.row_ved = RowItem("Ved", editable=True)
    self.row_med = RowItem("Med", editable=True)

      # Material
    self.row_fy = RowItem("fy", editable=True)

    self.card_data.add_input(self.row_ned)
    self.card_data.add_input(self.row_ved)
    self.card_data.add_input(self.row_med)

    # --- Params avancés (cachés par défaut) ---
      # Section
    title_sec = Label(text="Section", bold=True, \
      underline=True,italic=True)
    self.row_A = RowItem(
      "A",
      editable=True,
      row_type="param",
    )
    self.row_Avy = RowItem(
      "Avy",
      editable=True,
      row_type="param",
    )
    self.row_Avz = RowItem(
      "Avz",
      editable=True,
      row_type="param",
    )
    self.row_Wy = RowItem(
      "Wy",
      editable=True,
      row_type="param",
    )
    self.row_Wz = RowItem(
      "Wz",
      editable=True,
      row_type="param",
    )
    self.row_Iy = RowItem(
      "Iy",
      editable=True,
      row_type="param",
    )
    self.row_Iz = RowItem(
      "Iz",
      editable=True,
      row_type="param",
    )

    self.card_data.add_param(title_sec)
    self.card_data.add_param(self.row_A)
    self.card_data.add_param(self.row_Avy)
    self.card_data.add_param(self.row_Avz)
    self.card_data.add_param(self.row_Wy)
    self.card_data.add_param(self.row_Wz)
    self.card_data.add_param(self.row_Iy)
    self.card_data.add_param(self.row_Iz)
    
      # Material
    self.row_E = RowItem(
      "E",
      editable=True,
      row_type="param",
    )
    
    self.card_data.add_param(self.row_E)
      # Coef
    self.row_gm0 = RowItem(
      "γM0",
      editable=True,
      row_type="param",
    )

    self.row_gm1 = RowItem(
      "γM1",
      editable=True,
      row_type="param",
    )

    self.row_gm2 = RowItem(
      "γM2",
      editable=True,
      row_type="param",
    )

    self.row_alpha = RowItem(
      "α",
      editable=True,
      row_type="param",
    )

    self.row_beta = RowItem(
      "β",
      editable=True,
      row_type="param",
    )
    
    self.card_data.add_param(self.row_gm0)
    self.card_data.add_param(self.row_gm1)
    self.card_data.add_param(self.row_gm2)
    self.card_data.add_param(self.row_alpha)
    self.card_data.add_param(self.row_beta)

    # Lateral buckling

    # ??

    self.cp = ColumnPanel()
    self.content_panel.add_component(self.cp)
    self.cp.add_component(self.card_data)