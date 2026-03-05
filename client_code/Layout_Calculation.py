from ._anvil_designer import Layout_CalculationTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

from .StripePricing import StripePricing

from anvil import designer


class Layout_Calculation(Layout_CalculationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    # Any code you write here will run before the form opens.


