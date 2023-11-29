#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
common_lib/ca_utils.py

This module contains utility functions and classes for handling operations related to Certificate Authority (CA).
It includes functionalities for generating, validating, and parsing certificates, as well as handling private keys.

Functions:
x590_certificate: Handles operations related to X.590 certificates.
private_key: Handles operations related to private keys.

Note: Replace this with the actual list of functions and classes in the module, along with a brief description of each.

This module is part of the common_lib package and can be imported using "from common_lib import ca_utils".
"""

import os
import pathlib
from datetime import datetime, timedelta
from ipaddress import IPv4Address, IPv6Address
from typing import Any, Dict, LiteralString, Optional, Tuple, List

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.types import CertificatePublicKeyTypes, PrivateKeyTypes
from cryptography.x509 import (
    AuthorityKeyIdentifier,
    Certificate,
    CertificateBuilder,
    Name,
    NameAttribute,
    NameOID,
    SubjectKeyIdentifier,
    load_pem_x509_certificate,
    random_serial_number,
    ExtendedKeyUsage,
    Extension,
    KeyUsage,
    ExtensionNotFound,
    BasicConstraints,
    GeneralName,
    UniformResourceIdentifier,
    DNSName,
    IPAddress,
    RFC822Name,
    DirectoryName,
    SubjectAlternativeName,
)
from cryptography.x509.oid import ExtendedKeyUsageOID


def _is_property_set(properties: Dict[str, Any], property_name: str) -> bool:
    """
    Checks if a property is set.

    Parameters:
    properties (dict): A dictionary containing the properties.
    property_name (str): The name of the property to check.

    Returns:
    bool: True if the property is set, False otherwise.
    """

    return property_name in properties and properties[property_name] is not None


# pylint: disable=R0913,R0914,R0912,R0915,W0718
def private_key(
    private_key_path: LiteralString = None,
    private_key_content: LiteralString = None,
    private_key_passphrase: LiteralString = None,
    public_exponent: int = 65537,
    key_size: int = 1024 * 2,
    backend: Any = default_backend(),
    private_key_file_mode: int = 0o400,
) -> Tuple[PrivateKeyTypes, LiteralString, bool, LiteralString]:
    """
    Handles operations related to private keys.

    Parameters:
    private_key_path (LiteralString, optional): Path to the private key file.
    private_key_content (LiteralString, optional): Content of the private key.
    private_key_passphrase (LiteralString, optional): Passphrase for the private key.
    public_exponent (int, optional): Public exponent for the RSA key. Defaults to 65537.
    key_size (int, optional): Size of the key. Defaults to 2048 bits.
    backend (Any, optional): Backend to use for cryptography operations. Defaults to default_backend().
    private_key_file_mode (int, optional): File mode for the private key file. Defaults to 0o400.

    Returns:
    tuple: A tuple containing the private key, a literal string, a boolean value, and another literal string.
    """

    if private_key_path and private_key_content:
        raise ValueError("Only one of private_key_path or private_key_content can be specified")

    if private_key_path and os.path.exists(private_key_path) and pathlib.Path(private_key_path).is_dir():
        raise ValueError(f"private_key_path '{private_key_path}' is a directory, not a file")

    rsa_private_key: Optional[PrivateKeyTypes] = None
    need_to_generate: bool = False
    need_to_generate_reason: Optional[LiteralString] = None
    encryption_algorithm_private_key = serialization.BestAvailableEncryption(private_key_passphrase.encode("utf-8")) if private_key_passphrase else serialization.NoEncryption()

    if private_key_path and os.path.exists(private_key_path) and pathlib.Path(private_key_path).is_file():
        with open(private_key_path, "rb") as f:
            private_key_content = f.read()
    else:
        need_to_generate = True
        need_to_generate_reason = "private_key_path does not exist"

    if private_key_content:
        try:
            rsa_private_key = serialization.load_pem_private_key(
                private_key_content,
                password=private_key_passphrase.encode("utf-8"),
                backend=backend,
            )
        except Exception as e:
            need_to_generate = True
            need_to_generate_reason = "private_key_content is invalid + " + str(e)
    else:
        need_to_generate = True
        need_to_generate_reason = "private_key_content is empty"

    if not need_to_generate and rsa_private_key.key_size != key_size:
        need_to_generate = True
        need_to_generate_reason = "key_size is not valid"

    if not need_to_generate and rsa_private_key.public_key().public_numbers().e != public_exponent:
        need_to_generate = True
        need_to_generate_reason = "public_exponent is not valid"

    if need_to_generate:
        rsa_private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=backend,
        )

    private_key_bytes: bytes = rsa_private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=encryption_algorithm_private_key,
    )

    if private_key_path:
        # Remove existing file if it exists
        if os.path.exists(private_key_path):
            os.remove(private_key_path)
        with open(private_key_path, "wb") as f:
            f.write(private_key_bytes)
        os.chmod(private_key_path, private_key_file_mode)

    return (
        rsa_private_key,
        private_key_bytes.decode("utf-8"),
        need_to_generate,
        need_to_generate_reason,
    )


def _load_existing_certificate(certificate_path: LiteralString = None, certificate_content: LiteralString = None) -> Tuple[Optional[Certificate], Optional[LiteralString]]:
    """
    Handles loading an existing certificate.

    Parameters:
    certificate_path (LiteralString, optional): Path to the certificate file.
    certificate_content (LiteralString, optional): Content of the certificate.

    Returns:
    Certificate: The loaded certificate.
    String: An exception if the certificate could not be loaded.
    """

    if certificate_path and certificate_content:
        raise ValueError("Only one of certificate_path or certificate_content can be specified")

    if certificate_path and os.path.exists(certificate_path) and pathlib.Path(certificate_path).is_dir():
        raise ValueError(f"certificate_path '{certificate_path}' is a directory, not a file")

    _x590_certificate: Optional[Certificate] = None

    if certificate_path and os.path.exists(certificate_path) and pathlib.Path(certificate_path).is_file():
        with open(certificate_path, "rb") as f:
            certificate_content = f.read()
    else:
        return None, "certificate_path does not exist"

    if certificate_content:
        try:
            _x590_certificate = load_pem_x509_certificate(certificate_content, backend=default_backend())
        except Exception as e:
            return None, "certificate_content is invalid + " + str(e)
    else:
        return None, "certificate_content is empty"

    return _x590_certificate, None


# pylint: disable=R0913,R0914,R0912,R0915
def x590_certificate(
    certificate_path: LiteralString = None,
    certificate_content: LiteralString = None,
    rsa_private_key: PrivateKeyTypes = None,
    properties: Dict[str, Any] = None,
    certificate_file_mode: int = 0o444,
    certificate_authority: Optional[Tuple[Certificate, PrivateKeyTypes]] = None,
) -> Tuple[Certificate, LiteralString, bool, LiteralString]:
    """
    Handles operations related to X.590 certificates.

    Parameters:
    certificate_path (LiteralString, optional): Path to the certificate file.
    certificate_content (LiteralString, optional): Content of the certificate.
    rsa_private_key (PrivateKeyTypes, optional): RSA private key for the certificate.
    properties (dict, optional): Additional properties for the certificate.
    certificate_file_mode (int, optional): File mode for the certificate file. Defaults to 0o444.
    certificate_authority (tuple, optional): Tuple containing the certificate and private key of the certificate authority.

    Returns:
    tuple: A tuple containing the certificate, a literal string, a boolean value, and another literal string.
    """

    if certificate_path and certificate_content:
        raise ValueError("Only one of certificate_path or certificate_content can be specified")

    if certificate_path and os.path.exists(certificate_path) and pathlib.Path(certificate_path).is_dir():
        raise ValueError(f"certificate_path '{certificate_path}' is a directory, not a file")

    if not rsa_private_key:
        raise ValueError("rsa_private_key is required")

    need_to_generate: bool = False
    need_to_generate_reason: Optional[LiteralString] = None
    _x590_certificate: Optional[Certificate] = None
    # Check if certificate is there and set _x590_certificate
    certificate_load_exception: Tuple[Optional[Certificate], Optional[LiteralString]] = _load_existing_certificate(
        certificate_path=certificate_path, certificate_content=certificate_content
    )
    if certificate_load_exception[1]:
        need_to_generate = True
        need_to_generate_reason = certificate_load_exception[1]
    else:
        _x590_certificate = certificate_load_exception[0]

    builder = CertificateBuilder()
    expected_serial_number: int = random_serial_number()
    builder = builder.serial_number(expected_serial_number)

    # Set Expectation for the certificate -------------------------------------------------------------------------------------------------------------

    # Subject Name
    if not properties.get("NAME", None) and not certificate_authority:
        raise ValueError("NAME is required")

    if properties.get("NAME", None):
        expected_subject_name = Name([NameAttribute(getattr(NameOID, name_key), name_value) for name_key, name_value in properties["NAME"].items()])
    else:
        expected_subject_name = certificate_authority[0].subject

    builder = builder.subject_name(expected_subject_name)

    # Issuer Name
    if certificate_authority:
        expected_issuer_name = certificate_authority[0].subject
    else:
        expected_issuer_name = expected_subject_name

    builder = builder.issuer_name(expected_issuer_name)

    # Public Key
    expected_public_key: Optional[CertificatePublicKeyTypes] = None
    if properties.get("SetPublicKey", True):
        expected_public_key: CertificatePublicKeyTypes = rsa_private_key.public_key()

    if expected_public_key:
        builder = builder.public_key(expected_public_key)

    # Authority Key Identifier
    expected_authority_key_identifier_value: Optional[AuthorityKeyIdentifier] = None
    expected_authority_key_identifier_critical: Optional[bool] = None

    if not bool(properties.get("SetAuthorityKeyIdentifier", False)) and "SetAuthorityKeyIdentifierCritical" in properties:
        raise ValueError("SetAuthorityKeyIdentifierCritical cannot be set without SetAuthorityKeyIdentifier to True")

    if properties.get("SetAuthorityKeyIdentifier", False) and certificate_authority:
        issuer_general_names: SubjectAlternativeName = SubjectAlternativeName([])

        try:
            issuer_general_names = certificate_authority[0].extensions.get_extension_for_class(SubjectAlternativeName).value
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        expected_authority_key_identifier_value = AuthorityKeyIdentifier(
            key_identifier=AuthorityKeyIdentifier.from_issuer_public_key(certificate_authority[0].public_key()).key_identifier,
            authority_cert_serial_number=certificate_authority[0].serial_number,
            authority_cert_issuer=issuer_general_names,
        )
    elif properties.get("SetAuthorityKeyIdentifier", False):
        raise ValueError("SetAuthorityKeyIdentifier cannot be set without certificate_authority")

    if expected_authority_key_identifier_value:
        expected_authority_key_identifier_critical = properties.get("SetAuthorityKeyIdentifierCritical", False)
        builder = builder.add_extension(expected_authority_key_identifier_value, critical=expected_authority_key_identifier_critical)

    # Subject Key Identifier
    expected_subject_key_identifier_value: Optional[SubjectKeyIdentifier] = None
    expected_subject_key_identifier_critical: Optional[bool] = None
    if properties.get("SetSubjectKeyIdentifier", False):
        expected_subject_key_identifier_value = SubjectKeyIdentifier.from_public_key(rsa_private_key.public_key())

    if not expected_subject_key_identifier_value and "SetSubjectKeyIdentifierCritical" in properties:
        raise ValueError("SetSubjectKeyIdentifierCritical cannot be set without SetSubjectKeyIdentifier to True")

    if expected_subject_key_identifier_value:
        expected_subject_key_identifier_critical = properties.get("SetSubjectKeyIdentifierCritical", False)
        builder = builder.add_extension(expected_subject_key_identifier_value, critical=expected_subject_key_identifier_critical)

    # Key Usage
    expected_key_usage_value: Optional[KeyUsage] = None
    expected_key_usage_critical: Optional[bool] = None
    if "KeyUsage" in properties:
        if not isinstance(properties.get("KeyUsage"), dict):
            raise ValueError("KeyUsage must be a dictionary")
        _default_key_usage = {
            "digital_signature": False,
            "content_commitment": False,
            "key_encipherment": False,
            "data_encipherment": False,
            "key_agreement": False,
            "key_cert_sign": False,
            "crl_sign": False,
            "encipher_only": False,
            "decipher_only": False,
        }
        _default_key_usage.update(properties.get("KeyUsage", {}))
        expected_key_usage_value = KeyUsage(**_default_key_usage)

    if not expected_key_usage_value and "KeyUsageCritical" in properties:
        raise ValueError("KeyUsageCritical cannot be set without KeyUsage")

    if expected_key_usage_value:
        expected_key_usage_critical = properties.get("KeyUsageCritical", False)
        builder = builder.add_extension(expected_key_usage_value, critical=expected_key_usage_critical)

    # Extended Key Usage
    expected_extended_key_usage_value: Optional[ExtendedKeyUsage] = None
    expected_extended_key_usage_critical: Optional[bool] = None

    if "ExtendedKeyUsage" in properties:
        expected_extended_key_usage_value = ExtendedKeyUsage([ExtendedKeyUsageOID.__getattribute__(ExtendedKeyUsageOID, usage) for usage in properties.get("ExtendedKeyUsage", [])])

    if not expected_extended_key_usage_value and "ExtendedKeyUsageCritical" in properties:
        raise ValueError("ExtendedKeyUsageCritical cannot be set without ExtendedKeyUsage")

    if expected_extended_key_usage_value:
        expected_extended_key_usage_critical = properties.get("ExtendedKeyUsageCritical", False)
        builder = builder.add_extension(expected_extended_key_usage_value, critical=expected_extended_key_usage_critical)

    # Basic Constraints
    expected_basic_constraints_value: Optional[BasicConstraints] = None
    expected_basic_constraints_critical: Optional[bool] = None  # properties.get("BasicConstraintsCritical", False)

    if "BasicConstraints" in properties:
        expected_basic_constraints_value = BasicConstraints(
            ca=properties.get("BasicConstraints", {}).get("ca", False),
            path_length=properties.get("BasicConstraints", {}).get("path_length", None),
        )
    if not expected_basic_constraints_value and "BasicConstraintsCritical" in properties:
        raise ValueError("BasicConstraintsCritical cannot be set without BasicConstraints")

    if expected_basic_constraints_value:
        expected_basic_constraints_critical = properties.get("BasicConstraintsCritical", False)
        builder = builder.add_extension(expected_basic_constraints_value, critical=expected_basic_constraints_critical)

    # Subject Alternative Name
    expected_subject_alternative_name_value: Optional[SubjectAlternativeName] = None
    expected_subject_alternative_name_critical: Optional[bool] = None  # properties.get("SubjectAlternativeNameCritical", False)

    if "SubjectAlternativeName" in properties:
        expected_san_entries: List[GeneralName] = []
        for san in properties.get("SubjectAlternativeName", []):
            if san.startswith("DNS:"):
                expected_san_entries.append(DNSName(san[4:]))
            elif san.startswith("URI:"):
                expected_san_entries.append(UniformResourceIdentifier(san[4:]))
            elif san.startswith("IP:"):
                ip = san[3:]
                if ":" in ip:
                    expected_san_entries.append(IPAddress(IPv6Address(ip)))
                else:
                    expected_san_entries.append(IPAddress(IPv4Address(ip)))
            elif san.startswith("EMAIL:"):
                expected_san_entries.append(RFC822Name(san[6:]))
            elif san.startswith("DN:"):
                expected_san_entries.append(DirectoryName(san[3:]))
            else:
                raise ValueError(f"Unknown SubjectAlternativeName type: {san}")

        expected_subject_alternative_name_value = SubjectAlternativeName(expected_san_entries)

    if not expected_subject_alternative_name_value and "SubjectAlternativeNameCritical" in properties:
        raise ValueError("SubjectAlternativeNameCritical cannot be set without SubjectAlternativeName")

    if expected_subject_alternative_name_value:
        expected_subject_alternative_name_critical = properties.get("SubjectAlternativeNameCritical", False)
        builder = builder.add_extension(expected_subject_alternative_name_value, critical=expected_subject_alternative_name_critical)

    # Validity
    if not properties.get("not_valid_after", None):
        raise ValueError("not_valid_after is required")

    now = datetime.utcnow()
    expected_not_valid_before = now
    expected_not_valid_after = now + timedelta(days=int(properties["not_valid_after"]))

    # Check if Expected Valid after is less than CA Valid Till
    if certificate_authority:
        certificate_authority_certificate: Certificate = certificate_authority[0]
        issuer_valid_till: datetime = certificate_authority_certificate.not_valid_after

        if expected_not_valid_after > issuer_valid_till:
            raise ValueError("Certificate Authority is not valid for the duration of the certificate")

    builder = builder.not_valid_before(expected_not_valid_before)
    builder = builder.not_valid_after(expected_not_valid_after)

    # If certificate_authority is set, then sign the certificate with the certificate_authority's private key
    if certificate_authority:
        certificate_authority_private_key: PrivateKeyTypes = certificate_authority[1]
    else:
        certificate_authority_private_key: PrivateKeyTypes = rsa_private_key

    # Validate the certificate -------------------------------------------------------------------------------------------------------------

    # Subject Name
    if not need_to_generate and _x590_certificate and _x590_certificate.subject != expected_subject_name:
        need_to_generate = True
        need_to_generate_reason = "Existing certificate subject name is not as expected"

    # Issuer Name
    if not need_to_generate and _x590_certificate and _x590_certificate.issuer != expected_issuer_name:
        need_to_generate = True
        need_to_generate_reason = "Existing certificate issuer name is not as expected"

    # Public key
    if not need_to_generate and _x590_certificate and _x590_certificate.public_key() != expected_public_key:
        need_to_generate = True
        need_to_generate_reason = "Existing certificate's public key does not match private key used to sign it"

    # Authority Key Identifier
    if not need_to_generate:
        current_authority_key_identifier_value: Optional[AuthorityKeyIdentifier] = None
        current_authority_key_identifier_critical: Optional[bool] = None
        try:
            current_authority_key_identifier = _x590_certificate.extensions.get_extension_for_class(AuthorityKeyIdentifier)
            current_authority_key_identifier_value = current_authority_key_identifier.value
            current_authority_key_identifier_critical = current_authority_key_identifier.critical
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        if current_authority_key_identifier_value != expected_authority_key_identifier_value:
            need_to_generate = True
            need_to_generate_reason = "Authority Key Identifier Mismatch, Existing Certificate is not signed by OwnCA"

        if not need_to_generate and current_authority_key_identifier_critical != expected_authority_key_identifier_critical:
            need_to_generate = True
            need_to_generate_reason = "Authority Key Identifier Critical Mismatch, Existing Certificate is not signed by OwnCA"

    # Subject Key Identifier
    if not need_to_generate:
        current_subject_key_identifier_value: Optional[SubjectKeyIdentifier] = None
        current_subject_key_identifier_critical: Optional[bool] = None
        try:
            current_subject_key_identifier = _x590_certificate.extensions.get_extension_for_class(SubjectKeyIdentifier)
            current_subject_key_identifier_value = current_subject_key_identifier.value
            current_subject_key_identifier_critical = current_subject_key_identifier.critical
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        if current_subject_key_identifier_value != expected_subject_key_identifier_value:
            need_to_generate = True
            need_to_generate_reason = "Subject Key Identifier Mismatch"

        if not need_to_generate and current_subject_key_identifier_critical != expected_subject_key_identifier_critical:
            need_to_generate = True
            need_to_generate_reason = "Subject Key Identifier Critical Mismatch"

    # Key Usage
    if not need_to_generate:
        current_key_usage_value: Optional[KeyUsage] = None
        current_key_usage_critical: Optional[bool] = None
        try:
            current_key_usage: Extension[KeyUsage] = _x590_certificate.extensions.get_extension_for_class(KeyUsage)
            current_key_usage_value: KeyUsage = current_key_usage.value
            current_key_usage_critical: bool = current_key_usage.critical
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        if expected_key_usage_value != current_key_usage_value:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Key Usage does not match"

        if not need_to_generate and expected_key_usage_critical != current_key_usage_critical:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Key Usage Critical does not match"

    # Extended Key Usage
    if not need_to_generate:
        current_extended_key_usage_value: Optional[ExtendedKeyUsage] = None
        current_extended_key_usage_critical: Optional[bool] = None

        try:
            current_extended_key_usage: Extension[ExtendedKeyUsage] = _x590_certificate.extensions.get_extension_for_class(ExtendedKeyUsage)
            current_extended_key_usage_value = current_extended_key_usage.value
            current_extended_key_usage_critical = current_extended_key_usage.critical
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        if expected_extended_key_usage_value != current_extended_key_usage_value:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Extended Key Usage does not match"

        if not need_to_generate and expected_extended_key_usage_critical != current_extended_key_usage_critical:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Extended Key Usage Critical does not match"

    # Basic Constraints
    if not need_to_generate:
        current_basic_constraints_value: Optional[BasicConstraints] = None
        current_basic_constraints_critical: Optional[bool] = None
        try:
            current_basic_constraints: Extension[BasicConstraints] = _x590_certificate.extensions.get_extension_for_class(BasicConstraints)
            current_basic_constraints_value: BasicConstraints = current_basic_constraints.value
            current_basic_constraints_critical: bool = current_basic_constraints.critical
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        if expected_basic_constraints_value != current_basic_constraints_value:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Basic Constraints does not match"

        if not need_to_generate and expected_basic_constraints_critical != current_basic_constraints_critical:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Basic Constraints Critical does not match"

    # Subject Alternative Name
    if not need_to_generate:
        current_subject_alternative_name_value: Optional[SubjectAlternativeName] = None
        current_subject_alternative_name_critical: Optional[bool] = None
        try:
            current_subject_alternative_name: Extension[SubjectAlternativeName] = _x590_certificate.extensions.get_extension_for_class(SubjectAlternativeName)
            current_subject_alternative_name_value: SubjectAlternativeName = current_subject_alternative_name.value
            current_subject_alternative_name_critical: bool = current_subject_alternative_name.critical
        except ExtensionNotFound:
            pass
        except Exception as e:
            raise ValueError("Something went wrong", e)

        if expected_subject_alternative_name_value != current_subject_alternative_name_value:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Subject Alternative Name does not match"

        if not need_to_generate and expected_subject_alternative_name_critical != current_subject_alternative_name_critical:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate's Subject Alternative Name Critical does not match"

    # Validity
    if not need_to_generate:
        current_not_valid_before = _x590_certificate.not_valid_before
        current_not_valid_after = _x590_certificate.not_valid_after

        # Check if existing certificate is expired
        if current_not_valid_after < now:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate is expired"

        # Check if existing certificate is not valid yet
        if not need_to_generate and current_not_valid_before > now:
            need_to_generate = True
            need_to_generate_reason = "Existing certificate is not valid yet"

        # Check if existing certificates validity is more than Issuer Validity
        if not need_to_generate and certificate_authority:
            certificate_authority_certificate: Certificate = certificate_authority[0]
            issuer_valid_till: datetime = certificate_authority_certificate.not_valid_after
            if current_not_valid_after > issuer_valid_till:
                need_to_generate = True
                need_to_generate_reason = "Existing certificate's validity is more than Issuer Validity"

    if need_to_generate:
        _x590_certificate = builder.sign(certificate_authority_private_key, hashes.SHA256(), default_backend())

    certificate_bytes: bytes = _x590_certificate.public_bytes(
        encoding=serialization.Encoding.PEM,
    )

    if certificate_path:
        if os.path.exists(certificate_path):
            os.remove(certificate_path)
        with open(certificate_path, "wb") as f:
            f.write(certificate_bytes)
        os.chmod(certificate_path, certificate_file_mode)

    return _x590_certificate, certificate_bytes.decode("utf-8"), need_to_generate, need_to_generate_reason


# if __name__ == "__main__":
#     ca_a, ca_b, ca_c, ca_d = private_key(private_key_path="ca_private_key.pem", private_key_passphrase="123w456")
#     print("CA Private Key: ", ca_c, ca_d)
#     ca_w, ca_x, ca_y, ca_z = x590_certificate(
#         certificate_path="ca_certificate.pem",
#         rsa_private_key=ca_a,
#         properties={
#             "NAME": {
#                 "COUNTRY_NAME": "IN",
#                 "STATE_OR_PROVINCE_NAME": "state_or_province_name",
#                 "LOCALITY_NAME": "locality_name",
#                 "ORGANIZATION_NAME": "organization_name",
#                 "ORGANIZATIONAL_UNIT_NAME": "organizational_unit_name",
#                 "COMMON_NAME": "common_name",
#                 "EMAIL_ADDRESS": "email_address",
#             },
#             "SetPublicKey": True,
#             "SetSubjectKeyIdentifier": True,
#             "SetSubjectKeyIdentifierCritical": True,
#             "not_valid_after": "365",
#             "ExtendedKeyUsage": [
#                 "SERVER_AUTH",
#                 "CLIENT_AUTH",
#                 "CODE_SIGNING",
#                 "EMAIL_PROTECTION",
#                 "TIME_STAMPING",
#                 "SMARTCARD_LOGON",
#                 "KERBEROS_PKINIT_KDC",
#                 "IPSEC_IKE",
#                 "CERTIFICATE_TRANSPARENCY",
#                 "ANY_EXTENDED_KEY_USAGE",
#             ],
#             "ExtendedKeyUsageCritical": True,
#             "KeyUsage": {
#                 "digital_signature": True,
#                 "content_commitment": True,
#                 "key_encipherment": True,
#                 "data_encipherment": True,
#                 "key_agreement": True,
#                 "key_cert_sign": True,
#                 "crl_sign": True,
#                 "encipher_only": True,
#                 "decipher_only": True,
#             },
#             "KeyUsageCritical": False,
#             "BasicConstraints": {
#                 "ca": True,
#                 "path_length": None,
#             },
#             "BasicConstraintsCritical": True,
#             "SubjectAlternativeName": [
#                 "DNS:localhost",
#                 "DNS:localhost.localdomain",
#                 "DNS:localhost4",
#                 "DNS:localhost4.localdomain4",
#                 "DNS:localhost6",
#                 "DNS:localhost6.localdomain6",
#                 "IP:192.168.1.1",
#                 "IP:::1",
#                 "EMAIL:a@x.x",
#                 "URI:https://localhost",
#                 "URI:https://localhost.localdomain",
#             ],
#             "SubjectAlternativeNameCritical": True,
#         },
#     )
#     print("CA Certificate: ", ca_y, ca_z)

#     a, b, c, d = private_key(private_key_path="private_key.pem", private_key_passphrase="123w456")
#     print("Private Key: ", c, d)
#     v, x, y, z = x590_certificate(
#         certificate_path="certificate.pem",
#         certificate_authority=(ca_w, ca_a),
#         rsa_private_key=a,
#         properties={
#             "NAME": {
#                 "COUNTRY_NAME": "IN",
#                 "STATE_OR_PROVINCE_NAME": "state_or_province_name",
#                 "LOCALITY_NAME": "locality_name",
#                 "ORGANIZATION_NAME": "organization_name",
#                 "ORGANIZATIONAL_UNIT_NAME": "organizational_unit_name",
#                 "COMMON_NAME": "common_name",
#                 "EMAIL_ADDRESS": "email_address",
#             },
#             "SetAuthorityKeyIdentifierCritical": True,
#             "SetAuthorityKeyIdentifier": True,
#             "not_valid_after": "90000",
#             "KeyUsage": {
#                 "digital_signature": False,
#                 "content_commitment": True,
#                 "key_encipherment": True,
#                 "data_encipherment": True,
#                 "key_agreement": False,
#                 "key_cert_sign": False,
#                 "crl_sign": False,
#                 "encipher_only": False,
#                 "decipher_only": False,
#             },
#             "KeyUsageCritical": True,
#             "BasicConstraints": {},
#             "BasicConstraintsCritical": False,
#         },
#     )
#     print("Certificate: ", y, z)
