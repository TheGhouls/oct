import csv
import random
import argparse
import string


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
    email_generator_func(args.csvfile[0], args.what, args.nb_item, args.size)


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
    with open(csvfile, 'w+') as opencsv:
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
