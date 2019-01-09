#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/dbtables.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2018 Evolvia S.r.l.
# ------------------------------------------------------------------------------
# This file is part of X4GA
# 
# X4GA is free software: you can redistribute it and/or modify
# it under the terms of the Affero GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# X4GA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with X4GA.  If not, see <http://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------


import stormdb as adb
import glob

from ftel.acquisti.ftel_read import FTEL_Doc
import os
import Env
from Env import opj
from awc.controls.attachbutton import _AttachTableMixin

from suds.client import Client as SudsClient
import hashlib
import base64


class ElencoFiles(adb.DbMem, _AttachTableMixin):
    
    gateway_client = None
    
    def __init__(self, fields=None, primaryKey=None, mandatoryFields="", 
        defaults=None):
        adb.DbMem.__init__(self, fields='fullname filename pdc_id pdc_codice pdc_descriz tipdoc datdoc numdoc totdoc docinfo docxml'.split())
        
        pdc = adb.DbTable('pdc')
        pdc.AddJoin('pdctip', 'tipana', idLeft='id_tipo')
        pdc.AddJoin('fornit', 'anag', idLeft='id')
        pdc.AddBaseFilter('tipana.tipo="F"')
        pdc.AddOrder('pdc.codice', adb.ORDER_DESCENDING)
        self.pdc = pdc
    
    def update_list(self):
        
        self.Reset()
        
        pdc = self.pdc
        path = ElencoFiles.get_basepath()
        files = glob.glob(opj(path, '*.xml'))
        files.sort()
        
        for n, fullname in enumerate(files):
            f = FTEL_Doc(fullname)
            filename = fullname.replace('\\', '/')
            filename = filename[filename.rfind('/')+1:]
            for doc in f.docs:
                self.CreateNewRow()
                self.fullname = fullname
                self.filename = filename
                self.tipdoc = doc.tipdoc
                self.datdoc = doc.datdoc
                self.numdoc = doc.numdoc
                self.totdoc = doc.totdoc
                self.docinfo = doc
                self.docxml = f
                self.pdc_descriz = f.anag_fornit.descriz
                pdc.Retrieve('anag.piva=%s', f.anag_fornit.piva)
    
    def archive_file(self):
        
        h = open(self.fullname, 'r')
        stream = h.read()
        h.close()
        
        doc = FTEL_Doc(stream=stream)
        year = doc.docs[0].datdoc.year
        path = self.get_basepath(arc=True, subpath=str(year))
        filearc = opj(path, self.filename)
        h = open(filearc, 'w')
        h.write(stream)
        h.close()
        
        os.remove(self.fullname)
    
    def acquis_fornit(self):
        
        pdc = self.pdc
        tpa = adb.DbTable('pdctip', 'tipana')
        tpa.AddJoin('pdcrange')
        
        f = FTEL_Doc(self.fullname)
        pdc.Retrieve('anag.piva=%s', f.anag_fornit.piva)
        
        if pdc.IsEmpty():
            
            auto = adb.DbTable('cfgautom')
            auto.Retrieve('codice=%s', 'pdctip_fornit')
            id_tipana = auto.aut_id
            tpa.Get(id_tipana)
            auto.Retrieve('codice=%s', 'bilmas_fornit')
            id_bilmas = auto.aut_id
            auto.Retrieve('codice=%s', 'bilcon_fornit')
            id_bilcon = auto.aut_id
            pdc.AddFilter('pdc.codice>=%s AND pdc.codice<=%s', 
                          tpa.pdcrange.rangemin,
                          tpa.pdcrange.rangemax)
            pdc.Retrieve()
            if pdc.IsEmpty():
                lastnum = tpa.pdcrange.rangemin
            else:
                lastnum = int(pdc.codice or '')
            newcod = str(lastnum+1)
            pdc.CreateNewRow()
            pdc.codice = str(newcod).zfill(5)
            pdc.descriz = self.pdc_descriz
            pdc.id_tipo = id_tipana
            pdc.id_bilmas = id_bilmas
            pdc.id_bilcon = id_bilcon
            if not pdc.Save():
                raise Exception(repr(pdc.GetError()))
            
            cmd = r"""
                INSERT INTO fornit (id, indirizzo, cap, citta, prov, codfisc, nazione, piva, sm11_cognome, sm11_nome, numtel, numfax, email)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            if not pdc._info.db.Execute(cmd, (pdc.id,
                                              f.anag_fornit.indirizzo,
                                              f.anag_fornit.cap,
                                              f.anag_fornit.citta,
                                              f.anag_fornit.prov,
                                              f.anag_fornit.codfisc,
                                              f.anag_fornit.paese,
                                              f.anag_fornit.piva,
                                              f.anag_fornit.cognome,
                                              f.anag_fornit.nome,
                                              f.anag_fornit.numtel,
                                              f.anag_fornit.numfax,
                                              f.anag_fornit.email,)):
                raise Exception(pdc._info.dbError.description)
    
    @classmethod
    def get_basepath(cls, arc=False, subpath=''):
        try:
            path = Env.Azienda.config.get('Site', 'folder')  # @UndefinedVariable
        except:
            path = None
        if not path:
            path = Env.xpaths.GetConfigPath()
        path = opj(path, 'ftel')
        if not os.path.isdir(path):
            os.mkdir(path)
        path = opj(path, 'azienda_%s' % Env.Azienda.codice)
        if not os.path.isdir(path):
            os.mkdir(path)
        path = opj(path, 'acquisti')
        if not os.path.isdir(path):
            os.mkdir(path)
        if arc:
            path = opj(path, 'archiviati')
            if not os.path.isdir(path):
                os.mkdir(path)
        if subpath:
            path = opj(path, subpath)
            if not os.path.isdir(path):
                os.mkdir(path)
        return path
    
    @classmethod
    def gateway_get_url(cls, path):
        
        url = Env.Azienda.BaseTab.FTEL_EEB_URL
        while path.startswith('/'):
            path = path[1:]
        if path:
            if not url.endswith('/'):
                url += '/'
            url += path
        
        return url
    
    def gateway_get_client(self):
        if self.gateway_client is None:
            url = self.gateway_get_url('io/client/acquisti?wsdl')
            self.gateway_client = SudsClient(url=url)
        return self.gateway_client
    
    def gateway_get_info(self):
        
        client = self.gateway_get_client()
        username = Env.Azienda.BaseTab.FTEL_EEB_USER
        piva = Env.Azienda.piva
        password = hashlib.sha256(unicode(Env.Azienda.BaseTab.FTEL_EEB_PSWD)).hexdigest()
        info = piva+unicode(password).encode('utf-8')
        _hash = hashlib.sha256(info).hexdigest()
        
        resp = client.service.get_info(username=username,
                                       piva=piva,
                                       hash=_hash)
        if resp['result'] == "OK":
            out = {'numdocs': resp['numdocs'],}
            if resp['doc_ids'] is None:
                out['doc_ids'] = []
            else:
                out['doc_ids'] = map(int, resp['doc_ids'].split(','))
            return out
        
        raise Exception(resp['error'])
    
    def gateway_get_documento(self, id_doc):
        
        client = self.gateway_get_client()
        username = Env.Azienda.BaseTab.FTEL_EEB_USER
        piva = Env.Azienda.piva
        password = hashlib.sha256(unicode(Env.Azienda.BaseTab.FTEL_EEB_PSWD)).hexdigest()
        info = piva+str(id_doc)+unicode(password).encode('utf-8')
        _hash = hashlib.sha256(info).hexdigest()
        
        resp = client.service.get_documento(username=username,
                                            piva=piva,
                                            id_doc=id_doc,
                                            hash=_hash)
        
        if resp['result'] == "OK":
            filename = resp['filename']
            xml_stream = base64.b64decode(resp['xml_stream'])
            self.get_basepath()
            fullname = os.path.join(self.get_basepath(), filename)
            f = open(fullname, 'w')
            f.write(xml_stream)
            f.close()
            return filename
        
        raise Exception(resp['error'])


class RigheDbMem(adb.DbMem):
    
    def __init__(self):
        fields = 'numriga codart descriz qta unimis prezzo sconto_pe1 sconto_pe2 sconto_pe3 sconto_pe4 sconto_pe5 sconto_pe6 sconto_val totale aliqiva'.split()
        adb.DbMem.__init__(self, fields=fields)
    
    def get_descriz_sconto(self):
        sconti = []
        for n in range(1,6,1):
            s = getattr(self, 'sconto_pe%d' % n)
            if s:
                if s == int(s):
                    sconti.append(str(int(s)))
                else:
                    sconti.append(adb.DbTable.sepn(s, 2))
        if sconti:
            return '+'.join(sconti)
        if self.sconto_val:
            return adb.DbTable.sepnvi(self.sconto_val)
    
    def get_descriz_aliqiva(self):
        aliqiva = self.aliqiva
        if self.aliqiva and ('%.2f' % self.aliqiva).endswith('.00'):
            aliqiva = int(self.aliqiva)
        return str(aliqiva)
