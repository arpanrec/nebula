# Ansible Role: Setup Hashicorp Vault

An ansible Playbook to install [HashiCorp Vault](https://www.vaultproject.io) with file backend on [docker](https://hub.docker.com/_/vault)

## Playbook Variables

`rv_hashicorp_vault_access_hostname`

- description: The hostname of the Vault server, a TLS certificate will be issued to this name.
- required: no
- default: localhost
- type: str

`rv_hashicorp_vault_os_data_directory`

- description: The directory where Vault data is stored.
- required: no
- default: /vault
- type: str

Post Install check if vault is up

`rv_hashicorp_vault_post_install_action_api_addr`

- description: The address of the Vault server from native host.
- required: no
- default: <https://localhost:8200>
- type: str

`rv_hashicorp_vault_post_install_action_initialize`

- description: Initialize the Vault server if not already initialized.
- required: no
- default: no
- type: boolean
- required_vars

  `rv_hashicorp_vault_post_install_action_initialize_share`

  - description: "Number of key shares."
  - required: no
  - default: 5
  - type: int

  `rv_hashicorp_vault_post_install_action_initialize_threshold`

  - description: "Number of key minimum shares."
  - required: no
  - default: 3
  - type: int

  `rv_hashicorp_vault_post_install_action_initialize_secrets_directory`

  - description: "Root Token and unseal keys will be stored in this directory."
  - required: no
  - default: "{{  rv_hashicorp_vault_os_data_directory  }}/init_secrets"
  - type: str

Setup Basic cron based auto-unseal

`rv_hashicorp_vault_post_install_action_setup_auto_unseal_cron`

- description: Setup cron job to run auto-unseal.
- required: no
- default: no
- type: boolean
- required_vars

  `rv_hashicorp_vault_post_install_action_setup_auto_unseal_cron_dir`

  - description: "Cron Script and unseal keys will be stored here"
  - required: no
  - default: "{{ rv_hashicorp_vault_os_data_directory }}/unseal_corn"
  - type: str

  `rv_hashicorp_vault_post_install_action_setup_unseal_keys`

  - description: "Vault unseal keys"
  - required: yes
  - type: list[str]

## Testing

Prerequisite: `docker`, `python3-pip`, `virtualenv`

```bash
git clone git@github.com:arpanrec/ansible-play-hashicorp-vault.git arpanrec.setup_hashicorp_vault

cd arpanrec.setup_hashicorp_vault

pip install --user --upgrade virtualenv

virtualenv venv

source venv/bin/activate

pip install -r requirements.txt

molecule test
```

## License

MIT
