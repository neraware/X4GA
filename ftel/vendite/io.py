#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/vendite/io.py
# Copyright:    (C) 2018 Evolvia S.r.l. <info@evolvia.srl>
# ------------------------------------------------------------------------------


import os
import urllib2
import base64

from suds.client import Client as SudsClient

import Env
import hashlib
bt = Env.Azienda.BaseTab


def get_url(path):
    
    url = Env.Azienda.BaseTab.FTEL_EEB_URL
    while path.startswith('/'):
        path = path[1:]
    if path:
        if not url.endswith('/'):
            url += '/'
        url += path
    
    return url
# 
# 
# def send_file(keydoc, filename, xml_stream):
#     
#     url = get_url('io/client?wsdl')
#     
#     client = SudsClient(url=url)
#     username = bt.FTEL_EEB_USER
#     password = hashlib.sha256(unicode(bt.FTEL_EEB_PSWD)).hexdigest()
#     xml_b64 = base64.encodestring(unicode(xml_stream).encode('utf-8'))
#     info = xml_b64+unicode(password).encode('utf-8')
#     filehash = hashlib.sha256(info).hexdigest()
#     
#     return client.service.put_file(username=username,
#                                    keydoc=keydoc,
#                                    xml_b64=xml_b64,
#                                    xml_hash=filehash,
#                                    filename=filename)
# 
# 
# def receive_notif(keydoc):
#     
#     url = get_url('io/client?wsdl')
#     
#     client = SudsClient(url=url)
#     username = bt.FTEL_EEB_USER
#     password = hashlib.sha256(unicode(bt.FTEL_EEB_PSWD)).hexdigest()
#     info = keydoc+unicode(password).encode('utf-8')
#     key_hash = hashlib.sha256(info).hexdigest()
#     
#     return client.service.put_file(username=username,
#                                    keydoc=keydoc,
#                                    key_hash=key_hash)
# 
# 
# 
# if __name__ == '__main__':
#     
#     url = 'http://mysqldb:5000/io/sdi/notifiche?wsdl'
#      
#     import simplejson as json
#     stream_test = json.dumps('pippo')
#      
#     client = SudsClient(url=url)
# #     print client.service.ricevutaConsegna(IdentificativoSdI=123,
# #                                           NomeFile='ID01234567890',
# #                                           File=stream_test)
# #     print client.service.notificaMancataConsegna(IdentificativoSdI=123,
# #                                           NomeFile='ID01234567890',
# #                                           File=stream_test)
#     print client.service.notificaScarto(IdentificativoSdI=123,
#                                           NomeFile='ID01234567890',
#                                           File=stream_test)
# #     print client.service.notificaEsito(IdentificativoSdI=123,
# #                                           NomeFile='ID01234567890',
# #                                           File=stream_test)
# #     print client.service.notificaDecorrenzaTermini(IdentificativoSdI=123,
# #                                           NomeFile='ID01234567890',
# #                                           File=stream_test)
# # 
# # 
# #     url = 'http://mysqldb:5000/io/sdi/ricezione?wsdl'
# #      
# #     client = SudsClient(url=url)
# #     print client.service.RiceviFatture()
