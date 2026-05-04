from ._anvil_designer import bending_baTemplate
from anvil import *

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go


class bending_ba(bending_baTemplate):
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
    self.row_b = RowItem("b", editable=True)
    self.row_h = RowItem("h", editable=True)
    self.row_fck = RowItem("fck", editable=True)
    self.row_fyk = RowItem("fyk", editable=True)
    self.row_med = RowItem("Med", editable=True)
    
    self.card_data.add_input(self.row_b)
    self.card_data.add_input(self.row_h)
    self.card_data.add_input(self.row_fck)
    self.card_data.add_input(self.row_fyk)
    self.card_data.add_input(self.row_med)

    # --- Params avancés (cachés par défaut) ---
    self.row_gc = RowItem(
      "γc",
      editable=True,
      row_type = "param"
    )

    self.row_gs = RowItem(
      "γs",
      editable=True,
      row_type = "param"
    )

    self.row_acc = RowItem(
      "αcc",
      editable=True,
      row_type = "param"
    )

    self.row_d = RowItem(
      "d",
      editable=True,
      row_type = "param"
    )
    
    self.row_dp = RowItem(
      "d'",
      editable=True,
      row_type = "param"
    )

    self.row_est = RowItem(
      "εst",
      editable=True,
      row_type = "param"
    )
    
    self.row_eud = RowItem(
      "εud",
      editable=True,
      row_type = "param"
    )
    
    self.row_ecu = RowItem(
      "εcu",
      editable=True,
      row_type = "param"
    )
    self.row_es = RowItem(
      "Es",
      editable=True,
      row_type = "param"
    )
    self.row_lambda = RowItem(
      "λ",
      editable=True,
      row_type = "param"
    )
    
    self.row_eta = RowItem(
      "η",
      editable=True,
      row_type = "param"
    )

    self.chk_bx = RowItemChbx(
      name_lbl = "d = O.9"
    )

    component.append(self.row_gc)
    component.append(self.row_gs)
    component.append(self.row_acc)
    component.append(self.row_d)
    component.append(self.row_dp)
    component.append(self.row_est)
    component.append(self.row_eud)
    component.append(self.row_ecu)
    component.append(self.row_es)
    component.append(self.row_lambda)
    component.append(self.row_eta)

    for row in component:
      self.card_data.add_param(row)

    self.cp = ColumnPanel()
    self.content_panel.add_component(self.cp)
    self.cp.add_component(self.card_data)