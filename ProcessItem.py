#-*- coding:utf-8 -*-
__author__ = 'Boss'
import json
import redis


def main():
    r = redis.Redis(host='127.0.0.1', port=6378)
    while True:
        source, data = r.blpop(["CompanyInfo:items"])
        try:
            with open('res.json', 'a') as f:
                f.write(data+'\n')
            print ">>>Processing Item Successfully!"
        except KeyError:
            print u"Error proccessing:%r" % data

if __name__ == '__main__':
    main()