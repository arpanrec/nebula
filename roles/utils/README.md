# ansible-role-utils

Helper Ansible Roles

## TLS Certificate `tlscert.yml`

```yaml
- name: "Include tasks from set_secret_vault_env"
    import_role:
    name: arpanrec.utils
    tasks_from: tlscert.yml
```

## Test

```yaml
git clone git@github.com:arpanrec/ansible-role-utils.git arpanrec.utils
cd arpanrec.utils
python3 -m pip install --user --upgrade pip
python3 -m pip install --user --upgrade wheel setuptools
python3 -m pip install --user --upgrade virtualenv
virtualenv --python $(readlink -f $(which python3)) venv
source venv/bin/activate
venv/bin/python3 -m pip install -r requirements.txt --upgrade
molecule test
```
