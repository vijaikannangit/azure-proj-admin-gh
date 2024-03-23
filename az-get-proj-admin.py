import requests
from requests.auth import HTTPBasicAuth
import json

# Azure DevOps organization URL and personal access token
# organization_url = "https://dev.azure.com/YourOrganizationName"
username = ''
azure_pat = ""
org = "rakeshreddy3646"
azure_url = "https://dev.azure.com"


# Project name for which you want to fetch members of the Project Administrators group
project_name = "demo1"

# Construct organization URL
organization_url = f"{azure_url}/{org}"

# Construct projects URL
projects_url = f"{organization_url}/_apis/projects?api-version=7.1-preview.4"

# print(f'Proj Url {projects_url} / - https://dev.azure.com/rakeshreddy3646/_apis/projects?api-version=7.1-preview.4')
# print(f'PAT {azure_pat}')
try:
    # Make a GET request to retrieve projects
    response = requests.get(projects_url, auth=HTTPBasicAuth(username, azure_pat))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        projects = response.json().get("value", [])
        
        # Iterate through projects to find the desired project
        for project in projects:
            if project["name"] == project_name:
                project_id = project["id"]
                print(f'Org {org} / Project {project["name"]} / Project Id {project_id}')
                break
        else:
            # If the project was not found, print a message
            print(f"Project '{project_name}' not found.")
    else:
        # If the request was unsuccessful, print the status code and full response content
        print(f"Failed to retrieve projects for {org} - {response.status_code}")
        print("Response content:")
        print(response.content.decode("utf-8"))

except requests.exceptions.RequestException as e:
    # If a RequestException occurs (e.g., network issues), print the error message
    print(f"Request error occurred: {e}")
except Exception as e:
    # If an unexpected exception occurs, print the error message
    print(f"An unexpected error occurred: {e}")

# Get the Project Administrators group descriptor
try:
    # group_descriptor_url = f"{organization_url}/_apis/graph/groups?scopeDescriptor=vstfs://project/{project_id}&api-version=6.0"
    group_descriptor_url = f"{organization_url}/_apis/graph/groups?scopeDescriptor=vstfs://project/{project_id}&api-version=5.1-preview.1"

    response = requests.get(group_descriptor_url, auth=HTTPBasicAuth(username, azure_pat))
    response.raise_for_status()  # Raise an exception for HTTP errors
    group_descriptor_data = response.json()
    project_admins_group_descriptor = group_descriptor_data["value"][0]["descriptor"]

    # Get members of the Project Administrators group
    members_url = f"{organization_url}/_apis/graph/groups/{project_admins_group_descriptor}/members?api-version=6.0"
    response = requests.get(members_url, auth=HTTPBasicAuth(username, azure_pat))
    response.raise_for_status()  # Raise an exception for HTTP errors
    members_data = response.json()
 
    # Print members
    print("Members of the Project Administrators group:")
    for member in members_data["value"]:
        print(member["principalName"])

except requests.exceptions.RequestException as e:
    # If a RequestException occurs (e.g., network issues), print the error message
    print(f"Request error occurred: {e}")
except Exception as e:
    # If an unexpected exception occurs, print the error message
    print(f"An unexpected error occurred: {e}")

# https://dev.azure.com/rakeshreddy3646/_apis/projects/c31b66d3-b2b0-4922-984f-81281cddc891/administrators"
