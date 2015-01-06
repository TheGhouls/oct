from __future__ import absolute_import
import argparse
from xml.dom.minidom import parse
import csv


def sitemap_to_csv():
    """
    Take as options: Xml file, CSV File

    Parse the XML and write each value get from it inside the CSV file provided.
    :return: None
    """
    parser = argparse.ArgumentParser(description="Convert XML file to CSV file")
    parser.add_argument("xml", metavar='xml', type=str, nargs=1, help="The XML file to parse")
    parser.add_argument("csv", metavar='csv', type=str, nargs=1, help="The CSV file to generate")
    args = parser.parse_args()

    try:
        datasource = open(args.xml[0], "r")
        dom = parse(datasource)
    except IOError:
        raise IOError("Bad XML file provided")

    with open(args.csv[0], 'wb') as opencsv:
        urls = dom.getElementsByTagName('url')
        for url in urls:
            writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([url.getElementsByTagName('loc')[0].firstChild.nodeValue])