#!/bin/python3

from os import getenv
from sources.json_file import get_json_from_file
from sources.document_utils import (add_title_center, add_picture_center, add_title, save, page_break, create_array)
from datetime import date

CONFIG_PATH = getenv("CONFIG_PATH")
RESOURCES_FOLDER = getenv("RESOURCES_FOLDER")


def create_cover_page(config: dict) -> None:
    cover_image = f'{RESOURCES_FOLDER}/{config["cover-image"]["path"]}'
    size = config["cover-image"]["size"]
    add_picture_center(cover_image, width=size["width"], height=size["height"])
    add_title_center(config["title"], level=0)
    add_title_center(config["sub-title"], level=1)
    page_break()


def create_document_description(description: dict) -> None:
    add_title("Description du document")
    array = create_array(9, 2)
    array.rows[0].cells[0].text = "Titre"
    array.rows[0].cells[1].text = description["Titre"]
    array.rows[1].cells[0].text = "Objet"
    array.rows[1].cells[1].text = description["Objet"]
    array.rows[2].cells[0].text = "Auteur"
    array.rows[2].cells[1].text = description["Auteur"]
    array.rows[3].cells[0].text = "Responsable"
    array.rows[3].cells[1].text = description["Responsable"]
    array.rows[4].cells[0].text = "E-mail"
    array.rows[4].cells[1].text = description["E-mail"]
    array.rows[5].cells[0].text = "Mots-clés"
    array.rows[5].cells[1].text = ", ".join(list(description["Mots-clés"]))
    array.rows[6].cells[0].text = "Promotion"
    array.rows[6].cells[1].text = description["Promotion"]
    array.rows[7].cells[0].text = "Date de mise à jour"
    array.rows[7].cells[1].text = date.today().strftime("%d/%m/%Y")
    array.rows[8].cells[0].text = "Version du modèle"
    array.rows[8].cells[1].text = "1.0"
    page_break()


def create_document():
    config = get_json_from_file(CONFIG_PATH)
    create_cover_page(config)
    create_document_description(config["description"])
    save(RESOURCES_FOLDER + "/" + config["document_name"])
