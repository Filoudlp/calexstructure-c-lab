from ._anvil_designer import geometrie_POUTemplate
from anvil import handle

class geometrie_POU(geometrie_POUTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.btn_optionnal_click()

    # Any code you write here will run before the form opens.

  @handle("btn_optionnal", "click")
  def btn_optionnal_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.btn_optionnal.icon == "fa:arrow-down":
      self.btn_optionnal.icon = "fa:arrow-right"
      self.box_optional.visible = False
    else:
      self.btn_optionnal.icon = "fa:arrow-down"
      self.box_optional.visible = True