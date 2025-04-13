from xml_rpc import XMLRPC_API, myprint
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

ODOO_BACKEND = 'http://localhost:8069'
ODOO_DB = 'Odoo'
ODOO_USER = 'admin'
ODOO_PASS = 'admin'

def main():
  client = XMLRPC_API(url=ODOO_BACKEND, db=ODOO_DB, username=ODOO_USER, password=ODOO_PASS)

  # Create
  id = client.create(model_name="zoo.creature", data_dict={"name": "Husky", "is_rare": False, "environment": "ground"})
  print("Created creature @ %d" % id)

  # Read
  myprint(client.read(model_name='zoo.creature', conditions=[], params={'fields': ['name', 'is_rare', 'environment']}), 'Zoo Creatures')

  # Update
  client.update(model_name="zoo.creature", id_list=[id], new_data_dict={"name": "Alaska", "is_rare": True})
  print("Updated creature @ %d" % id)

  # Read
  myprint(client.read(model_name='zoo.creature', conditions=[], params={'fields': ['name', 'is_rare', 'environment']}), 'Zoo Creatures')

  # Delete
  client.delete(model_name="zoo.creature", id_list=[id])
  print("Deleted creature @ %d" % id)

if __name__ == "__main__":
  main()