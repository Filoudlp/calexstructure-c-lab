# routes.py
from routing.router import Route

#=========
#= Admin =
#=========
class IndexRoute(Route): # OK
  path = "/"
  form = "Landing_LoginPage" # Ok

class AcountManagement(Route): # OK
  path = "/Account"
  form = "AccountManagement"
#========
#= Bois =
#========
  
#======
#= BA =
#======
class CMCompressionRoute(Route): # OK
  path = "/cm_compression"
  form = 'norme.EC3.sollicitation.compression_cm'

class CMShearRoute(Route):
  path = "/cm_shear"
  form = 'norme.EC3.sollicitation.shear_cm'

class BABendingRoute(Route):
  path = "/ba_bending"
  form = 'norme.EC2.sollicitation.bending_ba'

#======
#= CM =
#======
class PouCMRoute(Route):
  path = "/poutre_cm"
  form = 'norme.EC3.Xlmt.Poutre_CM'

class CMCompressionRoute(Route): # OK
  path = "/cm_compression"
  form = 'norme.EC3.sollicitation.compression_cm'

class CMShearRoute(Route):
  path = "/cm_shear"
  form = 'norme.EC3.sollicitation.shear_cm'

class CMBendingRoute(Route):
  path = "/cm_bending"
  form = 'norme.EC3.sollicitation.bending_cm'

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