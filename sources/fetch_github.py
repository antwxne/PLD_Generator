#!/bin/python3

from bs4 import BeautifulSoup
from marko.ext.gfm import gfm as GithubMarkdownParser
from os import getenv
import requests

from sources.json_file import get_json_from_file, write_json


def load_name_association() -> dict:
    dest = {}
    file_path = getenv("USERS_CONFIG_PATH")
    try:
        json_list = get_json_from_file(file_path)
        for elem in json_list:
            dest[elem["user_name"]] = elem["name"]
    except (ValueError, KeyError) as e:
        print(e)
    return dest


def get_repository_list() -> list[str]:
    file_path = getenv("REPOSITORY_LIST_PATH")
    repo = []
    try:
        json_list = get_json_from_file(file_path)
        repo = [elem["repository"] for elem in json_list]
    except (ValueError, KeyError) as e:
        print(e)
    return repo


def get_issues() -> dict:
    repositories = get_repository_list()
    dest: dict[str, list[Issue]] = {}
    for repository in repositories:
        issues = fetch_issues(repository)
        for issue in issues:
            if issue.labels[0] in dest:
                dest[issue.labels[0]].append(issue)
            else:
                dest[issue.labels[0]] = [issue]
    return dest


NAME_CONVERTER = load_name_association()


class Issue:
    def __init__(self, json_response: dict):
        # print("json response == ", json_response)
        self.title = json_response["title"]
        self.labels = [label["name"] for label in json_response["labels"]]
        self.labels.remove("PLD")
        self.assignees = [NAME_CONVERTER[assignee["login"]] for assignee in json_response["assignees"]]
        self.milestone = json_response["milestone"]
        self.body = self.parse_md_body(json_response["body"])

    def to_json(self) -> dict:
        """
        It takes a class object and returns a dictionary of the class object's attributes

        Returns:
          A dictionary with the title, assignees, labels, milestone, and body of the issue.
        """
        return {
            "title": self.title,
            "assignees": self.assignees,
            "labels": self.labels,
            "milestone": self.milestone,
            "body": self.body
        }

    @staticmethod
    def parse_md_body(body: str) -> dict:
        """
        `parse_md_body` takes a string and returns a dictionary

        Args:
          body (str): The body of the markdown file.
        """
        dest = {}
        md_converted = GithubMarkdownParser(body)
        soup = BeautifulSoup(md_converted, features="lxml")
        for key in soup.findAll("h2"):
            if key.text == "Definition of done:":
                ul = key.find_next_sibling("ul")
                dest[key.text] = [elem.text for elem in ul.findAll("li")]
            else:
                p = key.find_next_sibling("p")
                dest[key.text] = p.text
        return dest


def fetch_issues(repo: str) -> list[Issue]:
    """
    It fetches issues from a GitHub repository

    Args:
      repo (str): str

    Returns:
      A list of Issue objects
    """
    res = requests.get(
        f"https://api.github.com/repos/{repo}/issues?labels=PLD",
        headers={
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f'token {getenv("OAUTH_TOKEN")}'
        }
    )
    issues = [Issue(issue) for issue in res.json()]
    return issues
