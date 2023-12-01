"""
This module provides functionality for encryption and decryption using GnuPG.

The main function, `gpg`, takes a set of parameters including the GnuPG home directory,
key server, key fingerprint, key path, key contents, passphrase,
mode of operation, data to be encrypted or decrypted, and a flag indicating whether to receive the key from the key server.

The module also includes a `FilterModule` class that makes the `gpg` function available as a filter in Ansible playbooks.

This module is part of the arpanrec.utilities collection.

Author:
    Arpan Mandal (arpan.rec@gmail.com)
"""

import os
import tempfile
from pathlib import Path
import gnupg

DOCUMENTATION = """
filter_name:
  - description: A brief description of what the filter does.
  - parameters:
    - gnupg_home: The path to the GnuPG home directory. Default is None.
    - key_server: The key server to use for key operations. Default is 'hkps://keys.openpgp.org'.
    - fingerprint: The fingerprint of the key to use for encryption or decryption. Required if recv_keys is False and key_path and key_contents are None.
    - key_path: The path to the key file to use for encryption or decryption. Required if key_contents is None and recv_keys is False and fingerprint is None.
    - key_contents: The contents of the key to use for encryption or decryption. Required if key_path is None and recv_keys is False and fingerprint is None.
    - passphrase: The passphrase to use for key operations. Default is None.
    - mode: The mode of operation. Must be either 'encrypt' or 'decrypt'. Required.
    - data: The data to encrypt or decrypt. Required.
    - recv_keys: Whether to receive the key from the key server. Default is False.
  - return: The result of the encryption or decryption operation.
"""


def d_gpg_ops(
    gnupg_home: str = None,
    key_server: str = "hkps://keys.openpgp.org",
    fingerprint: str = None,
    key_path: str = None,
    key_contents: str = None,
    passphrase: str = None,
    mode: str = None,
    data: str = None,
    recv_keys: bool = False,
) -> str:
    """
    __gpg_ops:
    - description: Performs encryption or decryption using GnuPG.
    - parameters:
        - gnupg_home: The path to the GnuPG home directory. Default is None.
        - key_server: The key server to use for key operations. Default is 'hkps://keys.openpgp.org'.
        - fingerprint: The fingerprint of the key to use for encryption or decryption. Required if recv_keys is False and key_path and key_contents are None.
        - key_path: The path to the key file to use for encryption or decryption. Required if key_contents is None and recv_keys is False and fingerprint is None.
        - key_contents: The contents of the key to use for encryption or decryption. Required if key_path is None and recv_keys is False and fingerprint is None.
        - passphrase: The passphrase to use for key operations. Default is None.
        - mode: The mode of operation. Must be either 'encrypt' or 'decrypt'. Required.
        - data: The data to encrypt or decrypt. Required.
        - recv_keys: Whether to receive the key from the key server. Default is False.
    - return: The result of the encryption or decryption operation.
    """
    if data is None or len(data) == 0:
        raise ValueError("data is required")

    if key_contents and key_path:
        raise ValueError("key_contents and key_path are mutually exclusive")

    if recv_keys and not fingerprint:
        raise ValueError("recv_keys is True but fingerprint is None")

    if mode not in ["encrypt", "decrypt"]:
        raise ValueError("mode must be either encrypt or decrypt")

    if mode == "decrypt" and recv_keys:
        raise ValueError("mode is decrypt but recv_keys is True")

    if not gnupg_home:
        gnupg_env_home = os.getenv("GNUPGHOME", None)
        if gnupg_env_home:
            gnupg_home = gnupg_env_home
        else:
            gnupg_home = Path.joinpath(Path.home(), ".gnupg")
    elif gnupg_home.lower() == "temp":
        with tempfile.TemporaryDirectory(suffix=None, prefix=None, dir=None, ignore_cleanup_errors=False) as temporary_directory:
            gnupg_home = temporary_directory
    else:
        pass
    if not os.path.exists(gnupg_home):
        os.makedirs(gnupg_home, exist_ok=True)
    elif os.path.exists(gnupg_home) and os.path.isfile(gnupg_home):
        raise ValueError("gnupg_home is a file, not a directory")

    gpg = gnupg.GPG(gnupghome=gnupg_home)
    gpg.encoding = "utf-8"

    if recv_keys and fingerprint:
        gpg.recv_keys(key_server, fingerprint)

    if key_path:
        gpg.import_keys_file(key_path, passphrase=passphrase)
    if key_contents:
        gpg.import_keys(key_contents, passphrase=passphrase)

    if mode == "encrypt":
        keys_list = gpg.list_keys()
    elif mode == "decrypt":
        keys_list = gpg.list_keys(True)
    else:
        raise ValueError("mode must be either encrypt or decrypt")

    if len(keys_list) == 0:
        raise ValueError("no keys found")

    if len(keys_list) > 1 and not fingerprint:
        raise ValueError("multiple keys found, please specify a fingerprint")

    if not fingerprint:
        fingerprint = keys_list[0]["fingerprint"]

    gpg.trust_keys(fingerprints=fingerprint, trustlevel="TRUST_ULTIMATE")

    if mode == "encrypt":
        ascii_data = gpg.encrypt(data=data, recipients=fingerprint)

    if mode == "decrypt":
        ascii_data = gpg.decrypt(
            message=data,
            passphrase=passphrase,
            extra_args=["--pinentry-mode", "loopback", "--recipient", fingerprint],
        )

    final_result = str(ascii_data)

    if not ascii_data.ok or len(final_result) == 0:
        raise ValueError("decryption failed : " + ascii_data.status)

    return final_result


def gpg_enc(
    data,
    fingerprint=None,
    gnupg_home="temp",
    key_server="hkps://keys.openpgp.org",
    key_path=None,
    passphrase=None,
    key_contents=None,
    recv_keys=False,
):
    """
    Encrypts the provided data using GnuPG.

    This function takes a set of parameters including the GnuPG home directory, key server, key fingerprint, key path, key contents, passphrase, and data to be encrypted.

    Parameters:
        gpg_home (str): The GnuPG home directory. Required.
        key_server (str): The key server. Optional.
        key_fingerprint (str): The key fingerprint. Required.
        key_path (str): The key path. Optional.
        key_contents (str): The key contents. Optional.
        passphrase (str): The passphrase. Required.
        data (str): The data to be encrypted. Required.

    Returns:
        str: The encrypted data.
    """

    return d_gpg_ops(
        fingerprint=fingerprint,
        gnupg_home=gnupg_home,
        key_server=key_server,
        key_path=key_path,
        passphrase=passphrase,
        key_contents=key_contents,
        mode="encrypt",
        data=data,
        recv_keys=recv_keys,
    )


def gpg_dec(
    data,
    fingerprint=None,
    gnupg_home="temp",
    key_server="hkps://keys.openpgp.org",
    key_path=None,
    passphrase=None,
    key_contents=None,
):
    """
    Decrypts the provided data using GnuPG.

    This function takes a set of parameters including the GnuPG home directory, key server, key fingerprint, key path, key contents, passphrase, and data to be decrypted.

    Parameters:
        gpg_home (str): The GnuPG home directory. Required.
        key_server (str): The key server. Optional.
        key_fingerprint (str): The key fingerprint. Required.
        key_path (str): The key path. Optional.
        key_contents (str): The key contents. Optional.
        passphrase (str): The passphrase. Required.
        data (str): The data to be decrypted. Required.

    Returns:
        str: The decrypted data.
    """
    return d_gpg_ops(
        fingerprint=fingerprint,
        gnupg_home=gnupg_home,
        key_server=key_server,
        key_path=key_path,
        passphrase=passphrase,
        key_contents=key_contents,
        mode="decrypt",
        data=data,
        recv_keys=False,
    )


class FilterModule:
    """
    A filter plugin class for Ansible.

    This class provides a filter named 'gpg_enc' and 'gpg_dec' that can be used in Ansible templates.
    The filters take a set of parameters including the GnuPG home directory, key server, key fingerprint, key path, key contents, passphrase, and data to be encrypted or decrypted.

    Methods:
        filters: Returns a dictionary mapping the filter names ('gpg_enc', 'gpg_dec') to the filter functions.
    """

    def filters(self):
        """
        Returns a dictionary mapping filter names to filter functions.

        This function is used by Ansible to discover all of the filters in this plugin. The returned dictionary maps the name of each filter (as a string) to the function that implements the filter.

        Returns:
            dict: A dictionary where the keys are filter names and the values are the corresponding filter functions.
        """
        return {"gpg_enc": gpg_enc, "gpg_dec": gpg_dec}
