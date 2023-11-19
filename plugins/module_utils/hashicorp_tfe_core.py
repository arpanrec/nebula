"""Terraform Cloud Resource Manage"""
import requests


def tfe_resource(
    resource_url: str = None,
    resource_name: str = None,
    headers: dict = None,
    resource_type: str = None,
    resource_attributes: str = None,
    result=None,
) -> dict:
    """Terraform Cloud Resource Manage"""
    _resource_url_name = f"{resource_url}/{resource_name}"
    _resource_details_response = requests.get(
        _resource_url_name, timeout=30, headers=headers
    )
    result[f"{resource_type}_{resource_name}_created"] = False
    result[f"{resource_type}_{resource_name}_updated"] = False
    if _resource_details_response.status_code == 200:
        _resource_details = _resource_details_response.json()
    elif _resource_details_response.status_code == 404:
        _resource_create_data = {"data": {"type": resource_type, "attributes": {}}}
        if resource_attributes and len(resource_attributes) > 0:
            _resource_create_data["data"]["attributes"] = resource_attributes
        _resource_create_data["data"]["attributes"]["name"] = resource_name
        _tfe_resource_create_response = requests.post(
            resource_url,
            timeout=30,
            headers=headers,
            json=_resource_create_data,
        )
        if _tfe_resource_create_response.status_code == 201:
            result["changed"] = True
            result[f"{resource_type}_{resource_name}_created"] = True
            _tfe_newly_created_resource_details_response = requests.get(
                _resource_url_name, timeout=30, headers=headers
            )
            if _tfe_newly_created_resource_details_response.status_code == 200:
                _resource_details = _tfe_newly_created_resource_details_response.json()
            else:
                result["error"] = {
                    "status": _tfe_newly_created_resource_details_response.status_code,
                    "msg": _tfe_newly_created_resource_details_response.json(),
                }
                return result
        else:
            result["error"] = {
                "status": _tfe_resource_create_response.status_code,
                "msg": _tfe_resource_create_response.json(),
            }
            return result
    else:
        result["error"] = {
            "status": _resource_details_response.status_code,
            "msg": _resource_details_response.json(),
        }
        return result

    if not result[f"{resource_type}_{resource_name}_created"]:
        if resource_attributes and len(resource_attributes) > 0:
            _existing_attributes = _resource_details["data"]["attributes"]
            for attribute in resource_attributes.keys():
                if (
                    attribute not in _existing_attributes.keys()
                    or resource_attributes[attribute] != _existing_attributes[attribute]
                ):
                    _org_update_data = {
                        "data": {
                            "type": "organizations",
                            "attributes": resource_attributes,
                        }
                    }
                    _org_update_response = requests.patch(
                        _resource_url_name,
                        timeout=30,
                        headers=headers,
                        json=_org_update_data,
                    )
                    if _org_update_response.status_code == 200:
                        result["changed"] = True
                        result[f"{resource_type}_{resource_name}_updated"] = True
                        _tfe_org_updated_details_response = requests.get(
                            _resource_url_name, timeout=30, headers=headers
                        )
                        if _tfe_org_updated_details_response.status_code == 200:
                            _resource_details = _tfe_org_updated_details_response.json()
                        else:
                            result["error"] = {
                                "status": _tfe_org_updated_details_response.status_code,
                                "msg": _tfe_org_updated_details_response.json(),
                            }
                            return result
                        break

                    result["error"] = {
                        "status": _org_update_response.status_code,
                        "msg": _org_update_response.json(),
                    }
                    return result
    result[f"{resource_type}"] = _resource_details
    return result


def crud(
    hostname=None,
    token=None,
    organization=None,
    organization_attributes=None,
    workspace=None,
    workspace_attributes=None,
) -> dict:
    """Terraform Cloud Resource Manage"""
    result = {
        "changed": False,
    }
    headers = {
        "Accept": "application/vnd.github+json",
        "content-type": "application/vnd.api+json",
        "Authorization": f"Bearer {token}",
    }
    if not hostname:
        result["error"] = "Hostname Can not be null"
        return result
    if not organization:
        result["error"] = "organization Can not be null"
        return result
    if not workspace:
        result["error"] = "workspace Can not be null"
        return result
    result_organization = tfe_resource(
        resource_url=f"https://{hostname}/api/v2/organizations",
        resource_name=organization,
        headers=headers,
        resource_type="organizations",
        resource_attributes=organization_attributes,
        result=result,
    )
    if "error" in result_organization.keys():
        return result_organization
    result_workspace = tfe_resource(
        resource_url=f"https://{hostname}/api/v2/organizations/{organization}/workspaces",
        resource_name=workspace,
        headers=headers,
        resource_type="workspaces",
        resource_attributes=workspace_attributes,
        result=result_organization,
    )
    return result_workspace
