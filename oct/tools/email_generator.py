import csv
import random
import string


def email_generator(xmlfile, number_of_email=15, size=6, chars=string.ascii_lowercase):
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
    with open(xmlfile, 'a') as opencsv:
        while i is not number_of_email:
            email_nick_random = ''.join(random.choice(chars) for _ in range(size))
            email_provider_random = ''.join(random.choice(chars) for _ in range(size))
            email_extention_random = ''.join(random.choice(chars) for _ in range(2, 4))
            writer = csv.writer(opencsv, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(email_nick_random + "@" + email_provider_random + "." + email_extention_random)
            i += 1
