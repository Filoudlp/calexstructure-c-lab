from ._anvil_designer import effort_CMTemplate
from anvil import handle

class effort_CM(effort_CMTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
