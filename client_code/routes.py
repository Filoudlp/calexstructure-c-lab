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
class BACompressionFrofaitaireRoute(Route):
  path = "/ba_compression_forfaitaire"
  form = 'norme.EC2.sollicitation.compression_forfaitaire_ba'
  
class BACompressioneRoute(Route):
  path = "/ba_compression"
  form = 'norme.EC2.sollicitation.compression_ba'

class BAShearRoute(Route):
  path = "/ba_shear"
  form = 'norme.EC2.sollicitation.shear_cm'

class BABendingRoute(Route):
  path = "/ba_bending"
  form = 'norme.EC2.sollicitation.bending_ba'

class BAMassifRoute(Route):
  path = "/ba_massif"
  form = 'norme.EC2.Xlmt.massif_ba'

class BAMassifRoute(Route):
  path = "/ba_column"
  form = 'norme.EC2.Xlmt.column_ba'

#======
#= CM =
#======
class PouCMRoute(Route):
  path = "/cm_beam"
  form = 'norme.EC3.Xlmt.beam_cm'
  
class ColCMRoute(Route):
  path = "/cm_Column"
  form = 'norme.EC3.Xlmt.column_cm'

class CMCompressionRoute(Route): # OK
  path = "/cm_compression"
  form = 'norme.EC3.sollicitation.compression_cm'

class CMShearRoute(Route):
  path = "/cm_shear"
  form = 'norme.EC3.sollicitation.shear_cm'

class CMBendingRoute(Route):
  path = "/cm_bending"
  form = 'norme.EC3.sollicitation.bending_cm'

class CMComposedBendingRoute(Route):
  path = "/cm_composed_bending"
  form = 'norme.EC3.sollicitation.composed_bending_cm'

class CMBoltRoute(Route):
  path = "/cm_bolt"
  form = 'norme.EC3.sollicitation.bolt_cm'

class CMWeldingRoute(Route):
  path = "/cm_welding"
  form = 'norme.EC3.sollicitation.welding_cm'

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