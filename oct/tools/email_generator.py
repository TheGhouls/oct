import csv
import random
import argparse
import string


def email_generator():
    """
    :param xmlfile: name of XML file provided
    :type xml file: xml formated text file
    :param number_of_email: Number of random generated email
    :type: int
    :param size: number of char generated
    :type: int
    :param chars: lower the generated char
    :type: string
    :return: None
    """
    parser = argparse.ArgumentParser(description="Check if user or email created")
    parser.add_argument("csvfile", metavar='csvfile', type=str, nargs=1, help="The CSV file provided")
    parser.add_argument("nb_item", metavar='email', type=str, nargs=1, help="Nb of item(s) generated")
    parser.add_argument("size", metavar='size', type=int, nargs=1, help="Size of each item(s)")
    parser.add_argument("what", metavar='email', type=str, nargs=1, help="Create Email or User")
    args = parser.parse_args()

    chars = string.ascii_lowercase
    i = 0
    with open(args.csvfile[0], 'a') as opencsv:
        while i is not args.nb_item[0]:
            rand = ''.join(random.choice(chars) for _ in range(args.size[0]))
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(args.size[0]))
            if args.what[0] == 'e':
                email_extention_random = ''.join(random.choice(chars) for _ in range(2, 4))
                writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([rand + "@" + rand + "." + email_extention_random + ";" + pwd])
            else:
                writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([rand + ";" + pwd])
            i += 1


def email_generator_func(csvfile, what, number_of_email=15, size=6, chars=string.ascii_lowercase):
    """
    :param xmlfile: name of XML file provided
    :type xml file: xml formated text file
    :param number_of_email: Number of random generated email
    :type: int
    :param size: number of char generated
    :type: int
    :param chars: lower the generated char
    :type: string
    :return: None
    """


    i = 0
    with open(csvfile, 'a') as opencsv:
        while i is not number_of_email:
            rand = ''.join(random.choice(chars) for _ in range(size))
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(size))
            if what == 'e':
                email_extention_random = ''.join(random.choice(chars) for _ in range(2, 4))
                writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([rand + "@" + rand + "." + email_extention_random + ";" + pwd])
            else:
                writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([rand + ";" + pwd])
            i += 1
