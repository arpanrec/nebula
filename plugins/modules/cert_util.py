"""
Ansible module to generate private key and certificate
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

from typing import Optional

from ansible.module_utils.basic import AnsibleModule

from psychicoctowinner.cert_util import gen_private_key, gen_x590_certificate

# pylint: disable=C0103
__metaclass__ = type

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

DOCUMENTATION = r"""
---
module: cert_util
short_description: Generate private key and certificate
description: Generate private key and certificate
options:
  private_key_path:
    description: Path to private key file
    required: false
    type: str
  private_key_content:
    description: Content of private key file
    required: false
    type: str
  private_key_passphrase:
    description: Passphrase of private key file
    required: false
    type: str
  public_exponent:
    description: Public exponent of private key
    required: false
    type: int
    default: 65537
  key_size:
    description: Key size of private key
    required: false
    type: int
    default: 2048
  certificate_path:
    description: Path to certificate file
    required: false
    type: str
  certificate_content:
    description: Content of certificate file
    required: false
    type: str
  properties:
    description: Certificate properties
    required: false
    type: dict
    default: {}
    suboptions:
      NAME:
        description: Subject Name
        required: false
        type: dict
        suboptions:
          COUNTRY_NAME:
            description: Country Name
            required: true
            type: str
          STATE_OR_PROVINCE_NAME:
            description: State or Province Name
            required: true
            type: str
          LOCALITY_NAME:
            description: Locality Name
            required: true
            type: str
          ORGANIZATION_NAME:
            description: Organization Name
            required: true
            type: str
          ORGANIZATIONAL_UNIT_NAME:
            description: Organizational Unit Name
            required: true
            type: str
          COMMON_NAME:
            description: Common Name
            required: true
            type: str
      not_valid_after:
        description: Certificate validity in days
        required: true
        type: int
      SetPublicKey:
        description: Set Public Key
        required: false
        type: bool
        default: true
      SetAuthorityKeyIdentifier:
        description: Set Authority Key Identifier
        required: false
        type: bool
        default: true
      SetAuthorityKeyIdentifierCritical:
        description: Set Authority Key Identifier Critical
        required: false
        type: bool
        default: false
      SetSubjectKeyIdentifier:
        description: Set Subject Key Identifier
        required: false
        type: bool
        default: true
      SetSubjectKeyIdentifierCritical:
        description: Set Subject Key Identifier Critical
        required: false
        type: bool
        default: false
      ExtendedKeyUsage:
        description: Extended Key Usage
        required: false
        type: list
        default: []
        elements: str
        options:
          - SERVER_AUTH
          - CLIENT_AUTH
          - CODE_SIGNING
          - EMAIL_PROTECTION
          - TIME_STAMPING
          - SMARTCARD_LOGON
          - KERBEROS_PKINIT_KDC
          - IPSEC_IKE
          - CERTIFICATE_TRANSPARENCY
          - ANY_EXTENDED_KEY_USAGE
        sample:
          - SERVER_AUTH
          - CLIENT_AUTH
          - CODE_SIGNING
          - EMAIL_PROTECTION
          - TIME_STAMPING
          - SMARTCARD_LOGON
          - KERBEROS_PKINIT_KDC
          - IPSEC_IKE
          - CERTIFICATE_TRANSPARENCY
          - ANY_EXTENDED_KEY_USAGE
      ExtendedKeyUsageCritical:
        description: Extended Key Usage Critical
        required: false
        type: bool
        default: false
      KeyUsage:
        description: Key Usage
        required: false
        type: dict
        default: {}
        suboptions:
          digital_signature:
            description: Digital Signature
            required: false
            type: bool
            default: false
          content_commitment:
            description: Content Commitment
            required: false
            type: bool
            default: false
          key_encipherment:
            description: Key Encipherment
            required: false
            type: bool
            default: false
          data_encipherment:
            description: Data Encipherment
            required: false
            type: bool
            default: false
          key_agreement:
            description: Key Agreement
            required: false
            type: bool
            default: false
          key_cert_sign:
            description: Key Cert Sign
            required: false
            type: bool
            default: false
          crl_sign:
            description: CRL Sign
            required: false
            type: bool
            default: false
          encipher_only:
            description: Encipher Only
            required: false
            type: bool
            default: false
          decipher_only:
            description: Decipher Only
            required: false
            type: bool
            default: false
      KeyUsageCritical:
        description: Key Usage Critical
        required: false
        type: bool
        default: false
      BasicConstraints:
        description: Basic Constraints
        required: false
        type: dict
        default: {}
        suboptions:
          ca:
            description: CA
            required: false
            type: bool
            default: false
          path_length:
            description: Path Length
            required: false
            type: int
            default: null
      BasicConstraintsCritical:
        description: Basic Constraints Critical
        required: false
        type: bool
        default: false
      SubjectAlternativeName:
        description: Subject Alternative Name
        required: false
        type: list
        default: []
        elements: str
      SubjectAlternativeNameCritical:
        description: Subject Alternative Name Critical
        required: false
        type: bool
        default: false
  certificate_authority:
    description: Certificate Authority
    required: false
    type: dict
    default: null
    suboptions:
      private_key_path:
        description: Path to private key file
        required: false
        type: str
      private_key_content:
        description: Content of private key file
        required: false
        type: str
      private_key_passphrase:
        description: Passphrase of private key file
        required: false
        type: str
      certificate_path:
        description: Path to certificate file
        required: false
        type: str
      certificate_content:
        description: Content of certificate file
        required: false
        type: str
  private_key_permission:
    description: Private Key Permission
    required: false
    type: int
    default: "0o600"
  certificate_permission:
    description: Certificate Permission
    required: false
    type: int
    default: "0o644"
"""

EXAMPLES = r"""
- name: Vault | Prepare
  arpanrec.utils.cert_util:
    private_key_passphrase: password
    private_key_path: ca_private_key.pem
    certificate_path: ca_certificate.pem
    properties:
      NAME:
      COUNTRY_NAME: US
      STATE_OR_PROVINCE_NAME: California11
      LOCALITY_NAME: San Francisco
      ORGANIZATION_NAME: Example Inc.
      ORGANIZATIONAL_UNIT_NAME: Example Inc. Unit
      COMMON_NAME: example.com
      SetSubjectKeyIdentifier: true
      SetSubjectKeyIdentifierCritical: true
      BasicConstraints:
      ca: true
      BasicConstraintsCritical: true
      KeyUsage:
        - digitalSignature
        - keyCertSign
        - cRLSign
      KeyUsageCritical: true
      ExtendedKeyUsage:
        - serverAuth
        - clientAuth
      ExtendedKeyUsageCritical: true
      not_valid_after: 365

- name: Vault | Prepare
  arpanrec.utils.cert_util:
    private_key_passphrase: password
    private_key_path: private_key.pem
    certificate_path: certificate.pem
    certificate_authority:
      private_key_path: ca_private_key.pem
      certificate_path: ca_certificate.pem
      private_key_passphrase: password
    properties:
      SetAuthorityKeyIdentifier: true
      SetAuthorityKeyIdentifierCritical: true
      NAME:
      COUNTRY_NAME: US
      STATE_OR_PROVINCE_NAME: California1
      LOCALITY_NAME: San Francisco
      ORGANIZATION_NAME: Example Inc.
      ORGANIZATIONAL_UNIT_NAME: Example Inc. Unit
      COMMON_NAME: example.com
      not_valid_after: 364
"""

RETURN = r"""
private_key:
  description: Private Key
  type: str
  returned: always
certificate:
  description: Certificate
  type: str
  returned: always
private_key_generated:
  description: Private Key Generated
  type: bool
  returned: always
certificate_generated:
  description: Certificate Generated
  type: bool
  returned: always
private_key_generated_reason:
  description: Private Key Generated Reason
  type: str
  returned: always
certificate_generated_reason:
  description: Certificate Generated Reason
  type: str
  returned: always
"""


def run_module():
    """
    Ansible Module
    """
    module_args = {
        "private_key_path": {"type": "path", "required": False, "default": None},
        "private_key_content": {"type": "str", "required": False, "default": None},
        "private_key_passphrase": {"type": "str", "required": False, "default": None, "no_log": True},
        "public_exponent": {"type": "int", "required": False, "default": 65537},
        "key_size": {"type": "int", "required": False, "default": 1024 * 2},
        "certificate_path": {"type": "path", "required": False, "default": None},
        "certificate_content": {"type": "str", "required": False, "default": None},
        "properties": {"type": "dict", "required": False, "default": {}},
        "certificate_authority": {"type": "dict", "required": False, "default": None},
        "private_key_permission": {"type": "int", "required": False, "default": 0o600},
        "certificate_permission": {"type": "int", "required": False, "default": 0o644},
    }

    module = AnsibleModule(module_args, supports_check_mode=False)

    private_key_path: str = module.params["private_key_path"]
    private_key_content: str = module.params["private_key_content"]
    private_key_passphrase: str = module.params["private_key_passphrase"]
    public_exponent: int = module.params["public_exponent"]
    key_size: int = module.params["key_size"]
    certificate_path: str = module.params["certificate_path"]
    certificate_content: str = module.params["certificate_content"]
    properties: dict = module.params["properties"]
    certificate_authority: dict = module.params["certificate_authority"]
    certificate_sign_authority: Optional[tuple] = None
    private_key_file_mode: int = module.params["private_key_permission"]
    certificate_file_mode: int = module.params["certificate_permission"]

    if certificate_authority:
        ca_private_key_content: str = certificate_authority.get("private_key_content", None)
        ca_private_key_path: str = certificate_authority.get("private_key_path", None)
        ca_certificate_content: str = certificate_authority.get("certificate_content", None)
        ca_certificate_path: str = certificate_authority.get("certificate_path", None)
        cat_private_key_passphrase: str = certificate_authority.get("private_key_passphrase", None)

        if ca_certificate_content and ca_certificate_path:
            module.fail_json(msg="Cannot specify both certificate_path and certificate_content")

        if not ca_certificate_content and not ca_certificate_path:
            module.fail_json(msg="Must specify either certificate_path or certificate_content")

        if ca_private_key_content and ca_private_key_path:
            module.fail_json(msg="Cannot specify both private_key_path and private_key_content")

        if not ca_private_key_content and not ca_private_key_path:
            module.fail_json(msg="Must specify either private_key_path or private_key_content")

        if ca_private_key_path:
            with open(ca_private_key_path, "r", encoding="utf-8") as f:
                ca_private_key_content = f.read()

        if ca_certificate_path:
            with open(ca_certificate_path, "r", encoding="utf-8") as f:
                ca_certificate_content = f.read()

        cat_private_key = serialization.load_pem_private_key(
            ca_private_key_content.encode(encoding="utf-8", errors="strict"),
            password=cat_private_key_passphrase.encode() if cat_private_key_passphrase else None,
            backend=default_backend(),
        )
        cat_certificate = x509.load_pem_x509_certificate(ca_certificate_content.encode(encoding="utf-8", errors="strict"), backend=default_backend())

        certificate_sign_authority: tuple = (
            cat_certificate,
            cat_private_key,
        )

    try:
        gen_private_key_res = gen_private_key(
            private_key_path=private_key_path,
            private_key_content=private_key_content,
            private_key_passphrase=private_key_passphrase,
            public_exponent=public_exponent,
            key_size=key_size,
            private_key_file_mode=private_key_file_mode,
        )
        gen_x590_certificate_res = gen_x590_certificate(
            certificate_path=certificate_path,
            certificate_content=certificate_content,
            rsa_private_key=gen_private_key_res["private_key"],
            properties=properties,
            certificate_authority=certificate_sign_authority,
            certificate_file_mode=certificate_file_mode,
        )
        module.exit_json(
            changed=gen_private_key_res["need_to_generate"] or gen_x590_certificate_res["need_to_generate"],
            private_key=gen_private_key_res["private_key_content"],
            certificate=gen_x590_certificate_res["certificate_full_chain"],
            private_key_generated=gen_private_key_res["need_to_generate"],
            certificate_generated=gen_x590_certificate_res["need_to_generate"],
            private_key_generated_reason=gen_private_key_res.get("need_to_generate_reason", None),
            certificate_generated_reason=gen_x590_certificate_res.get("need_to_generate_reason", None),
        )
    except Exception as e:
        module.fail_json(msg=str(e))


if __name__ == "__main__":
    run_module()
