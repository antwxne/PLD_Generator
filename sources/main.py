#!/bin/python3

from sources.fetch_github import fetch_issues
from os import getenv
from sources.json_file import get_json_from_file
from sources.document_generator import create_document


def get_repository_list() -> list[str]:
    file_path = getenv("REPOSITORY_LIST_PATH")
    repo = []
    try:
        json_list = get_json_from_file(file_path)
        repo = [elem["repository"] for elem in json_list]
    except (ValueError, KeyError) as e:
        print(e)
    return repo


if __name__ == "__main__":
    # repositories = get_repository_list()
    #
    # for repository in repositories:
    #     issues = fetch_issues(repository)
    #     for issue in issues:
    #         print(issue.to_json())
    create_document()
