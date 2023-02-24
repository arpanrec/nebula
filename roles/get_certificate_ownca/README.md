# Ansible Role: Get Certificate (arpanrec.utilities.get_certificate_ownca)

Get Server or Client certificate.

## Variables

- `rv_getcert_ownca_private_key_content`

  - Description:
    - Private Key as String of OWNCA
    - Mutually exclusive with `rv_getcert_ownca_private_key_path`
  - Type: `str`
  - Required: `true`

- `rv_getcert_ownca_private_key_path`

  - Description:
    - Private Key path of OWNCA
    - Mutually exclusive with `rv_getcert_ownca_private_key_content`
  - Type: `str`
  - Required: `true`

- `rv_getcert_ownca_private_key_password`

  - Description: password if the ownca private key is encrypted.
  - Type: `str`
  - Required: `false`

- `rv_getcert_ownca_certificate_content`

  - Description:
    - Certificate as String of OWNCA
    - Mutually exclusive with `rv_getcert_ownca_certificate_path`
  - Type: `str`
  - Required: `true`

- `rv_getcert_ownca_certificate_path`

  - Description:
    - Certificate path of OWNCA
    - Mutually exclusive with `rv_getcert_ownca_certificate_content`
  - Type: `str`
  - Required: `true`

- `rv_getcert_private_key_path`

  - Description:
    - Private Key path
    - Mutually exclusive with `rv_getcert_private_key_content`
  - Type: `str`
  - Required: `true`

- `rv_getcert_private_key_content`

  - Description:
    - Private Key Content
    - Mutually exclusive with `rv_getcert_private_key_path`
  - Type: `str`
  - Required: `true`

- `rv_getcert_private_key_password`

  - Description: password if the private key is encrypted.
  - Type: `str`
  - Required: `false`

- `rv_getcert_certificate_content`

  - Description:
    - Certificate as String
    - Mutually exclusive with `rv_getcert_certificate_path`
  - Type: `str`
  - Required: `true`

- `rv_getcert_certificate_path`

  - Description:
    - Certificate path
    - Mutually exclusive with `rv_getcert_certificate_content`
  - Type: `str`
  - Required: `true`

- `rv_getcert_private_key_size`

  - Description: Size of the private key
  - Type: `int`
  - Required: `false`

- `rv_getcert_validity_days`

  - Description: Validity of certificate in days
  - Type: `int`
  - Required: `false`
  - Default: `7`

- `rv_getcert_key_use`
  - Description: Validity of certificate in days
  - Type: `int`
  - Required: `false`
  - Default: `7`

## Example Playbook Bitwarden Desktop

```yaml
- name: Create Certificate
  ansible.builtin.import_role:
    name: arpanrec.utilities.bitwarden_desktop
```

## Testing Bitwarden Desktop

```bash
molecule test -s role.bitwarden_desktop.default
```
