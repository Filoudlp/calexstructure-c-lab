# routes.py
from routing.router import Route

class IndexRoute(Route):
  path = "/"
  form = "Landing_LoginPage"

class PouCMRoute(Route):
  path = "/poutre_cm"
  form = 'norme.EC3.Xlmt.Poutre_CM'

class DeflectionRoute(Route):
  path = "/deflection"
  form = 'norme.general.Unit.deflection_POU'