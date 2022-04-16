# PLD_Generator

## Requirements

- docker
- docker-compose
- Github OAUTH token with `repo` scope authorization

## Usage

```shell
docker-compose build
docker-compose up
```

## Config

### .env file

Please provide a `.env` file in the `config` folder.

And provide the following informations:

```
# Your github OAUTH_TOKEN
OAUTH_TOKEN=

# Path to the json file containing the users config
USERS_CONFIG_PATH=

# Path to the json file containing the general config
CONFIG_PATH=

# Path to the json file containing the repository list
REPOSITORY_LIST_PATH=
```

### USERS_CONFIG

This file contains an association between your github user_name and you real name

format: 

```json
[
  {
    "user_name": "your github user name",
    "name": "Your Name"
  }
]
```

### REPOSITORIES_CONFIG

This file contains a list of repositories

format: 

```json
[
  {
    "repository": "owner/repository"
  }
]
```

> https://github.com/owner/repository