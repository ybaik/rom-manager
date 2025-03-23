import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

from typing import Dict
from pathlib import Path
from common.tags import XML_TAGS


def read_xml(path: Path) -> Dict:
    """
    Read game data from an XML file and return it as a dictionary.

    :param path: A Path object pointing to the XML file to be read.
    :return: A dictionary where each key is a game ID (derived from the 'path' attribute) and each value is a dictionary of game attributes.
             Returns None if the file does not exist or if there is an error parsing the XML.
    """
    if not path.exists():
        print(f"File not found: {path}")
        return None

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None

    games = {}
    for game in root.findall("game"):
        g = {tag: elem.text for tag in XML_TAGS if (elem := game.find(tag)) is not None}

        if game.get("id") is not None:
            g["id"] = int(game.get("id"))
        key = g.get("path", "").replace("./", "")
        if key:
            key = Path(key).stem
            games[key] = g

    return games


def indent(elem: ET.Element, level: int = 0) -> None:
    i = "\n" + level * "\t"
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "\t"
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def save_xml(data: Dict, path: Path) -> None:
    """
    Save a dictionary of game data to an XML file.

    :param data: A dictionary where each key is a game ID and each value is a dictionary of game attributes.
    :param path: A Path object pointing to the file where the XML should be saved.
    """
    root = ET.Element("gameList")
    for key, info in data.items():
        element = ET.Element("game")
        root.append(element)

        for tag in XML_TAGS:
            if tag in info:
                sub_element = ET.SubElement(element, tag)
                sub_element.text = str(info[tag])  # Ensure the text is a string
        ET.SubElement(element, "scrap", name="ScreenScraper", date="300001011T000000")

    indent(root)
    tree = ET.ElementTree(root)
    tree.write(path, encoding="utf-8", xml_declaration=True)


def read_csv(path: Path) -> Dict:
    if not path.exists():
        print("File not found")
        return None

    df = pd.read_csv(path, dtype=str)
    head = df.columns.values.tolist()

    games = dict()
    for i, row in df.iterrows():
        g = dict()
        zip_path = row.path
        for tag in head:
            val = row[tag]
            if val is np.nan:
                continue
            g[tag] = row[tag]
        games[zip_path] = g
    return games
