from ._anvil_designer import compression_forfaitaire_baTemplate
from anvil import *

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go


class compression_forfaitaire_ba(compression_forfaitaire_baTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # ==========================================================
    # BLOC 1 : DONNÉES D'ENTRÉE
    # ==========================================================
    self.card_data = BlockCard(
      title="Données",
      header_color="input",  # jaune
    )

    # --- Inputs principaux (toujours visibles) ---
    # Section
    self.row_b = RowItem("b", editable=True)
    self.row_h = RowItem("h", editable=True)
    self.row_L = RowItem("L", editable=True)

    self.card_data.add_input(self.row_b)
    self.card_data.add_input(self.row_h)
    self.card_data.add_input(self.row_L)

    # Materiaux
    self.row_fck = RowItem("fck", editable=True)
    self.row_fyk = RowItem("fyk", editable=True)

    self.card_data.add_input(self.row_fck)
    self.card_data.add_input(self.row_fyk)

    # Effort
    self.row_as = RowItem(name = "As", editable=True)

    self.card_data.add_input(self.row_as)
    
    # Effort
    self.row_ned = RowItem("Ned", editable=True)

    self.card_data.add_input(self.row_ned)

    # Checkbox d and d'
    self.chk_bx_d = RowItemChbx(
      name_lbl="", name_chbx="d = 0.9 h", on_checked=self.chk_bx_d
    )
    self.gp1 = GridPanel()

    self.card_data.add_input(self.gp1)

    self.gp1.add_component(self.chk_bx_d, row="A", col_xs=0, width_xs=6)

    # --- Params avancés (cachés par défaut) ---
    self.row_gc = RowItem("γc", editable=True, row_type="param")

    self.row_gs = RowItem("γs", editable=True, row_type="param")

    self.row_acc = RowItem("αcc", editable=True, row_type="param")

    self.row_d = RowItem("d", editable=True, row_type="param")

    self.card_data.add_param(self.row_gc)
    self.card_data.add_param(self.row_gs)
    self.card_data.add_param(self.row_acc)
    self.card_data.add_param(self.row_d)

    self.content_panel.add_component(self.card_data)
    

    # ==========================================================
    # BLOC 2 : RÉSULTATS
    # ==========================================================
    self.card_results = BlockCard(
      title="Vérification Compression forfaitaire",
      header_color="output",  # bleu
    )
    geo = Label(text="Caractéristique géométrique", bold=True, underline=True)
    self.row_ac = RowItem(name = "Ac", editable=False, row_type="param")
    self.row_Iy = RowItem(name = "Iy", editable=False, row_type="param")
    self.row_Iz = RowItem(name = "Iz", editable=False, row_type="param")
    self.row_iy = RowItem(name = "iy", editable=False, row_type="param")
    self.row_iz = RowItem(name = "iz", editable=False, row_type="param")
    self.row_ly = RowItem(name = "λy", editable=False, row_type="param")
    self.row_lz = RowItem(name = "λz", editable=False, row_type="param")
    self.row_lmax = RowItem(name = "λmax", editable=False, row_type="param")

    verif = Label(text="Vérificaiton", bold=True, underline=True)

    self.card_results.add_param(geo)
    self.card_results.add_param(self.row_ac)
    self.card_results.add_param(self.row_Iy)
    self.card_results.add_param(self.row_Iz)
    self.card_results.add_param(self.row_iy)
    self.card_results.add_param(self.row_iz)
    self.card_results.add_param(self.row_ly)
    self.card_results.add_param(self.row_lz)
    self.card_results.add_param(self.row_lmax)
    
    self.card_results.add_param(verif)

    self.row_alpha = RowItem(name = "alpha", editable=False, row_type="param")
    self.row_kh = RowItem(name = "kh", editable=False, row_type="param")
    self.row_delta = RowItem(name = "delta", editable=False, row_type="param")
    self.row_roh = RowItem(name = "roh", editable=False, row_type="param")
    self.row_ks = RowItem(name = "ks", editable=False, row_type="param")

    self.card_results.add_param(self.row_alpha)
    self.card_results.add_param(self.row_kh)
    self.card_results.add_param(self.row_delta)
    self.card_results.add_param(self.row_roh)
    self.card_results.add_param(self.row_ks)

    self.row_nedmax = RowItem(name = "Ned,max", editable=False, row_type="param")

    self.card_results.add_result(self.row_nedmax)

    self.val = RowItem(name = "Ned < Ned,max", editable=False, row_type="param")

    self.card_results.add_result(self.val)

    self.card_results.toggle_button_visible = True
    
    self.content_panel.add_component(self.card_results)

  def chk_bx_d(self, **event_args):
    if self.chk_bx_d.checked:
      self.chk_bx_d.chkbx_value = "d = O.9 h"
    else:
      self.chk_bx_d.chkbx_value = "d ≠ O.9 h"
