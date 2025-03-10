import json
import os
import time

import requests
from roboflow.core.workspace import Workspace
from roboflow.core.project import Project
from roboflow.config import *


def check_key(api_key):
    """Function that takes in the user provided api_key and calls the REST API for authentication.
    :param api_key: user provided roboflow private key for authentication
    :return authenticated response
    """
    if type(api_key) is not str:
        raise RuntimeError(
            "API Key is of Incorrect Type \n Expected Type: " + str(type("")) + "\n Input Type: " + str(type(api_key)))

    response = requests.post(API_URL + "/?api_key=" + api_key)
    r = response.json()

    if "error" in r or response.status_code != 200:
        raise RuntimeError(response.text)
    else:
        return r


def auth(api_key):
    r = check_key(api_key)
    w = r['workspace']

    return Roboflow(api_key, w)


class Roboflow():
    """Roboflow class that contains all of the intiial functions to retrieve user information
    """
    def __init__(self, api_key):
        self.api_key = api_key
        self.auth()

    def auth(self):
        r = check_key(self.api_key)
        w = r['workspace']

        self.current_workspace=w

        return self

    def workspace(self, the_workspace=None):
        """Function that takes in a workspace name and returns a workspace object with appropriate information
        :param the_workspace: workspace name
        :return workspace object
        """

        if the_workspace is None:
            the_workspace = self.current_workspace

        list_projects = requests.get(API_URL + "/" + the_workspace + '?api_key=' + self.api_key).json()

        return Workspace(list_projects, self.api_key, the_workspace)

    def project(self, project_name, the_workspace=None):
        """Function that takes in the name of the project and returns the project object
        :param project_name api_key: project name
        :param the_workspace workspace name
        :return project object
        """

        if the_workspace is None:
            if "/" in project_name:
                splitted_project = project_name.rsplit("/")
                the_workspace, project_name = splitted_project[0], splitted_project[1]
            else:
                the_workspace = self.current_workspace

        dataset_info = requests.get(API_URL + "/" + the_workspace + "/" + project_name + "?api_key=" + self.api_key)

        # Throw error if dataset isn't valid/user doesn't have permissions to access the dataset
        if dataset_info.status_code != 200:
            raise RuntimeError(dataset_info.text)

        dataset_info = dataset_info.json()['project']

        return Project(self.api_key, dataset_info)

    def __str__(self):
        """to string function
        """
        json_value = {'api_key': self.api_key,
                      'workspace': self.workspace}
        return json.dumps(json_value, indent=2)