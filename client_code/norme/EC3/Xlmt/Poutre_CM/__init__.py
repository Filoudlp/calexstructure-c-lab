from ._anvil_designer import Poutre_CMTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.http
import json

from .....Layout_Calculation import Layout_Calculation
from ..... import norme

class Poutre_CM(Poutre_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    norme.check_connectednsub(var=self) 
    self.init_components(**properties)
    self.btn_optional_click()
    self.btn_detail_rslt_click()
    #

    # Any code you write here will run before the form opens.

  @handle("btn_calc", "click")
  def btn_calc_click(self, **event_args):
    """This method is called when the component is clicked."""
    #self.layout.fun_show_sidesheet(False)
    # Récupère les inputs depuis l'interface
    payload = {
      "section": self.geometrie_1.ddm_section.selected_value,    # "IPE 80"
      "length": self.geometrie_1.txb_length.text,         # mm
      "b": self.geometrie_1.txb_b.text,
      "h": self.geometrie_1.txb_h.text,
      "e": self.geometrie_1.txb_e.text,
      "A": self.geometrie_1.txb_A.text,
      "Avz": self.geometrie_1.txb_Av.text,
      "Iy": self.geometrie_1.txb_Iy.text,
      "Iz": self.geometrie_1.txb_Iz.text,
      "Wy": self.geometrie_1.txb_Wy.text,
      "Wz": self.geometrie_1.txb_Wz.text,
      "steel_class": self.geometrie_1.txb_steelclass.text,
      "material": self.materiaux_cm_1.steel_grade_ddm.selected_value[0][1],  # "S235"
      "N": self.effort_cm_2.txb_N.text,
      "Vy": self.effort_cm_2.txb_vy.text,
      "Vz": self.effort_cm_2.txb_vz.text,            # N
      "My": self.effort_cm_2.txb_my.text,   
      "Mz": self.effort_cm_2.txb_mz.text,   # N.mm
      "els_lim": self.option_avancer_cm_1.txb_els_lim.text,
      "gamma_m0": self.option_avancer_cm_1.txb_gamma_m0.text,
      "gamma_m1": self.option_avancer_cm_1.txb_gamma_m1.text,
      "gamma_m2": self.option_avancer_cm_1.txb_gamma_m2.text,
      "alpha_rhs_shs": self.option_avancer_cm_1.txb_alpha_rhs_shs.text, 
      "alpha_chs": self.option_avancer_cm_1.txb_alpha_chs.text,
      "alpha_i_h": self.option_avancer_cm_1.txb_alpha_i_h.text, 
      "beta_rhs_shs": self.option_avancer_cm_1.txb_beta_rhs_shs.text, 
      "beta_chs": self.option_avancer_cm_1.txb_beta_chs.text,
      "beta_i_h": self.option_avancer_cm_1.txb_beta_i_h.text, 
    }
    API_URL = "/api/pou_cm"
    response = norme.api_call(API_URL, payload)

  @handle("btn_optional", "click")
  def btn_optional_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optional.icon == "fa:arrow-down":
      self.btn_optional.icon = "fa:arrow-right"
      self.option_avancer_cm_1.visible = False
    else:
      self.btn_optional.icon = "fa:arrow-down"
      self.option_avancer_cm_1.visible = True

  @handle("btn_hide", "click")
  def btn_hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_detail_rslt.icon == "fa:arrow-right":
      self.btn_detail_rslt.icon = "fa:arrow-left"
      self.btn_hide.icon = "fa:arrow-left"
      self.layout.fun_show_sidesheet(False)
    else:
      self.btn_detail_rslt.icon = "fa:arrow-right"
      self.btn_hide.icon = "fa:arrow-right"
      self.layout.fun_show_sidesheet(True)

  @handle("btn_detail_rslt", "click")
  def btn_detail_rslt_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.btn_hide_click()
    
