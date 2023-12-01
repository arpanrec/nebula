"""
This module provides functionality for splitting a string of concatenated certificates into a list of individual certificates.

The main function, `split_certificates`, takes a string that contains one or more PEM-formatted certificates and splits it into a list of individual certificates.
Each certificate in the list is a string that begins with "-----BEGIN CERTIFICATE-----" and ends with "-----END CERTIFICATE-----".

The module also includes a `FilterModule` class that makes the `split_certificates` function available as a filter in Ansible playbooks.

This module is part of the arpanrec.utilities collection.

Author:
    Arpan Mandal (arpan.rec@gmail.com)
"""


def split_certificates(string):
    """
    Splits a string of concatenated certificates into a list of individual certificates.

    This function takes a string that contains one or more PEM-formatted certificates and splits it into a list of individual certificates.
    Each certificate in the list is a string that begins with "-----BEGIN CERTIFICATE-----" and ends with "-----END CERTIFICATE-----".

    Parameters:
        certificates_str (str): A string containing one or more concatenated PEM-formatted certificates.

    Returns:
        list: A list of strings, where each string is a PEM-formatted certificate.
    """

    list_of_certs = []
    list_of_lines = string.split("\n")
    for line in list_of_lines:
        if line == "-----BEGIN CERTIFICATE-----":
            temp_cert_list = []
            temp_cert_list.append(line)
        elif line == "":
            continue
        elif line == "-----END CERTIFICATE-----":
            temp_cert_list.append(line + "\n")
            certificate = "\n".join(temp_cert_list)
            list_of_certs.append(certificate)
        else:
            temp_cert_list.append(line)
    return list_of_certs


class FilterModule:
    """
    A filter plugin class for Ansible.

    This class provides a filter named 'split_certificates' that can be used in Ansible templates. The filter takes a string of concatenated PEM-formatted certificates and splits it into a list of individual certificates.

    Methods:
        filters: Returns a dictionary mapping the filter name ('split_certificates') to the filter function.
    """

    def filters(self):
        """
        Returns a dictionary mapping filter names to filter functions.

        This function is used by Ansible to discover all of the filters in this plugin. The returned dictionary maps the name of each filter (as a string) to the function that implements the filter.

        Returns:
            dict: A dictionary where the keys are filter names and the values are the corresponding filter functions.
        """
        return {"split_certificates": split_certificates}
