from ._anvil_designer import slab_baTemplate
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

from .....composant.BlockCard import BlockCard
from .....composant.RowItem import RowItem
from .....composant.RowItemDdm import RowItemDdm
from .....composant.RowItemChbx import RowItemChbx
from .....composant.RowPlot import RowPlot

from ..... import norme
from plotly import graph_objs as go


class slab_ba(slab_baTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # ==========================================================
    # BLOC 1 : DONNÉES D'ENTRÉE
    # ==========================================================
    self.card_data = BlockCard(
      title="Données — Massif",
      header_color="input",  # jaune
    )

    # --- Inputs principaux (toujours visibles) ---
    # Section
    self.row_b = RowItem("b", editable=True)
    self.row_h = RowItem("h", editable=True)
    self.row_L = RowItem("L", editable=True)
    self.row_hp = RowItem("h", editable=True)

    self.card_data.add_input(self.row_b)
    self.card_data.add_input(self.row_h)
    self.card_data.add_input(self.row_hp)
    self.card_data.add_input(self.row_L)

    # Materiaux
    self.row_fck = RowItem("fck", editable=True)
    self.row_fyk = RowItem("fyk", editable=True)

    self.card_data.add_input(self.row_fck)
    self.card_data.add_input(self.row_fyk)

    # Effort
    self.row_ned = RowItem("Ned", editable=True)

    self.card_data.add_input(self.row_ned)

    # Checkbox d and d'
    self.chk_bx_d = RowItemChbx(
      name_lbl="", name_chbx="d = 0.9 h", on_checked=self.chk_bx_d
    )

    self.chk_bx_dp = RowItemChbx(
      name_lbl="", name_chbx="d' = 0.1 h", on_checked=self.chk_bx_dp
    )
    self.gp1 = GridPanel()

    self.card_data.add_input(self.gp1)

    self.gp1.add_component(self.chk_bx_d, row="A", col_xs=0, width_xs=6)
    self.gp1.add_component(self.chk_bx_dp, row="A", col_xs=6, width_xs=6)

    self.lbl_way = Label(text="Méthode", bold=True, underline=True)

    self.card_data.add_input(self.lbl_way)

    self.chk_way1 = RowItemChbx(
      name_lbl="", name_chbx="Bielle/Tirant centré", on_checked=self.on_chk_way1
    )

    self.chk_way1.checked = True

    self.chk_way2 = RowItemChbx(
      name_lbl="", name_chbx="Bielle/Tirant excentré", on_checked=self.on_chk_way2
    )

    self.chk_way3 = RowItemChbx(
      name_lbl="", name_chbx="Réseaux d'état", on_checked=self.on_chk_way3
    )

    self.btn_help = Button(icon="fa:question-circle")
    self.btn_help.set_event_handler("click", self.btn_help_click)
    self.gp2 = GridPanel()

    self.card_data.add_input(self.gp2)

    self.gp2.add_component(self.chk_way1, row="A", col_xs=0, width_xs=4)
    self.gp2.add_component(self.chk_way2, row="A", col_xs=0, width_xs=4)
    self.gp2.add_component(self.chk_way3, row="A", col_xs=0, width_xs=4)
    self.gp2.add_component(self.btn_help, row="A", col_xs=0, width_xs=2)

    # --- Params avancés (cachés par défaut) ---
    self.row_gc = RowItem("γc", editable=True, row_type="param")

    self.row_gs = RowItem("γs", editable=True, row_type="param")

    self.row_acc = RowItem("αcc", editable=True, row_type="param")

    self.row_d = RowItem("d", editable=True, row_type="param")

    self.row_dp = RowItem("d'", editable=True, row_type="param")

    self.card_data.add_param(self.row_gc)
    self.card_data.add_param(self.row_gs)
    self.card_data.add_param(self.row_acc)
    self.card_data.add_param(self.row_d)
    self.card_data.add_param(self.row_dp)

    self.cp = ColumnPanel()
    self.content_panel.add_component(self.cp)
    self.cp.add_component(self.card_data)

  def btn_help_click(self, **event_args):
    """Quand on clique sur le bouton"""
    alert(
      """Bielle/Tirant centrée : explication \nBielle/Tirant excentré : explication \nMéthode réseau d'état : explication \n"""
    )

  def chk_bx_d(self, **event_args):
    if self.chk_bx_d.checked:
      self.chk_bx_d.chkbx_value = "d = O.9 h"
    else:
      self.chk_bx_d.chkbx_value = "d ≠ O.9 h"

  def chk_bx_dp(self, **event_args):
    if self.chk_bx_dp.checked:
      self.chk_bx_dp.chkbx_value = "d' = O.1 h"
    else:
      self.chk_bx_dp.chkbx_value = "d' ≠ O.1 h"

  def on_chk_way1(self, **event_args):
    if self.chk_way1.checked:
      self.row_hp.visible = False
      self.chk_way2.checked = False
      self.chk_way3.checked = False

  def on_chk_way2(self, **event_args):
    pass

  def on_chk_way3(self, **event_args):
    if self.chk_way3.checked:
      self.row_hp.visible = False
      self.chk_way1.checked = False
      self.chk_way2.checked = False
