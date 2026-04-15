from routing import router
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import user_has_subscription

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

def say_hello():
  print("Hello, world")

def check_connected():
  if anvil.users.get_user():
    print("Connected my reuf")
  if user_has_subscription:
    print("Has subscription")