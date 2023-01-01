from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.utils.vars import load_extra_vars
from ansible.template import Templar


class InventoryModule(BaseInventoryPlugin):

  NAME = 'vault_inv'

  def verify_file(self, path):
    ''' return true/false if this is possibly a valid file for this plugin to consume '''
    valid = False
    if super(InventoryModule, self).verify_file(path):
      # base class verifies that file exists and is readable by current user
      if path.endswith(('virtualbox.yaml', 'virtualbox.yml', 'vbox.yaml', 'vbox.yml')):
        valid = True
    self.display.vvvv("34235252" + path)
    return True

  def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path, cache)
    self.display.vvvv("asfhaskjhiu" + path)
    self.inventory.add_host('name11')
    self.inventory.set_variable('name11', 'ansible_host', 'dlkdslddkl')
    self.inventory.set_variable('name11', 'pathfilecon', open(path).read())

    self.loader = loader
    self.inventory = inventory
    self.templar = Templar(loader=loader)
    self._vars = load_extra_vars(loader)
