from routing import router
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *

# This is a package.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from .. import Package1
#
#    Package1.say_hello()
#

#@anvil.server.route("/hello")
#def poutre_cm(**p):
#  open_form('norme.EC3.Xlmt.Poutre_CM') 

def check_connectednsub(var):
  if not anvil.users.get_user():
    print("not connected")
    user = anvil.users.login_with_form(allow_cancel=True, show_signup_option=True,
                                       allow_remembered=True, remember_by_default=False)
    if user:
      open_form(var)
      print("succeed")
    else:
      open_form('Landing_LoginPage')

  user = anvil.users.get_user()
  if user["subscription"] == "Abonnement C-Lab":
    print('bien ouej mon reuf')
  else:
    print("no subscription")
