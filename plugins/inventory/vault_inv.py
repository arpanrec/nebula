from __future__ import absolute_import, division, print_function
from yaml.loader import SafeLoader
import yaml
from ansible.utils.vars import load_extra_vars
from ansible.plugins.inventory import BaseInventoryPlugin
import hvac
import os

__metaclass__ = type

DOCUMENTATION = r"""
  name: vault_inv
  short_description: Ansible dynamic inventory from hashicorp Vault.
  requirements:
      - python >= 3
      - hvac >= 1.0.2
  description: Reads inventories from the HashiCorp Vault KV engine.
  options:
    plugin:
      description: The name of this plugin, it should always be set to 'vault_inv' for this plugin to recognize it as it's own.
      type: str
      required: true
      choices:
        - vault_inv
        - arpanrec.utilities.vault_inv
    hostname:
      description: The URL of the hashicorp vault.
      type: str
      required: false
      default: http://localhost:8200
    mount_point:
      description: Name of KV secret engine.
      type: str
      required: true
    path:
      description: Path to secrets.
      type: str
      required: false
      default: "/"
    token:
      description:
        - Vault Token.
        - Environment variable `VAULT_TOKEN` has more priority
      type: str
      required: true
    verify:
      description:
        - Verify Vault HTTPS Connection
        - False to disable verification
        - Environment variable `VAULT_CAPATH` < `VAULT_CACERT`, this comes in to effect if `verify` is not provided.
      required: false
      default: true
    cert:
      description:
        - Mutual Client Certificate
        - Environment variable `VAULT_CLIENT_CERT` and `VAULT_CLIENT_KEY`
      type: tuple
      required: false
"""

EXAMPLES = """
# inventory.yml
plugin: arpanrec.utilities.vault_inv
host: http://localhost:8200
"""


class VaultInventoryModule(BaseInventoryPlugin):

  NAME = "vault_inv"

  __inventory_config = {}

  def verify_file(self, path):
    """return true/false if this is possibly a valid file for this plugin to consume"""
    valid = False
    if super(VaultInventoryModule, self).verify_file(path):
      with open(path, encoding="utf-8") as inventory_file_stream:
        self.__inventory_config = yaml.load(
            inventory_file_stream, Loader=SafeLoader
        )
        self.display.vvv("Ansible Inventory Loaded from: " + path)
        self.display.vvvv(
            "Ansible Inventory Information: " + self.__inventory_config
        )
        valid = True
    return valid

  def parse(self, inventory, loader, path, cache=True):
    super(VaultInventoryModule, self).parse(inventory, loader, path, cache)
    self.display.vvvv("Adding Localhost")
    self.inventory.add_host("localhost")
    self.inventory.set_variable("localhost", "ansible_connection", "local")
    self.inventory.set_variable(
        "localhost", "ansible_python_interpreter", "/usr/bin/env python3"
    )

    self.display.vvvv("Parsing Vault inventory : " + path)
    self.inventory = inventory
    self._vars = load_extra_vars(loader)

  @staticmethod
  def get_from_vault(
      hostname: str = "http://localhost:8200",
      mount_point: str = "secret",
      path: str = "/",
      token: str = None,
      verify: bool = False,
      cert: tuple = None,
  ) -> None:
    vault_client = hvac.Client(
        hostname,
        token=os.environ.get("VAULT_TOKEN", token),
        verify=verify,
        cert=cert,
    )
    print(vault_client.is_authenticated())
    secret_version_response = vault_client.secrets.kv.v2.read_secret_version(
        path=path, mount_point=mount_point
    )
    print(secret_version_response)
