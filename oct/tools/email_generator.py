import csv
import random
import argparse
import string
import sys


def email_generator():
    """
    Command line tool for generating csv file containing user / password pairs

    :return: None
    """
    parser = argparse.ArgumentParser(description="Check if user or email created")
    parser.add_argument("csvfile", metavar='csvfile', type=str, nargs=1, help="The CSV file provided")
    parser.add_argument("-n", metavar='nb_item',
                        type=int, nargs='?', help="Nb of item(s) generated", default=250, dest='nb_item')
    parser.add_argument("-s", metavar='size', type=int, nargs='?', help="Size of each item(s)", default=6,
                        dest='size')
    parser.add_argument("-w", metavar='type', type=str, nargs='?', help="Create Email or Login (e: email, u:user)",
                        default='e', dest='what')
    args = parser.parse_args()

    chars = string.ascii_lowercase
    i = 0
    with open(args.csvfile[0], 'a') as opencsv:
        sys.stdout.write('\n')
        while i <= args.nb_item:
            sys.stdout.write("{0}/{1}\r".format(i, args.nb_item))
            sys.stdout.flush()
            rand = ''.join(random.choice(chars) for _ in range(args.size))
            pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(args.size))
            if args.what == 'e':
                email_extention_random = ''.join(random.choice(chars) for _ in range(2, 4))
                writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([rand + "@" + rand + "." + email_extention_random + ";" + pwd])
            else:
                writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([rand + ";" + pwd])
            i += 1
        sys.stdout.write('\n\n')


def email_generator_func(csvfile, what, number_of_email=15, size=6, chars=string.ascii_lowercase):
    """

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
