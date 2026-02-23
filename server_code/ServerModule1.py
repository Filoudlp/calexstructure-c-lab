import anvil.email
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def calculer_section(inputs):
  b = inputs['b'] / 100  # cm -> m
  h = inputs['h'] / 100
  fyk = inputs['fyk']
  ned = inputs['ned']
  gamma_s = inputs['gamma_s']

  fyd = fyk / gamma_s
  section = b * h
  sigma = ned / section  # kN/m²

  return {
    'fyd': round(fyd, 2),
    'section': round(section, 4),
    'sigma': round(sigma, 2),
  }