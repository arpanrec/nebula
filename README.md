# Ansible Collection utilities (arpanrec.utilities)

Collection of ansible roles to bootstrap a new server.

## Prepare Dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install pip pip-tools --upgrade
rm -f requirements.txt
pip-compile --output-file=requirements.txt requirements.in --upgrade --no-header --no-annotate
```

## Install Dependencies

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ansible-galaxy install -r requirements.yml --force
```

## Run Playbook

```bash
source .venv/bin/activate
ansible-playbook  --extra-vars=@/app/secrets/bootstrap/extra_vars.json site.yml --tags <Tags>
```

## License

`MIT`
