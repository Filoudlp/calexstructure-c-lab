# routes.py
from routing.router import Route

class IndexRoute(Route):
  path = "/"
  form = "Landing_LoginPage"
#========
#= Bois =
#========
  
#======
#= BA =
#======

#======
#= CM =
#======
class PouCMRoute(Route):
  path = "/poutre_cm"
  form = 'norme.EC3.Xlmt.Poutre_CM'

class CMCompressionRoute(Route):
  path = "/cm_compression"
  form = 'norme.EC3.sollicitation.compression'

#=======
#= RDM =
#=======

class DeflectionRoute(Route):
  path = "/deflection"
  form = 'norme.general.Unit.deflection_POU'

#========
#= tool =
#========

class ToolListRoute(Route):
  path = "/tools_list"
  form = 'norme.tools_list'