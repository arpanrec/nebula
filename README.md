# Ansible Collection utilities (arpanrec.utilities)

## Prepare Dependencies

    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install pip-tools
    pip-compile --output-file=requirements.txt --resolver=backtracking requirements.in
    ```

## Install Dependencies

    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Run Playbook

    ```bash
    source venv/bin/activate
    ansible-playbook  --extra-vars=@/app/secrets/bootstrap/extra_vars.json site.yml --tags <Tags>
    ```

## License

`MIT`
