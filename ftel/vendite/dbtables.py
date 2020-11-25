#!/bin/env/python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         fatturpa_magazz/dbtables.py
# Copyright:    (C) 2018 Evolvia S.r.l. <info@evolvia.srl>
# ------------------------------------------------------------------------------

import magazz.dbtables as dbm
import stormdb as adb

import Env

from xml.dom.minidom import Document
import re

import os
from magazz.dbtables import BodyFtelADG
from stormdb import JOIN_LEFT
import version
import simplejson
def opj(*x):
    return os.path.join(*x).replace('\\', '/')

import report as rpt
from cStringIO import StringIO
import base64

from suds.client import Client as SudsClient
import hashlib

import zipfile


FTEL_NOCODE = '0000000'

class FatturaElettronicaException(Exception):
    pass


def normalize(x, upper=False):
    c = True
    x = x.encode('ascii', 'xmlcharrefreplace')
    if upper:
        x = x.upper()
    y = ''
    for n in range(len(x)):
        if x[n] == '.':
            c = True
        if c and x[n].isalpha():
            y += x[n].upper()
            c = False
        elif x[n].isalnum() or x[n].isspace():
            y += x[n]
    return y


def fmt_qt(x):
    mask = '%%.%df' % max(2,Env.Azienda.BaseTab.MAGQTA_DECIMALS)
    return mask % x

def fmt_pr(x, dp=None):
    if dp is None:
        dp = Env.Azienda.BaseTab.MAGPRE_DECIMALS
    mask = '%%.%df' % dp
    return mask % x

def fmt_sc(x):
    mask = '%%.%df' % 2
    return mask % x

def fmt_arrot(x):
    mask = '%%.%df' % 10
    return mask % x

def fmt_ii(x):
    mask = '%%.%df' % Env.Azienda.BaseTab.VALINT_DECIMALS
    return mask % x


class FatturaElettronica(dbm.DocMag):
    
    STATUS_XML_DA_GENERARE = 'X'
    
    #senza gateway
    STATUS_XML_GENERATO =    'G'
    
    #con gateway
    STATUS_ATTESA_ESITO =    'A'
    STATUS_IN_CODA_X_SDI =   'Q'
    STATUS_CONSEGNATO =      'C'
    STATUS_MANCATACONS =     'M'
    STATUS_ERRORE =          'E'
    STATUS_PA_ACCETTATI =    'Z'
    STATUS_PA_RIFIUTATI  =   'K'
    STATUS_PA_DECOTERM =     'T'
    
    STATUS_COLORS = {STATUS_XML_DA_GENERARE: 'lemonchiffon',
                     STATUS_XML_GENERATO:    'dodgerblue1',
                     STATUS_ATTESA_ESITO:    'bisque',
                     STATUS_IN_CODA_X_SDI:   'plum1',
                     STATUS_CONSEGNATO:      'turquoise1',
                     STATUS_MANCATACONS:     'seagreen1',
                     STATUS_ERRORE:          'darkorange1',
                     STATUS_PA_ACCETTATI:    'olivedrab1',
                     STATUS_PA_RIFIUTATI:    'chocolate',
                     STATUS_PA_DECOTERM:     'seashell3',}
    
    COLOR_STATUS_DA_INVIARE_AL_GATEWAY = 'darkseagreen'
    
    COLOR_DATI_MANCANTI = 'sienna1'
    
    stampaDescriz = None
    
    def __init__(self, *args, **kwargs):
        dbm.DocMag.__init__(self, *args, **kwargs)
        self['pdc'].AddJoin('clienti', 'anag', idLeft='id', join=JOIN_LEFT)
        self['pdc'].AddJoin('fornit', 'anafor', idLeft='id', join=JOIN_LEFT)
        self.AddBaseFilter('(regiva.tipo="V" AND (caucon.ftel_tipdoc IS NOT NULL AND caucon.ftel_tipdoc<>"")) OR config.ftel_autacq IS TRUE')
        self.Reset()
        self.SetDebug()
        
        self.dbcfg = dbm.adb.DbTable('cfgsetup', 'setup')        
        self.dbcfg.Retrieve('setup.chiave=%s', 'azienda_ftel_flagdescriz')
        if self.dbcfg.OneRow():
            self.stampaDescriz=(int(self.dbcfg.flag)==1)
        self._info.displayonly = True #no ricalcolo in lettura doc.
        
        self.gateway_client = None
    
    @classmethod
    def ftel_get_name(cls, numprogr):
        return 'IT%s_%s' % (Env.Azienda.codfisc, str(numprogr).zfill(5))
    
    @classmethod
    def ftel_get_basepath(cls):
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
        path = opj(path, 'vendite')
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
    
    @classmethod
    def ftel_get_pathname(cls, year):
#         path = cls.ftel_get_basepath()
#         if not Env.Azienda.BaseTab.is_eeb_enabled():
#             path = opj(path, cls.ftel_get_name(numprogr))
#             if not os.path.isdir(path):
#                 os.mkdir(path)
#         return path
        path = cls.ftel_get_basepath()
        path = os.path.join(path, str(year))
        if not os.path.isdir(path):
            os.mkdir(path)
        return path
    
#     @classmethod
#     def ftel_get_filename(cls, numprogr, ext='xml'):
#         path = cls.ftel_get_pathname(numprogr)
#         name = cls.ftel_get_name(numprogr)
#         return opj(path, '%s.%s' % (name, ext))
#     
    def ftel_get_filename(self, numprogr, year, ext='xml'):
        path = self.ftel_get_pathname(year)
        name = self.ftel_get_name(numprogr)
        return opj(path, '%s.%s' % (name, ext))
    
    def ftel_get_datiazienda(self):
        cfg = dbm.adb.DbTable('cfgsetup', 'setup')
        dataz = {}
        for name in """cognome nome regfisc reanum reauff """\
                    """soind socap socit sopro capsoc socuni socliq """\
                    """rfnome rfcognome rfdes rfind rfcap rfcit rfpro rfcodfis rfpiva """\
                    """trcodfis trstato """\
                    """senome secognome sedes secodfis sepiva sestato setit seeori sesogemi """\
                    """cassaprev""".split():
            cfg.Retrieve('setup.chiave=%s', 'azienda_ftel_%s' % name)
            if name == 'sesogemi':
                if cfg.flag == "C":
                    dataz[name] = "CC"
                elif cfg.flag == "T":
                    dataz[name] = "TZ"
                else:
                    dataz[name] = ""
            else:
                if cfg.importo:
                    dataz[name] = cfg.importo
                else:
                    dataz[name] = cfg.descriz
        return dataz
    
    def get_keydoc(self):
        if version.VERSION_STRING >= '1.9.84':
            return '%s-%s' % (Env.Azienda.piva, self.id)
        return str(self.id)
    
    def ftel_make_files(self, numprogr, pa_callback):
        
        def si_no(test, v1="SI", v2="NO"):
            if test:
                return v1
            return v2
        
        def data(data):
            try:
                return data.strftime('%Y-%m-%d')
            except:
                return ''
        
        if self.IsEmpty():
            raise FatturaElettronicaException, "Il documento è vuoto"
        
        dataz = self.ftel_get_datiazienda()
        
        pdc = self.pdc
        cli = self.GetAnag()
        
        if not cli.nazione or cli.nazione == "IT":
            ftel_nocode = '0000000'
        else:
            ftel_nocode = 'XXXXXXX'
        
        ftel_codice = self.pdc.ftel_codice or ftel_nocode
        is_pa = len(ftel_codice) == 6
        
        xmldoc = FTEL_Document()
        dbadg = BodyFtelADG()
        
        fat = xmldoc.createRoot(is_pa=is_pa)
        
        # 1 <FatturaElettronicaHeader>
        head = xmldoc.appendElement(fat, 'FatturaElettronicaHeader')
        
        # 1.1 <DatiTrasmissione>
        datitrasm = xmldoc.appendElement(head, 'DatiTrasmissione')
        
        # 1.1.1 <IdTrasmittente>
        idtrasm = xmldoc.appendElement(datitrasm, 'IdTrasmittente')
        if dataz['trcodfis']:
            trcodfis = dataz['trcodfis']
            trstato = dataz['trstato'] or "IT"
        else:
            trcodfis = Env.Azienda.codfisc or Env.Azienda.piva
            trstato = Env.Azienda.stato or "IT"
        xmldoc.appendItems(idtrasm, (('IdPaese',  trstato),
                                     ('IdCodice', trcodfis),))
        
        # 1.1.2 <ProgressivoInvio>
        xmldoc.appendItems(datitrasm, (('ProgressivoInvio',    str(numprogr).zfill(5)),
                                       ('FormatoTrasmissione', xmldoc.sdicver),))
        
        if self.config.ftel_autacq:
            
            # documento di autofattura per acquisto da soggetti esonerati dall'obbligo della fatturazione:
            # nel file xml il fornitore è l'azienda, il cliente è l'anafgrafica del documento (il vero fornitore)
            
            ftel_tipdoc = self.config.ftel_aacqtd or ''
            if not ftel_tipdoc.startswith('TD'):
                raise Exception("Errata definizione tipo documento xml")
            
            # 1.1.5 <ContattiTrasmittente>
            xmldoc.appendItems(datitrasm, (('CodiceDestinatario',  ftel_codice),))
            
            # 1.2 <CedentePrestatore>
            cedente = xmldoc.appendElement(head, 'CedentePrestatore')
            
            # 1.2.1 <DatiAnagrafici>
            cedente_datianag = xmldoc.appendElement(cedente, 'DatiAnagrafici')
            
            # 1.2.1.1 <IdFiscaleIVA>
            cedente_datianag_datifisc = xmldoc.appendElement(cedente_datianag, 'IdFiscaleIVA')
            xmldoc.appendItems(cedente_datianag_datifisc, (('IdPaese',  cli.nazione or "IT"),
                                                           ('IdCodice', cli.piva)))
    #         if Env.Azienda.codfisc:
            if cli.codfisc and cli.codfisc != cli.piva:
                # 1.2.1.2 <CodiceFiscale>
                xmldoc.appendItems(cedente_datianag, (('CodiceFiscale', cli.codfisc),))
            
            # 1.2.1.3 <Anagrafica>
            cedente_datianag_anagraf = xmldoc.appendElement(cedente_datianag, 'Anagrafica')
            dati = []
            if True:
#             if dataz['cognome']:
#                 dati.append(('Nome', dataz['nome']))
#                 dati.append(('Cognome', dataz['cognome']))
#             else:
                dati.append(('Denominazione', pdc.descriz))
            xmldoc.appendItems(cedente_datianag_anagraf, dati)
            
            # 1.2.1.8 <RegimeFiscale>
            if not 1 <= int(pdc.ftel_regfisc or 0) <= 19:
                raise Exception("Manca indicazione del regime fiscale su %s" % pdc.descriz)
            xmldoc.appendItems(cedente_datianag, (('RegimeFiscale', "RF%s" % pdc.ftel_regfisc.zfill(2)),))
            
            # 1.2.2 <Sede>
            cedente_sede = xmldoc.appendElement(cedente, 'Sede')
            xmldoc.appendItems(cedente_sede, (('Indirizzo', cli.indirizzo),
                                              ('CAP',       cli.cap),
                                              ('Comune',    cli.citta),
                                              ('Provincia', cli.prov),
                                              ('Nazione',   cli.nazione or "IT"),))
            
            # 1.4 <CessionarioCommittente>
            cessionario = xmldoc.appendElement(head, 'CessionarioCommittente')
            
            # 1.4.1 <DatiAnagrafici>
            cessionario_datianag = xmldoc.appendElement(cessionario, 'DatiAnagrafici')
            if cli.piva:
                # 1.4.1.1 <IdFiscaleIVA>
                cessionario_datianag_idf = xmldoc.appendElement(cessionario_datianag, 'IdFiscaleIVA')
                xmldoc.appendItems(cessionario_datianag_idf, (('IdPaese',  Env.Azienda.stato or "IT"),
                                                              ('IdCodice', Env.Azienda.piva)),)
    #         if cli.nazione == 'IT' or len(cli.nazione or '') == 0:
    #             # 1.4.1.2 <CodiceFiscale>
    #             xmldoc.appendItems(cessionario_datianag, (('CodiceFiscale', cli.codfisc or cli.piva),))
    #         
            if Env.Azienda.codfisc and Env.Azienda.codfisc != Env.Azienda.piva:
                # 1.4.1.2 <CodiceFiscale>
                xmldoc.appendItems(cessionario_datianag, (('CodiceFiscale', Env.Azienda.codfisc),))
            
            # 1.4.1.3 <Anagrafica>
            cessionario_datianag_anagraf = xmldoc.appendElement(cessionario_datianag, 'Anagrafica')
            xmldoc.appendItems(cessionario_datianag_anagraf, (('Denominazione', Env.Azienda.descrizione),))
            
            #1.4.2 <Sede>
            cessionario_sede = xmldoc.appendElement(cessionario, 'Sede')
            xmldoc.appendItems(cessionario_sede, (('Indirizzo', Env.Azienda.indirizzo),
                                                  ('CAP',       Env.Azienda.cap),
                                                  ('Comune',    Env.Azienda.citta),
                                                  ('Provincia', Env.Azienda.prov),
                                                  ('Nazione',   Env.Azienda.stato or "IT"),))
            
            #1.6 <SoggettoEmittente>
            xmldoc.appendItems(head, (('SoggettoEmittente', "CC"),))
            
        else:
            
            # documento di vendita normale
            
            ftel_tipdoc = self.config.caucon.ftel_tipdoc
            
            # 1.1.5 <ContattiTrasmittente>
            xmldoc.appendItems(datitrasm, (('CodiceDestinatario',  ftel_codice),))
            
            # 1.1.5 <ContattiTrasmittente>
            dati = []
            if Env.Azienda.numtel:
                numtel = ''
                for x in Env.Azienda.numtel.replace('+39',''):
                    if x.isalnum():
                        numtel += x
                if numtel:
                    # 1.1.5.1 <Telefono>
                    dati.append(('Telefono', numtel))
            if Env.Azienda.email:
                # 1.1.5.2 <Email>
                dati.append(('Email', Env.Azienda.email))
            if dati:
                contattitrasm = xmldoc.appendElement(datitrasm, 'ContattiTrasmittente',)
                xmldoc.appendItems(contattitrasm, dati)
            
            if not ftel_codice or ftel_codice == FTEL_NOCODE:
                if self.pdc.ftel_pec:
                    # 1.1.6 <PECDestinatario>
                    xmldoc.appendItems(datitrasm, (('PECDestinatario',  self.pdc.ftel_pec),))
            
            # 1.2 <CedentePrestatore>
            cedente = xmldoc.appendElement(head, 'CedentePrestatore')
            
            # 1.2.1 <DatiAnagrafici>
            cedente_datianag = xmldoc.appendElement(cedente, 'DatiAnagrafici')
            
            # 1.2.1.1 <IdFiscaleIVA>
            cedente_datianag_datifisc = xmldoc.appendElement(cedente_datianag, 'IdFiscaleIVA')
            xmldoc.appendItems(cedente_datianag_datifisc, (('IdPaese',  Env.Azienda.stato or "IT"),
                                                           ('IdCodice', Env.Azienda.piva)))
    #         if Env.Azienda.codfisc:
            if Env.Azienda.codfisc and Env.Azienda.codfisc != Env.Azienda.piva:
                # 1.2.1.2 <CodiceFiscale>
                xmldoc.appendItems(cedente_datianag, (('CodiceFiscale', Env.Azienda.codfisc),))
            
            # 1.2.1.3 <Anagrafica>
            cedente_datianag_anagraf = xmldoc.appendElement(cedente_datianag, 'Anagrafica')
            dati = []
            if dataz['cognome']:
                dati.append(('Nome', dataz['nome']))
                dati.append(('Cognome', dataz['cognome']))
            else:
                dati.append(('Denominazione', Env.Azienda.descrizione))
            xmldoc.appendItems(cedente_datianag_anagraf, dati)
            
            # 1.2.1.8 <RegimeFiscale>
            try:
                regfisc = 'RF%s' % str(int(dataz['regfisc'])).zfill(2)
            except:
                regfisc = 'RF01'
            xmldoc.appendItems(cedente_datianag, (('RegimeFiscale', regfisc),))
            
            # 1.2.2 <Sede>
            cedente_sede = xmldoc.appendElement(cedente, 'Sede')
            xmldoc.appendItems(cedente_sede, (('Indirizzo', Env.Azienda.indirizzo),
                                              ('CAP',       Env.Azienda.cap),
                                              ('Comune',    Env.Azienda.citta),
                                              ('Provincia', Env.Azienda.prov),
                                              ('Nazione',   Env.Azienda.stato),))
            
            if dataz['soind'] and dataz['socap'] and dataz['socit'] and dataz['sopro']:
                # 1.2.3 <StabileOrganizzazione>
                cedente_staborg = xmldoc.appendElement(cedente, 'StabileOrganizzazione')
                xmldoc.appendItems(cedente_staborg, (('Indirizzo', dataz['soind']),
                                                     ('CAP',       dataz['socap']),
                                                     ('Comune',    dataz['socit']),
                                                     ('Provincia', dataz['sopro']),
                                                     ('Nazione',   'IT'),))
            
            if dataz['reanum']:
                # 1.2.4 <IscrizioneREA>
                cedente_rea = xmldoc.appendElement(cedente, 'IscrizioneREA')
                xmldoc.appendItems(cedente_rea, (('Ufficio',   dataz['reauff']),
                                                 ('NumeroREA', dataz['reanum']),))
                if dataz['capsoc']:
                    if dataz['socuni']:
                        socuni = 'SU'
                    else:
                        socuni = 'SM'
                    xmldoc.appendItems(cedente_rea, (('CapitaleSociale', fmt_ii(dataz['capsoc'])),
                                                     ('SocioUnico',      socuni),))
                if dataz['socliq']:
                    socliq = 'LS'
                else:
                    socliq = 'LN'
                xmldoc.appendItems(cedente_rea, (('StatoLiquidazione', socliq),))
            
            if dataz['rfdes'] or dataz['rfcognome']:
                dati = []
                if dataz['rfcognome']:
                    dati.append(('Cognome', dataz['rfcognome']))
                    dati.append(('Nome', dataz['rfnome']))
                else:
                    dati.append(('Denominazione', dataz['rfdes']))
                # 1.3 <RappresentanteFiscale>
                cedente_rapfis = xmldoc.appendElement(cedente, 'RappresentanteFiscale')
                # 1.3.1 <DatiAnagrafici>
                cedente_rapfis_anag = xmldoc.appendElement(cedente_rapfis, 'DatiAnagrafici')
                xmldoc.appendItems(cedente_rapfis_anag, dati)
                # 1.3.1.1 <IdFiscaleIVA>
                cedente_rapfis_idf = xmldoc.appendElement(cedente_rapfis_anag, 'IdFiscaleIVA')
                xmldoc.appendItems(cedente_rapfis_idf, (('IdPaese',  dataz['rfstato']),
                                                        ('IdCodice', dataz['rfcodfis'] or dataz['rfpiva'])),)
            
            # 1.4 <CessionarioCommittente>
            cessionario = xmldoc.appendElement(head, 'CessionarioCommittente')
            
            # 1.4.1 <DatiAnagrafici>
            cessionario_datianag = xmldoc.appendElement(cessionario, 'DatiAnagrafici')
            if cli.piva:
                # 1.4.1.1 <IdFiscaleIVA>
                cessionario_datianag_idf = xmldoc.appendElement(cessionario_datianag, 'IdFiscaleIVA')
                xmldoc.appendItems(cessionario_datianag_idf, (('IdPaese',  cli.nazione or 'IT'),
                                                              ('IdCodice', cli.piva)),)
    #         if cli.nazione == 'IT' or len(cli.nazione or '') == 0:
    #             # 1.4.1.2 <CodiceFiscale>
    #             xmldoc.appendItems(cessionario_datianag, (('CodiceFiscale', cli.codfisc or cli.piva),))
    #         
            if cli.codfisc and cli.codfisc != cli.piva:
                # 1.4.1.2 <CodiceFiscale>
                xmldoc.appendItems(cessionario_datianag, (('CodiceFiscale', cli.codfisc),))
            
            # 1.4.1.3 <Anagrafica>
            cessionario_datianag_anagraf = xmldoc.appendElement(cessionario_datianag, 'Anagrafica')
            xmldoc.appendItems(cessionario_datianag_anagraf, (('Denominazione', pdc.descriz),))
            
            #1.4.2 <Sede>
            cessionario_sede = xmldoc.appendElement(cessionario, 'Sede')
            xmldoc.appendItems(cessionario_sede, (('Indirizzo', cli.indirizzo),
                                                  ('CAP',       cli.cap),
                                                  ('Comune',    cli.citta),
                                                  ('Provincia', cli.prov),
                                                  ('Nazione',   cli.nazione or "IT"),))
            
            if dataz['secodfis']:
                #1.5 <TerzoIntermediarioOSoggettoEmittente>
                tsogemi = xmldoc.appendElement(head, 'TerzoIntermediarioOSoggettoEmittente')
                #1.5.1 <DatiAnagrafici>
                tsogemi_datianag = xmldoc.appendElement(tsogemi, 'DatiAnagrafici')
                tsogemi_datianag_id_iva = xmldoc.appendElement(tsogemi_datianag, 'IdFiscaleIVA')
                xmldoc.appendItems(tsogemi_datianag_id_iva, (('IdPaese', dataz['sestato'] or "IT"),
                                                             ('IdCodice', dataz['sepiva'])))
                #1.5.2 <CodiceFiscale>
                xmldoc.appendItems(tsogemi_datianag, (('CodiceFiscale', dataz['secodfis']),))
                #1.5.3 <Anagrafica>
                tsogemi_datianag_anag = xmldoc.appendElement(tsogemi_datianag, 'Anagrafica')
                f = []
                if dataz['sedes']:
                    f.append(('Denominazione', dataz['sedes']))
                if dataz['senome']:
                    f.append(('Nome', dataz['senome']))
                if dataz['secognome']:
                    f.append(('Cognome', dataz['secognome']))
                if dataz['setit']:
                    f.append(('Titolo', dataz['setit']))
                if dataz['seeori']:
                    f.append(('CodEORI', dataz['seeori']))
                xmldoc.appendItems(tsogemi_datianag_anag, f)
            
            if dataz['sesogemi']:
                #1.6 <SoggettoEmittente>
                xmldoc.appendItems(head, (('SoggettoEmittente', dataz['sesogemi']),))
        
        loop = True
        while loop:
            
            # 2 <FatturaElettronicaBody>
            body = xmldoc.appendElement(fat, 'FatturaElettronicaBody')
            
            # 2.1 <DatiGenerali>
            body_gen = xmldoc.appendElement(body, 'DatiGenerali')
            
            # 2.1.1 <DatiGeneraliDocumento>
            body_gen_doc = xmldoc.appendElement(body_gen, 'DatiGeneraliDocumento')
            
            xmldoc.appendItems(body_gen_doc, 
                               (('TipoDocumento',          ftel_tipdoc),
#                                 ('Causale',                self.config.descriz),  #indicato in v.1.1, ma da errore
                                ('Divisa',                 'EUR'),
                                ('Data',                   data(self.datdoc)),
                                ('Numero',                 str(self.get_numdoc_print())),))
            
            if self.totritacc:
                # 2.1.1.5 <DatiRitenuta>
                cfg = self.dbcfg
                cfg.Retrieve('chiave=%s', 'azienda_ftel_ritaccpag')
                ra_caupag = cfg.descriz or 'A' #versamento per professione se manca setup
                cfg.Retrieve('chiave=%s', 'azienda_ftel_ritacctipo')
                ra_tipo = "RT0%s" % (int(cfg.importo or '1')) #default persone fisiche se manca setup
                body_gen_doc_rit = xmldoc.appendElement(body_gen_doc, 'DatiRitenuta')
                xmldoc.appendItems(body_gen_doc_rit, 
                                   (('TipoRitenuta',     ra_tipo),
                                    ('ImportoRitenuta',  fmt_ii(self.totritacc)),
                                    ('AliquotaRitenuta', fmt_sc(self.perritacc)),
                                    ('CausalePagamento', ra_caupag),))
            
            if self.totscodoc:
                # 2.1.1.8 <ScontoMaggiorazione>
                body_gen_doc_ssd = xmldoc.appendElement(body_gen_doc, 'ScontoMaggiorazione')
                xmldoc.appendItems(body_gen_doc_ssd, 
                                   (('Tipo',        "SC"),
                                    ('Percentuale', fmt_ii(self.perscodoc)),
                                    ('Importo',     fmt_ii(self.totscodoc)),))
            
            if self.ftel_bollovirt:
                # 2.1.1.6 <DatiBollo>
                body_gen_doc_bol = xmldoc.appendElement(body_gen_doc, 'DatiBollo')
                xmldoc.appendItems(body_gen_doc_bol, 
                                   (('BolloVirtuale', "SI"),
                                    ('ImportoBollo',  fmt_ii(self.ftel_bollovirt)),))
            
            if 'prof_conpre' in self.mov.config.GetFieldNames():
                # 2.1.1.7 <DatiCassaPrevidenziale> - gestito se presente plugin 'prof'
                contot = conimp = 0
                conalp = conaln = None
                for mov in self.mov:
                    if mov.config.prof_conpre:
                        contot += mov.importo
                        conalp = mov.iva.perciva
                        conaln = mov.iva.ftel_natura
                    elif mov.config.prof_calcon:
                        conimp += mov.importo
                if contot:
                    cfg = self.dbcfg
                    cfg.Retrieve('chiave=%s', 'prof_perconpre')
                    if not cfg.OneRow():
                        raise Exception, "Manca indicazione percentuale contributo su setup plugin 'prof'"
                    cassaprev = "TC%s" % str(int(dataz["cassaprev"])).zfill(2)
                    cp = [('TipoCassa',              cassaprev),
                          ('AlCassa',                fmt_sc(cfg.importo)),
                          ('ImportoContributoCassa', fmt_ii(contot)),
                          ('ImponibileCassa',        fmt_ii(conimp)),
                          ('AliquotaIVA',            fmt_pr(conalp)),
                          ('Ritenuta',               "SI")]
                    if conalp == 0:
                        if not conaln:
                            raise Exception, "Manca natura aliquota IVA su controib.prev."
                        cp['Natura'] = conaln
                    body_gen_doc_prv = xmldoc.appendElement(body_gen_doc, 'DatiCassaPrevidenziale')
                    xmldoc.appendItems(body_gen_doc_prv, cp)
            
            # 2.1.1.9 <ImportoTotaleDocumento>
            xmldoc.appendItems(body_gen_doc,
                               (('ImportoTotaleDocumento', fmt_ii(self.totimporto)),))
            
            if self.ftel_head_caus:
                # 2.1.1.11 <Causale>
                for rc in self.ftel_head_caus.split('\n'):
                    rc = rc.strip()
                    if rc:
                        xmldoc.appendItems(body_gen_doc, (('Causale', rc),))
            
            # 2.1.2 <DatiOrdineAcquisto>
            v = []
            if self.ftel_ordnum:
                v.append(('IdDocumento', self.ftel_ordnum))
            if self.ftel_orddat:
                v.append(('Data', data(self.ftel_orddat)))
            if self.ftel_codcup:
                v.append(('CodiceCUP', self.ftel_codcup))
            if self.ftel_codcig:
                v.append(('CodiceCIG', self.ftel_codcig))
            if v:
                body_gen_acq = xmldoc.appendElement(body_gen, 'DatiOrdineAcquisto')
                xmldoc.appendItems(body_gen_acq, v)
            
            if Env.Azienda.BaseTab.FTEL_DACOCO:
                
                if self.ftel_contr_num or self.ftel_contr_dat or self.ftel_contr_cig or self.ftel_contr_cup or self.ftel_contr_ccc:
                    # 2.1.3 <DatiContratto>
                    v = []
                    if self.ftel_contr_num:
                        v.append(('IdDocumento', self.ftel_contr_num))
                    if self.ftel_contr_dat:
                        v.append(('Data', data(self.ftel_contr_dat)))
                    if self.ftel_contr_ccc:
                        v.append(('CodiceCommessaConvenzione', self.ftel_contr_ccc))
                    if self.ftel_contr_cup:
                        v.append(('CodiceCUP', self.ftel_contr_cup))
                    if self.ftel_contr_cig:
                        v.append(('CodiceCIG', self.ftel_contr_cig))
                    if v:
                        body_gen_acq = xmldoc.appendElement(body_gen, 'DatiContratto')
                        xmldoc.appendItems(body_gen_acq, v)
                
                if self.ftel_conve_num or self.ftel_conve_dat or self.ftel_conve_cig or self.ftel_conve_cup or self.ftel_conve_ccc:
                    # 2.1.4 <DatiConvenzione>
                    v = []
                    if self.ftel_conve_num:
                        v.append(('IdDocumento', self.ftel_conve_num))
                    if self.ftel_conve_dat:
                        v.append(('Data', data(self.ftel_conve_dat)))
                    if self.ftel_conve_ccc:
                        v.append(('CodiceCommessaConvenzione', self.ftel_conve_ccc))
                    if self.ftel_conve_cup:
                        v.append(('CodiceCUP', self.ftel_conve_cup))
                    if self.ftel_conve_cig:
                        v.append(('CodiceCIG', self.ftel_conve_cig))
                    if v:
                        body_gen_acq = xmldoc.appendElement(body_gen, 'DatiConvenzione')
                        xmldoc.appendItems(body_gen_acq, v)
            
            if not self.config.ftel_noddt:
                # 2.1.8 <DatiDDT>
                ddt = dbm.DocMag()
                ddt.ClearOrders()
                ddt.AddOrder('doc.datdoc')
                ddt.AddOrder('doc.numdoc')
                ddt.Retrieve("doc.id_docacq=%s" % self.id)
                if not ddt.IsEmpty():
                    for _ in ddt:
                        body_gen_ddt = xmldoc.appendElement(body_gen, 'DatiDDT')
                        xmldoc.appendItems(body_gen_ddt, (('NumeroDDT', str(ddt.numdoc)),
                                                          ('DataDDT',   data(ddt.datdoc)),))
#                         for movddt in ddt.mov:
#                             xmldoc.appendItems(body_gen_ddt, (('RiferimentoNumeroLinea', str(movddt.numriga)),))
            
            # 2.2 <DatiBeniServizi>
            
            body_det = xmldoc.appendElement(body, 'DatiBeniServizi')
            
            # 2.2.1 <DettaglioLinee>
            
            id_aliq_first = None
            col_id_aliq = self.mov._GetFieldIndex('id_aliqiva', inline=True)
            rsb = self.mov.GetRecordset()
            for n in range(len(rsb)):
                if rsb[n][col_id_aliq]:
                    id_aliq_first = rsb[n][col_id_aliq]
                    break
            if id_aliq_first is None:
                raise Exception('Aliquota non trovata')
            first_aliq = adb.DbTable('aliqiva')
            first_aliq.Get(id_aliq_first)
            
            for i, mov in enumerate(self.mov):
                
                _numriga = mov.numriga
                _codart = mov.prod.codice
                _codfor = mov.prod.codfor or ''
                _barcode = mov.prod.barcode or ''
                _descriz = mov.descriz or '.'
                _qta = mov.qta
                _prezzo = mov.prezzo
                _importo = mov.importo
                _um = mov.um
                
                _datper1 = _datper2 = None
                if hasattr(mov, 'dm_datpar') and hasattr(mov, 'dm_datsca'):
                    _datper1 = mov.dm_datpar
                    _datper2 = mov.dm_datsca
                
                if mov.config.tipologia == "E":
                    #righe sconto merce usano aliquota first_aliq, poi si accoda riga negativa
                    tabiva = first_aliq
                else:
                    tabiva = mov.iva
                
                DP = Env.Azienda.BaseTab.MAGPRE_DECIMALS
                
                if _importo and self.config.scorpiva:
                    _prezzo = round(_prezzo/(100+mov.iva.perciva)*100, 5)
                    DP = 5
                    _importo = round(_importo/(100+mov.iva.perciva)*100, 2)
                
                #body dettaglio linea
                body_det_row = xmldoc.appendElement(body_det, 'DettaglioLinee')
                
                xmldoc.appendItems(body_det_row, (('NumeroLinea', str(_numriga)),))
                
                dati = []
                
                if Env.Azienda.BaseTab.FTEL_VENCOD and len(_codart or '') > 0:
                    _tipdat = Env.Azienda.BaseTab.FTEL_TIPDAT
                    if _tipdat:
                        if Env.Azienda.BaseTab.FTEL_TIPCOD == "P":
                            _outcod = _codart
                        elif Env.Azienda.BaseTab.FTEL_TIPCOD == "F":
                            _outcod = _codfor
                        elif Env.Azienda.BaseTab.FTEL_TIPCOD == "B":
                            _outcod = _barcode
                        else:
                            raise Exception("Tipo codice errato in setup")
                        if _outcod:
                            body_det_row_codart = xmldoc.appendElement(body_det_row, 'CodiceArticolo')
                            xmldoc.appendItems(body_det_row_codart, (('CodiceTipo', _tipdat),
                                                                     ('CodiceValore', _outcod)))
                
                dati.append(('Descrizione', _descriz))
                
                if not _importo:
                    dati.append(('Quantita', '0.00'))
                    if _datper1 and _datper2:
                        dati.append(('DataInizioPeriodo', data(_datper1)))
                        dati.append(('DataFinePeriodo', data(_datper2)))
                    dati.append(('PrezzoUnitario', '0.00'))
                    dati.append(('PrezzoTotale', '0.00'))
                    dati.append(('AliquotaIVA', fmt_sc(first_aliq.perciva)))
                    if first_aliq.ftel_natura:
                        dati.append(('Natura', first_aliq.ftel_natura))
                else:
                    dati.append(('Quantita', fmt_qt(_qta or 1)))
                    if _um:
                        dati.append(('UnitaMisura', _um))
                    if _datper1 and _datper2:
                        dati.append(('DataInizioPeriodo', data(_datper1)))
                        dati.append(('DataFinePeriodo', data(_datper2)))
                    if _prezzo:
                        dati.append(('PrezzoUnitario', fmt_pr(_prezzo, DP)))
                    else:
                        dati.append(('PrezzoUnitario', fmt_pr(_importo)))
                    xmldoc.appendItems(body_det_row, dati)
                    dati = []
                    for n in range(1, 7):
                        per_sconto = getattr(mov, 'sconto%d' % n) or 0
                        if per_sconto:
                            #body dettaglio sconto
                            sdati = []
                            sdati.append(('Tipo', 'SC'))
                            sdati.append(('Percentuale', fmt_sc(per_sconto)))
                            body_det_row_sconto = xmldoc.appendElement(body_det_row, 'ScontoMaggiorazione')
                            xmldoc.appendItems(body_det_row_sconto, sdati)
                    dati.append(('PrezzoTotale', fmt_ii(_importo)))
                    dati.append(('AliquotaIVA', fmt_sc(tabiva.perciva)))
                    if mov.samefloat(tabiva.perciva, 0):
                        dati.append(('Natura', tabiva.ftel_natura))
                    if self.ftel_rifamm:
                        dati.append(('RiferimentoAmministrazione', self.ftel_rifamm))
                
                xmldoc.appendItems(body_det_row, dati)

                if mov.ftel_adg:
                    dbadg.json_load(mov)
                    for _ in dbadg:
                        adg = xmldoc.appendElement(body_det_row, 'AltriDatiGestionali')
                        adgpar = [('TipoDato', dbadg.tipdat)]
                        if dbadg.riftxt:
                            adgpar.append(('RiferimentoTesto', dbadg.riftxt))
                        if dbadg.rifnum:
                            adgpar.append(('RiferimentoNumero', fmt_pr(dbadg.rifnum, 4)))
                        if dbadg.rifdat:
                            adgpar.append(('RiferimentoData', dbadg.rifdat)) # gia' stringa in formato %Y-%m-%d
                        xmldoc.appendItems(adg, adgpar)
                
                if mov.config.tipologia == "E":
                    #body dettaglio linea aggiunta x sconto merce
                    
                    body_det_row = xmldoc.appendElement(body_det, 'DettaglioLinee')
                    
                    xmldoc.appendItems(body_det_row, (('NumeroLinea', str(_numriga)),))
                    
                    dati = []
                    
                    if Env.Azienda.BaseTab.FTEL_VENCOD and len(_codart or '') > 0:
                        _tipdat = Env.Azienda.BaseTab.FTEL_TIPDAT
                        if _tipdat:
                            if Env.Azienda.BaseTab.FTEL_TIPCOD == "P":
                                _outcod = _codart
                            elif Env.Azienda.BaseTab.FTEL_TIPCOD == "F":
                                _outcod = _codfor
                            elif Env.Azienda.BaseTab.FTEL_TIPCOD == "B":
                                _outcod = _barcode
                            else:
                                raise Exception("Tipo codice errato in setup")
                            if _outcod:
                                body_det_row_codart = xmldoc.appendElement(body_det_row, 'CodiceArticolo')
                                xmldoc.appendItems(body_det_row_codart, (('CodiceTipo', _tipdat),
                                                                         ('CodiceValore', _outcod)))
                    
                    dati.append(('Descrizione', _descriz))
                    
                    if not _importo:
                        dati.append(('Quantita', '0.00'))
                        dati.append(('PrezzoUnitario', '0.00'))
                        dati.append(('PrezzoTotale', '0.00'))
                        dati.append(('AliquotaIVA', fmt_sc(first_aliq.perciva)))
                        if first_aliq.ftel_natura:
                            dati.append(('Natura', first_aliq.ftel_natura))
                    else:
                        if True:#_qta:
                            dati.append(('Quantita', fmt_qt(_qta or 1)))
                        if _um:
                            dati.append(('UnitaMisura', _um))
                        if _prezzo:
                            dati.append(('PrezzoUnitario', fmt_pr(-_prezzo, DP)))
                        else:
                            dati.append(('PrezzoUnitario', fmt_pr(-_importo)))
                        xmldoc.appendItems(body_det_row, dati)
                        dati = []
                        for n in range(1, 7):
                            per_sconto = getattr(mov, 'sconto%d' % n) or 0
                            if per_sconto:
                                #body dettaglio sconto
                                sdati = []
                                sdati.append(('Tipo', 'SC'))
                                sdati.append(('Percentuale', fmt_sc(per_sconto)))
                                body_det_row_sconto = xmldoc.appendElement(body_det_row, 'ScontoMaggiorazione')
                                xmldoc.appendItems(body_det_row_sconto, sdati)
                        dati.append(('PrezzoTotale', fmt_ii(-_importo)))
                        dati.append(('AliquotaIVA', fmt_sc(tabiva.perciva)))
                        if mov.samefloat(tabiva.perciva, 0):
                            dati.append(('Natura', tabiva.ftel_natura))
                        if self.ftel_rifamm:
                            dati.append(('RiferimentoAmministrazione', self.ftel_rifamm))
                            
                    xmldoc.appendItems(body_det_row, dati)
                    
                    adg = xmldoc.appendElement(body_det_row, 'AltriDatiGestionali')
                    xmldoc.appendItems(adg, (('TipoDato',          'OMAGGIO'),
                                             ('RiferimentoTesto',  'SCONTO MERCE'), ))
            
            self.MakeTotals()
            
            if self.id_speinc:
                #aggiungo riga spese
                for t in self._info.totpdc:
                    if t[7] == "S":
                        #body dettaglio linea
                        body_det_row = xmldoc.appendElement(body_det, 'DettaglioLinee')
                        _numriga += 1
                        _prezzo = self.speinc.importo
                        _importo = t[3]
                        iva = dbm.adb.DbTable('aliqiva')
                        iva.Get(self.speinc.id_aliqiva)
                        _qta = len(self.regcon.scad)
                        dati = []
                        dati.append(('NumeroLinea', str(_numriga)))
                        dati.append(('Descrizione', 'SPESE DI INCASSO'))
#                         dati.append(('TipoCessionePrestazione', 'SC'))
                        if True:#_qta:
                            dati.append(('Quantita', fmt_qt(_qta or 1)))
                        if _prezzo:
                            dati.append(('PrezzoUnitario', fmt_pr(_prezzo)))
                        else:
                            dati.append(('PrezzoUnitario', fmt_ii(_importo)))
                        dati.append(('PrezzoTotale', fmt_ii(_importo)))
                        dati.append(('AliquotaIVA', fmt_sc(iva.perciva)))
                        if mov.samefloat(iva.perciva, 0):
                            dati.append(('Natura', iva.ftel_natura))
                        xmldoc.appendItems(body_det_row, dati)
                        break
            
            # 2.2.2 <DatiRiepilogo>
            iva = dbm.adb.DbTable('aliqiva')
            for ivaid, ivacod, ivades, imponib, imposta, importo, imposcr, isomagg, perciva, percind, tipoalq in self._info.totiva:
                if iva.id != ivaid:
                    iva.Get(ivaid)
                body_det_rie = xmldoc.appendElement(body_det, 'DatiRiepilogo')
                dativa = []
                dativa.append(('AliquotaIVA',       fmt_sc(perciva)))
                if iva.ftel_natura:
                    dativa.append(('Natura', iva.ftel_natura))
                dativa.append(('ImponibileImporto', fmt_ii(imponib)))
                dativa.append(('Imposta',           fmt_ii(imposta)))
                if iva.ftel_natura and iva.ftel_rifnorm:
                    dativa.append(('RiferimentoNormativo', iva.ftel_rifnorm))
                else:
                    if iva.tipo == "S":
                        #split payment
                        esig = "S"
                    else:
                        #esigilità immediata
                        esig = "I"
                    dativa.append(('EsigibilitaIVA', esig))
                xmldoc.appendItems(body_det_rie, dativa)
            
            if self.id_reg is not None:
                
                reg = self.regcon
                reg.Get(self.id_reg)
                
                if reg.OneRow():
                    
                    # 2.4 <DatiPagamento>
                    body_pag = xmldoc.appendElement(body, 'DatiPagamento')
                    
                    # 2.4.1 <CondizioniPagamento>
                    xmldoc.appendItems(body_pag, (('CondizioniPagamento', self.modpag.ftel_tippag),))
                    
                    if len(self.regcon.scad) == 0:
                        datipag = [('ModalitaPagamento',     self.modpag.ftel_modpag),
                                   ('DataScadenzaPagamento', data(self.datdoc)),
                                   ('ImportoPagamento',      fmt_ii(self.totdare)),]
                        if cli.id_bancapag:
                            dbban = dbm.adb.DbTable('banche')
                            if dbban.Get(cli.id_bancapag) and dbban.OneRow():
                                if len(dbban.iban or '') > 0:
                                    datipag.append(('IBAN', dbban.iban))
                        body_pag_det = xmldoc.appendElement(body_pag, 'DettaglioPagamento')
                        xmldoc.appendItems(body_pag_det, datipag)
                    else:
                        for scad in self.regcon.scad:
                            # 2.4.2 <DettaglioPagamento>
                            datipag = [('ModalitaPagamento',     self.modpag.ftel_modpag),
                                       ('DataScadenzaPagamento', data(scad.datscad)),
                                       ('ImportoPagamento',      fmt_ii(scad.importo)),]
                            if cli.id_bancapag:
                                dbban = dbm.adb.DbTable('banche')
                                if dbban.Get(cli.id_bancapag) and dbban.OneRow():
                                    if len(dbban.iban or '') > 0:
                                        datipag.append(('IBAN', dbban.iban))
                            body_pag_det = xmldoc.appendElement(body_pag, 'DettaglioPagamento')
                            xmldoc.appendItems(body_pag_det, datipag)
            
            #genero file pdf dei documenti elaborati
            pdf_stream = None
            rptname = self.config.ftel_layout or self.config.toolprint
            if rptname and Env.Azienda.BaseTab.FTEL_VENPDF:
                doc = FatturaElettronica()
                doc.Get(self.id)
                doc.MakeTotals()
                doc._info.anag = doc.GetAnag()
                pdf_h = StringIO()
                rpt.Report(None, doc, rptname, pdf_h, output="STORE") 
                pdf_h.seek(0)
                pdf_stream = pdf_h.read()
                pdf_h.close()
            
            if pdf_stream:
                
                fullname = self.ftel_get_filename(numprogr, self.datdoc.year)
                _, filename = os.path.split(fullname)
                filename = filename.replace('.xml', '.pdf')
                
                zip_h = StringIO()
                zf = zipfile.ZipFile(zip_h, mode='w', compression=zipfile.ZIP_DEFLATED)
                zf.writestr(str(filename), pdf_stream)
                zf.close()
                zip_h.seek(0)
                zip_stream = zip_h.read()
                zip_h.close()
                
                # 2.5 <Allegati>
                body_pdf = xmldoc.appendElement(body, 'Allegati')
                xmldoc.appendItems(body_pdf, (('NomeAttachment',        filename),
                                              ('AlgoritmoCompressione', 'ZIP'),
                                              ('FormatoAttachment',     'PDF'),
                                              ('Attachment',            base64.b64encode(zip_stream)),))
            
            for filename, pdf_stream in self.add_attachments():
                zip_h = StringIO()
                zf = zipfile.ZipFile(zip_h, mode='wb', compression=zipfile.ZIP_DEFLATED)
                zf.writestr(str(filename), pdf_stream)
                zf.close()
                zip_h.seek(0)
                zip_stream = zip_h.read()
                zip_h.close()
                
                # 2.5 <Allegati>
                body_pdf = xmldoc.appendElement(body, 'Allegati')
                xmldoc.appendItems(body_pdf, (('NomeAttachment',        filename),
                                              ('AlgoritmoCompressione', 'ZIP'),
                                              ('FormatoAttachment',     'PDF'),
                                              ('Attachment',            base64.b64encode(zip_stream)),))
            
            if not self.MoveNext():
                loop = False
        
        #genero file xml dei documenti elaborati
#         stream = unicode(xmldoc.toprettyxml(encoding="utf-8"))
        stream = xmldoc.toprettyxml(encoding="utf-8")
        text_re = re.compile('>\n\s+([^<>\s].*?)\n\s+</', re.DOTALL)    
        stream = text_re.sub('>\g<1></', stream)
#         stream = stream.replace("’", "'")
        
        if "’" in stream:
            stream = stream.replace("’", "'")
        
        n = stream.index('>')+1
        stream = stream[:n] + '\n<?xml-stylesheet type="text/xsl" href="fatturapa_v1.2.1.xsl"?>' + stream[n:]
        
        fullname = self.ftel_get_filename(numprogr, self.datdoc.year)
        pathname, filename = os.path.split(fullname)
        
        h = open(fullname, 'w')
        h.write(stream)
        h.close()
        
        self.ftel_make_style(self.datdoc.year)
        
        bt = Env.Azienda.BaseTab
        do_trasm = bt.is_eeb_enabled()
        if do_trasm and is_pa:
            filename_p7m = pa_callback(pathname, filename)
            if filename_p7m:
                filename = filename_p7m
                h = open(os.path.join(pathname, filename), 'rb')
                stream = h.read()
                h.close()
            else:
                do_trasm = False
        
        if do_trasm:
            response = self.gateway_send_file(self.get_keydoc(), filename, stream)
            if response['result'] == "OK":
                status = self.STATUS_ATTESA_ESITO
                message = ""
                cmd = """
                    UPDATE movmag_h SET ftel_numtrasm=%%s,
                                        ftel_eeb_status=%%s,
                                        ftel_eeb_message=%%s
                     WHERE id=%s
                """ % self.id
                db = self._info.db
                if not db.Execute(cmd, (numprogr, status, message)):
                    raise Exception(db.dbError.description)
            elif response['result'] == "ERROR":
                raise Exception("Errore nella trasmissione al gateway:\n%s" % response['error'])
        else:
            cmd = """
                UPDATE movmag_h SET ftel_numtrasm=%%s,
                                    ftel_eeb_status=%%s,
                                    ftel_eeb_message=%%s
                 WHERE id=%s
            """ % self.id
            db = self._info.db
            status = self.STATUS_XML_GENERATO
            if not db.Execute(cmd, (numprogr, status, '')):
                raise Exception(db.dbError.description)
        
        p = ProgrMagazz_FatturaElettronica()
        p.Retrieve()
        if p.IsEmpty():
            p.CreateNewRow()
        if numprogr > (p.progrimp1 or 0):
            p.progrimp1 = numprogr
            p.Save()
        
        return pathname, filename
    
    def add_attachments(self):
        return []
    
    def ftel_make_style(self, year):
        path = self.ftel_get_pathname(year)
        filename = os.path.join(path, 'fatturapa_v1.2.1.xsl')
        if not os.path.isfile(filename):
            import ftel.vendite.fatturapa_v121_xsl as xsl
            open(filename, 'w').write(xsl.xsl)
    
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
            url = self.gateway_get_url('io/client/vendite?wsdl')
            self.gateway_client = SudsClient(url=url)
        return self.gateway_client
    
    def gateway_send_file(self, keydoc, filename, xml_stream):
        
        client = self.gateway_get_client()
        username = Env.Azienda.BaseTab.FTEL_EEB_USER
        password = hashlib.sha256(unicode(Env.Azienda.BaseTab.FTEL_EEB_PSWD)).hexdigest()
#         if filename.lower().endswith('.xml'):
#             xml_stream = unicode(xml_stream).encode('utf-8')
        xml_b64 = base64.encodestring(xml_stream)#unicode(xml_stream).encode('utf-8'))
        info = xml_b64+unicode(password).encode('utf-8')
        filehash = hashlib.sha256(info).hexdigest()
        
        return client.service.put_file(username=username,
                                       keydoc=keydoc,
                                       xml_b64=xml_b64,
                                       xml_hash=filehash,
                                       filename=filename)
    
    def gateway_receive_notif(self):
        
        client = self.gateway_get_client()
        username = Env.Azienda.BaseTab.FTEL_EEB_USER
        password = hashlib.sha256(unicode(Env.Azienda.BaseTab.FTEL_EEB_PSWD)).hexdigest()
        keydoc = self.get_keydoc()
        info = keydoc+unicode(password).encode('utf-8')
        key_hash = hashlib.sha256(info).hexdigest()
        
        return client.service.get_notifica(username=username,
                                           keydoc=keydoc,
                                           key_hash=key_hash)
    
    def gateway_receive_dettaglio_scarto(self):
         
        client = self.gateway_get_client()
        username = Env.Azienda.BaseTab.FTEL_EEB_USER
        password = hashlib.sha256(unicode(Env.Azienda.BaseTab.FTEL_EEB_PSWD)).hexdigest()
        keydoc = self.get_keydoc()
        info = keydoc+unicode(password).encode('utf-8')
        key_hash = hashlib.sha256(info).hexdigest()
        
        resp = client.service.get_dettaglio_scarto(username=username,
                                                   keydoc=keydoc,
                                                   key_hash=key_hash)
        print resp
        if resp['result'] == "ERROR":
            raise Exception(resp['error'])
        
        if resp['result'] == "OK":
            return simplejson.loads(base64.b64decode(resp['data']))
        
        raise Exception


class FTEL_Document(Document):
    
    version = '1.2'
    sdicver = 'fpx12'
        
    def createRoot(self, is_pa):
        
        assert type(is_pa) is bool
        
        fat = self.appendElement(self, "p:FatturaElettronica")
        fat.setAttribute('xmlns:p', "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v%s" % self.version) # >= 1.2
        fat.setAttribute('xmlns:ds', "http://www.w3.org/2000/09/xmldsig#")
        fat.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        fat.setAttribute('xsi:schemaLocation', "http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v%s http://www.fatturapa.gov.it/export/fatturazione/sdi/fatturapa/v1.2/Schema_del_file_xml_FatturaPA_versione_%s.xsd" % (self.version,
                                                                                                                                                                                                                                  self.version,))
        if is_pa:
            self.sdicver = 'FPA'
        else:
            self.sdicver = 'FPR'
        self.sdicver += self.version.replace('.', '')
        fat.setAttribute('versione', self.sdicver)
        
        return fat
    
    def appendElement(self, parent, tagName):
        element = self.createElement(tagName)
        parent.appendChild(element)
        return element
    
    def appendItems(self, node, key_values):
        for name, val in key_values:
            item = self.createElement(name)
            item_content = self.createTextNode(val)
            item.appendChild(item_content)
            node.appendChild(item)
        return node



class ProgrMagazz(adb.DbTable):
    
    _key = None
    
    def __init__(self):
        if self._key is None:
            raise Exception, "Classe non istanziabile"
        adb.DbTable.__init__(self, 'cfgprogr', 'progr')
        self.AddBaseFilter('progr.codice=%s', self._key)
        self.Reset()
    
    def CreateNewRow(self, *args, **kwargs):
        adb.DbTable.CreateNewRow(self)
        self.codice = self._key


class ProgrMagazz_FatturaElettronica(ProgrMagazz):
    _key = 'ftel_numprogr'
