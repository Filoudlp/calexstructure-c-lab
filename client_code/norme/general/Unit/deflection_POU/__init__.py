from ._anvil_designer import deflection_POUTemplate
from anvil import *
from routing import router
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from plotly import graph_objs as go

from ..... import norme


class deflection_POU(deflection_POUTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.layout.fun_show_sidesheet(False)

    # Any code you write here will run before the form opens.

  @handle("btn_calc", "click")
  def btn_calc_click(self, **event_args):
    """This method is called when the component is clicked."""
    API_URL = "/api/deflection_calc"
    payload = {
      "length": float(self.geo_def_1.txb_length.text),
      "E": float(self.sec_type_1.tbx_E.text),
      "b": float(self.geo_def_1.txb_b.text),
      "h": float(self.geo_def_1.txb_h.text),
      "A": float(self.geo_def_1.txb_A.text),
      "Iy": float(self.geo_def_1.txb_Iy.text),
      "Iz": float(self.geo_def_1.txb_Iz.text),
      "load": float(self.effort_def_1.txb_load.text),
    }
    response = norme.api_call(API_URL, payload)
    
    x = response["x"]
    m = response["M"]
    v = response["V"]
    n = response["N"]


    trace0 = go.Scatter(
      x = x,
      y = m,
      name = 'Bending moment',
      line = dict(
        color = ('rgb(0, 4, 255)'),
        width = 1)
    )
    trace1 = go.Scatter(
      x = x,
      y = v,
      name = 'Shear force',
      line = dict(
        color = ('rgb(255, 8, 0)'),
        width = 1)
    )
    trace2 = go.Scatter(
      x = x,
      y = n,
      name = 'normal force',
      line = dict(
        color = ('rgb(0, 255, 34)'),
        width = 1)
    )
    self.plot_cm_1.plot_1.data = [trace0, trace1, trace2]

    self.plot_cm_1.plot_1.layout = dict(title = 'Effort interne',
                 xaxis = dict(title = 'distance'),
                  yaxis = dict(title = 'Effort interne'),
    )

    self.btn_detailed.enabled = True
    
    index_N = n.index(max(n))
    index_V = v.index(max(v))
    index_M = m.index(min(m))

    self.lbl_Nmax_val.text =  f"x = {x[index_N]} N = {n[index_N]:2f}"
    self.lbl_Vmax_val.text =  f"x = {x[index_V]} V = {v[index_V]:2f}"
    self.lbl_Mmax_val.text =  f"x = {x[index_M]} M = {m[index_M]:2f}"
    #self.lbl_Nmax_val.text =  f"x = {x[index_N]} N = {n[index_N]}"
    
    

  @handle("btn_detailed", "click")
  def btn_detailed_click(self, **event_args):
    """This method is called when the button is clicked"""
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

    