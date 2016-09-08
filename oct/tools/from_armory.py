import os
import six
import requests

from oct.utilities.newproject import from_template


def download_armory(args):
    plan_name = args.plan

    results = requests.get("http://armory.theghouls.io/get-plan/%s" % plan_name)
    plan_name = plan_name.split('/')[-1]
    if results.status_code != 200:
        print("No plan found with name %s" % plan_name)
        print("Status : %s" % results.status_code)
        return None
    results = results.json()
    if not results.get('plans'):
        print("No plan found with name %s" % plan_name)
        return
    download_url = results['plans'][0]['gh_tar_url']
    file_name = os.path.join("/", "tmp", plan_name + ".tar.gz")
    r = requests.get(download_url, allow_redirects=True)
    with open(file_name, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    args.template = file_name
    from_template(args)
    os.remove(file_name)


def from_armory(sp):
    if six.PY2:
        parser = sp.add_parser('from-armory', help="create project from armory template")
    else:
        parser = sp.add_parser('from-armory', help="create project from armory template", aliases=['armory'])
    parser.add_argument('name', type=str, help="new project name")
    parser.add_argument('plan')
    parser.set_defaults(func=download_armory)
