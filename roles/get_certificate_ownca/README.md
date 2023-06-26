# Ansible Role: Get Certificate (arpanrec.utilities.get_certificate_ownca)

Get Server or Client certificate.

## Variables

### Variables: CA

#### Variables: CA: Private Key

- `get_certificate_ownca_rv_private_key_content`

  - Description:
    - Private Key as String of OWNCA
    - Mutually exclusive with `get_certificate_ownca_rv_private_key_path`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_private_key_path`

  - Description:
    - Private Key path of OWNCA
    - Mutually exclusive with `get_certificate_ownca_rv_private_key_content`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_private_key_password`

  - Description: password if the ownca private key is encrypted.
  - Type: `str`
  - Required: `false`

#### Variables: CA: Certificate

- `get_certificate_ownca_rv_certificate_content`

  - Description:
    - Certificate as String of OWNCA
    - Mutually exclusive with `get_certificate_ownca_rv_certificate_path`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_certificate_path`

  - Description:
    - Certificate path of OWNCA
    - Mutually exclusive with `get_certificate_ownca_rv_certificate_content`
  - Type: `str`
  - Required: `true`

### Variables: Private Key

- `get_certificate_ownca_rv_getcert_private_key_content`

  - Description:
    - Private Key Content
    - Mutually exclusive with `get_certificate_ownca_rv_getcert_private_key_path`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_getcert_private_key_path`

  - Description:
    - Private Key path
    - Mutually exclusive with `get_certificate_ownca_rv_getcert_private_key_content`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_getcert_private_key_owner`

  - Description: Private Key file owner, when `get_certificate_ownca_rv_getcert_private_key_path` is defined
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_private_key_group`

  - Description: Private Key file owner group, when `get_certificate_ownca_rv_getcert_private_key_path` is defined
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_private_key_file_mode`

  - Description: Private Key file mode, when `get_certificate_ownca_rv_getcert_private_key_path` is defined
  - Type: `str`
  - Required: `false`
  - Default: `0600`

- `get_certificate_ownca_rv_getcert_private_key_size`

  - Description: Size of the private key
  - Type: `int`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_private_key_password`

  - Description: password if the private key is encrypted.
  - Type: `str`
  - Required: `false`

### Variables: Certificate

- `get_certificate_ownca_rv_getcert_certificate_content`

  - Description:
    - Certificate as String
    - Mutually exclusive with `get_certificate_ownca_rv_getcert_certificate_path`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_getcert_certificate_path`

  - Description:
    - Certificate path
    - Mutually exclusive with `get_certificate_ownca_rv_getcert_certificate_content`
  - Type: `str`
  - Required: `true`

- `get_certificate_ownca_rv_getcert_certificate_file_mode`

  - Description: Private Key file mode, when `get_certificate_ownca_rv_getcert_certificate_path` is defined
  - Type: `str`
  - Required: `false`
  - Default: `0600`

- `get_certificate_ownca_rv_getcert_certificate_owner`

  - Description: Private Key file owner, when `get_certificate_ownca_rv_getcert_certificate_path` is defined
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_certificate_group`

  - Description: Private Key file owner group, when `get_certificate_ownca_rv_getcert_certificate_path` is defined
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_validity_days`

  - Description: Validity of certificate in days
  - Type: `int`
  - Required: `false`
  - Default: `7`

#### Variables: Certificate: CSR Config

- `get_certificate_ownca_rv_getcert_key_usage`
  - Description: Key Usages, that can be found [here](https://www.openssl.org/docs/manmaster/man5/x509v3_config.html)
  - Type: `list[str]`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_extended_key_usage`
  - Description: Extended Key Usages, that can be found [here](https://www.openssl.org/docs/manmaster/man5/x509v3_config.html)
  - Type: `list[str]`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_subject_alt_name`
  - Description:
    - Subject Alternative Name (SAN) extension to attach to the certificate signing request.
    - Values must be prefixed by their options. (These are email, URI, DNS, RID, IP, dirName, otherName, and the ones specific to your CA).
    - Note that if no SAN is specified, but a common name, the common name will be added as a SAN except if useCommonNameForSAN is set to false.
    - More at <https://tools.ietf.org/html/rfc5280#section-4.2.1.6>.
  - Type: `list[str]`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_subject`
  - Description:
    - Key/value pairs that will be present in the subject name field of the certificate signing request.
    - If you need to specify more than one value with the same key, use a list as value.
    - Subject field option, such as `countryName`, `stateOrProvinceName`, `localityName`, `organizationName`, `organizationalUnitName`, `commonName`, or `emailAddress`.
  - Type: `dict`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_basic_constraints`
  - Description: Indicates basic constraints, such as if the certificate is a CA.
  - Type: `list[str]`
  - Required: `false`

### Variables: Certificate Full Chain

- `get_certificate_ownca_rv_getcert_certificatefullchain_path`

  - Description: Certificate full chain path
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_certificatefullchain_file_mode`

  - Description: Private Key file mode, when `get_certificate_ownca_rv_getcert_certificatefullchain_path` is defined
  - Type: `str`
  - Required: `false`
  - Default: `0600`

- `get_certificate_ownca_rv_getcert_certificatefullchain_owner`

  - Description: Private Key file owner, when `get_certificate_ownca_rv_getcert_certificatefullchain_path` is defined
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_certificatefullchain_group`

  - Description: Private Key file owner group, when `get_certificate_ownca_rv_getcert_certificatefullchain_path` is defined
  - Type: `str`
  - Required: `false`

### Variables: PKCS12 Certificate

- `get_certificate_ownca_rv_getcert_pkcs12_path`

  - Description: Certificate pkcs12 path
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_pkcs12_password`

  - Description: Certificate pkcs12 password
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_pkcs12_file_mode`

  - Description: Private Key file mode, when `get_certificate_ownca_rv_getcert_pkcs12_path` is defined
  - Type: `str`
  - Required: `false`
  - Default: `0600`

- `get_certificate_ownca_rv_getcert_pkcs12_owner`

  - Description: Private Key file owner, when `get_certificate_ownca_rv_getcert_pkcs12_path` is defined
  - Type: `str`
  - Required: `false`

- `get_certificate_ownca_rv_getcert_pkcs12_group`

  - Description: Private Key file owner group, when `get_certificate_ownca_rv_getcert_pkcs12_path` is defined
  - Type: `str`
  - Required: `false`

## Example Certificate Role

```yaml
- name: Create Certificate
  ansible.builtin.import_role:
    name: arpanrec.utilities.get_certificate_ownca
  vars:
    get_certificate_ownca_rv_private_key_path: ownca_private_key.pem
    get_certificate_ownca_rv_certificate_path: ownca_certificate_path.pem
    get_certificate_ownca_rv_private_key_password: password
    get_certificate_ownca_rv_getcert_private_key_password: password
    get_certificate_ownca_rv_getcert_private_key_path: private_key.pem
    get_certificate_ownca_rv_getcert_certificate_path: certificate_path.pem
    get_certificate_ownca_rv_getcert_molecule_prepare_csr_path: ownca_csr.pem
    get_certificate_ownca_rv_getcert_certificatefullchain_path: certificate_chain_path.pem
    get_certificate_ownca_rv_getcert_key_usage:
      - digitalSignature
      - nonRepudiation
      - keyEncipherment
      - dataEncipherment
      - keyCertSign
      - cRLSign
    get_certificate_ownca_rv_getcert_extended_key_usage:
      - serverAuth
      - clientAuth
      - codeSigning
      - emailProtection
      - timeStamping
      - OCSPSigning
      - msCTLSign
    get_certificate_ownca_rv_getcert_subject_alt_name:
      - DNS:www.arpanrec.com
      - IP:172.0.0.1
    get_certificate_ownca_rv_getcert_subject:
      commonName: www.arpanrec.com
    get_certificate_ownca_rv_getcert_basic_constraints:
      - CA:TRUE
      - pathlen:0
    get_certificate_ownca_rv_getcert_private_key_file_mode: "0600"
```

## Testing Certificate Role

```bash
molecule test -s role.get_certificate_ownca.default
```
