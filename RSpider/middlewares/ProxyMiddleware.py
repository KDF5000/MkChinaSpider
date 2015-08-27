# -*- coding:utf-8 -*-
__author__ = 'Boss'


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        proxy = "222.88.144.12:8118"
        try:
            request.meta['proxy'] = "http://%s" % proxy
        except Exception, e:
            print "<<<<<Exception: %s" % e.message

