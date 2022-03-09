import configparser
import ast

parser = configparser.ConfigParser()
interval = []

def load_args():
    global interval
    parser.read('settings.ini')
    interval = ast.literal_eval(parser['search']['key'])
    print(interval)


def add_args(ele):
    global interval
    interval.append(ele)
    parser.set('search', 'key', str(interval))
    with open("settings.ini", "w+") as configfile:
        parser.write(configfile)
    sort


def delete_args(index):
    global interval
    interval.pop(index)
    parser.set('search', 'key', str(interval))
    with open("settings.ini", "w+") as configfile:
        parser.write(configfile)

def delete_args2(ele):
    global interval
    interval = [x for x in interval if x != ele]
    parser.set('search', 'key', str(interval))
    with open("settings.ini", "w+") as configfile:
        parser.write(configfile)

#delete_args(0)
load_args()
delete_args2('gas')

#delete_args(0)

load_args()
add_args('gas')
load_args()