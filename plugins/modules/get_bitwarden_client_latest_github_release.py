#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Ansible Module for Searching the latest bitwarden client release version from github
"""

# Copyright: (c) 2022, Arpan Mandal <arpan.rec@gmail.com>
# MIT (see LICENSE or https://en.wikipedia.org/wiki/MIT_License)
from __future__ import absolute_import, division, print_function

import requests
from ansible.module_utils.basic import AnsibleModule

# pylint: disable=C0103
__metaclass__ = type

DOCUMENTATION = r"""
---
module: get_bitwarden_client_latest_github_release
"""


def run_module(which="desktop"):
    """
    Get the latest bitwarden client release version from github
    """
    module_args = {}

    tag_version = None
    url = "https://api.github.com/repos/bitwarden/clients/releases"

    headers = {
        "Accept": "application/vnd.github.v3+json",
    }

    params = {
        "per_page": 50,
    }

    page_num = 0
    is_tag_found = False

    while True:
        params["page"] = page_num
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code != 200:
            raise ValueError(
                f"Error fetching releases: {response.status_code}, {response.text}"
            )
        response_data = response.json()
        if len(response_data) == 0:
            break
        for release in response_data:
            tag_name = release["tag_name"]
            if tag_name.lower().startswith(f"{which}-"):
                is_tag_found = True
                tag_version = tag_name.replace(f"{which}-", "", 1)
                break
        if is_tag_found:
            break
        page_num += 1
        print(f"Page {page_num} processed")
    if not is_tag_found:
        raise ValueError(f"No tag found for f{which}")

    result = dict(changed=False, original_message="", message="")

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    result["msg"] = tag_version

    module.exit_json(**result)


def main():
    """
    Python Main Module
    """
    run_module()


if __name__ == "__main__":
    main()
