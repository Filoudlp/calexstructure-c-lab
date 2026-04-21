from ._anvil_designer import compressionTemplate
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

from ..... import norme

class compression(compressionTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.geometrie_pou_1.txb_length.visible = False
    self.geometrie_pou_1.lbl_length.visible = False

    self.geometrie_pou_1.txb_b.visible = False
    self.geometrie_pou_1.lbl_b.visible = False

    self.geometrie_pou_1.txb_h.visible = False
    self.geometrie_pou_1.lbl_h.visible = False

    self.geometrie_pou_1.txb_e.visible = False
    self.geometrie_pou_1.lbl_e.visible = False

    self.geometrie_pou_1.txb_Av.visible = False
    self.geometrie_pou_1.lbl_av.visible = False

    self.geometrie_pou_1.txb_Iy.visible = False
    self.geometrie_pou_1.lbl_Iy.visible = False

    self.geometrie_pou_1.txb_Iz.visible = False
    self.geometrie_pou_1.lbl_Iz.visible = False

    self.geometrie_pou_1.txb_Wy.visible = False
    self.geometrie_pou_1.lbl_Wy.visible = False

    self.geometrie_pou_1.txb_Wz.visible = False
    self.geometrie_pou_1.lbl_Wz.visible = False

    self.rslt_cm_1.lbl_els.visible = False
    self.rslt_cm_1.lbl_els_percent.visible = False
    self.rslt_cm_1.lbl_els_worst_verif.visible = False
    self.rslt_cm_1.plt_els.visible = False

    self.option_avancer_cm_1.lbl_alpha.visible = False
    self.option_avancer_cm_1.lbl_beta.visible = False
    self.option_avancer_cm_1.lbl_els_lim.visible = False
    self.option_avancer_cm_1.lbl_alpha_rhs.visible = False
    self.option_avancer_cm_1.lbl_alpha_chs.visible = False
    self.option_avancer_cm_1.lbl_alpha_i_h.visible = False
    self.option_avancer_cm_1.lbl_beta_rhs.visible = False
    self.option_avancer_cm_1.lbl_beta_chs.visible = False
    self.option_avancer_cm_1.lbl_beta_i_h.visible = False
    self.option_avancer_cm_1.txb_beta_chs.visible = False
    self.option_avancer_cm_1.txb_beta_rhs_shs.visible = False
    self.option_avancer_cm_1.txb_beta_i_h.visible = False
    self.option_avancer_cm_1.txb_alpha_chs.visible = False
    self.option_avancer_cm_1.txb_alpha_rhs_shs.visible = False
    self.option_avancer_cm_1.txb_alpha_i_h.visible = False
    self.option_avancer_cm_1.txb_els_lim.visible = False
    self.option_avancer_cm_1.lbl_gamma_m1.visible = False
    self.option_avancer_cm_1.lbl_gamma_m2.visible = False
    self.option_avancer_cm_1.txb_gamma_m1.visible = False
    self.option_avancer_cm_1.txb_gamma_m2.visible = False

    self.btn_optional_click()
    self.layout.fun_show_sidesheet(False)

    # Any code you write here will run before the form opens.

  @handle("btn_optional", "click")
  def btn_optional_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optional.icon == "fa:arrow-down":
      self.btn_optional.icon = "fa:arrow-right"
      self.option_avancer_cm_1.visible = False
    else:
      self.btn_optional.icon = "fa:arrow-down"
      self.option_avancer_cm_1.visible = True

  @handle("btn_calc", "click")
  def btn_calc_click(self, **event_args):
    """This method is called when the component is clicked."""
    API_URL = "/api/cm_compression_calc"
    payload = {
      "fy": float(self.materiaux_cm_1.steel_grade_ddm.selected_value),
      "gamma_m0": float(self.option_avancer_cm_1.txb_gamma_m0.text),
      "A": float(self.geo_def_1.txb_A.text),
      "load": float(self.effort_normal_1.txb_load.text),
    }
    response = norme.api_call(API_URL, payload)
