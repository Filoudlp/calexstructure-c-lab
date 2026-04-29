from ._anvil_designer import compression_oldTemplate
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
from plotly import graph_objs as go

from ..... import norme

class compression_old(compression_oldTemplate):
  # Statut : OK without buckling
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

    self.rslt_cm_1.lbl_elu_worst_verif.visible = False

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
    fy = self.materiaux_cm_1.steel_grade_ddm.selected_value[0][1]
    payload = {
      "fy": float(fy[1:]),
      "gamma_m0": float(self.option_avancer_cm_1.txb_gamma_m0.text),
      "A": float(self.geometrie_pou_1.txb_A.text),
      "load": norme.convert_unit(float(self.effort_normal_1.txb_N.text), "kN", "N"),
    }
    response = norme.api_call(API_URL, payload)
    
    formula = response["nc_rd"]["formula"]
    formula_val = response["nc_rd"]["formula_values"]
    ref = response["nc_rd"]["ref"]
    nc_rd = norme.convert_unit(response["nc_rd"]["result"], "N", "kN")
    verif = response["verif"]["formula_values"]
    verif_ref = response["verif"]["ref"]
    ned = float(self.effort_normal_1.txb_N.text)

    self.lbl_formula.text = formula
    self.lbl_formula_values.text = formula_val
    self.lbl_ref.text = f"{ref}\n"
    self.lbl_verif.text = verif
    self.lbl_verif_ref.text = verif_ref

    self.rslt_cm_1.lbl_elu_percent.text = f"Taux : {ned / nc_rd * 100:.2f} %"

    # Valeur à afficher
    pourcentage = response["verif"]["result"] * 100
    
    # Couleur conditionnelle
    couleur = 'green' if pourcentage < 100 else 'red'
    
    # Gérer le cas > 100% (on plafonne visuellement à 100)
    valeur_affichee = min(pourcentage, 100)
    reste = 100 - valeur_affichee
    
    fig = go.Figure(data=[go.Pie(
      values=[valeur_affichee, reste],
      labels=['Atteint', 'Restant'],
      hole=0.6,
      marker=dict(colors=[couleur, '#E8E8E8']),
      textinfo='none',            # Pas de texte sur les parts
      hoverinfo='skip',           # Pas de survol
      sort=False,                 # Garde l'ordre
      direction='clockwise',
      rotation=0,
      showlegend=False
    )])
    
    fig.update_layout(
      annotations=[dict(
        text=f'<b>{pourcentage:.2f}%</b>',
        x=0.5, y=0.5,
        font=dict(size=40, color=couleur),
        showarrow=False
      )],
      margin=dict(t=20, b=20, l=20, r=20)
    )
    self.rslt_cm_1.plt_elu.figure = fig

    self.btn_detailed.enabled = True

  @handle("btn_detailed", "click")
  def btn_detailed_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_detailed.icon == "fa:arrow-right":
      self.btn_detailed.icon = "fa:arrow-left"
      self.btn_hide.icon = "fa:arrow-left"
      self.layout.fun_show_sidesheet(True)
    else:
      self.btn_detailed.icon = "fa:arrow-right"
      self.btn_hide.icon = "fa:arrow-right"
      self.layout.fun_show_sidesheet(True)

  @handle("btn_hide", "click")
  def btn_hide_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.btn_detailed_click()
