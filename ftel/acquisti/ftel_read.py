# -*- coding: utf-8 -*-

import xml.dom.minidom as minidom
import base64
import datetime
from StringIO import StringIO
from decimal import Decimal
import stormdb as adb
import zipfile


class _FTEL_Anag(object):
    
    paese = None
    piva = None
    codfisc = None
    descriz = None
    indirizzo = None
    civico = None
    cap = None
    citta = None
    prov = None
    numtel = None
    numfax = None
    email = None
    
    def get_indirizzo2(self):
        i = ''
        if self.cap:
            i += ('%s ' % self.cap)
        i += ('%s ' % self.citta)
        if self.prov:
            i += ('(%s)' % self.prov)
        return i


class _FTEL_Head(object):
    
    tipdoc = None
    divisa = None
    datdoc = None
    numdoc = None
    totdoc = None
    totiva = None
    ritacc = None
    bollov = None
    
    oa_num = None
    oa_dat = None
    oa_cig = None
    oa_cup = None
    
    righe = None
    totiva = None
    scadenze = None
    
    allegati = None
    
    def __init__(self):
        object.__init__(self)
        self.righe = []
        self.totiva = []
        self.allegati = []
        self.scadenze = []
    
    def get_descriz_tipdoc(self):
        if self.tipdoc == "TD01": return "Fattura"
        if self.tipdoc == "TD02": return "Acconto fattura"
        if self.tipdoc == "TD03": return "Acconto parcella"
        if self.tipdoc == "TD04": return "Nota credito"
        if self.tipdoc == "TD05": return "Nota debito"
        if self.tipdoc == "TD06": return "Parcella"
        if self.tipdoc == "TD07": return "Fattura semplif."
        if self.tipdoc == "TD08": return "Nota cr.semplif."
        if self.tipdoc == "TD10": return "Ft.Intra beni"
        if self.tipdoc == "TD11": return "Ft.Intra servizi"
        return "??? %s" % self.tipdoc
    
    def get_descriz_datdoc(self):
        return adb.DbTable.sepnvi(self.datdoc)
    
    def get_descriz_modpag(self):
        if len(self.scadenze) == 0:
            return ''
        modpag = self.scadenze[0].modpag
        if modpag == "MP01": return "Contanti"
        if modpag == "MP02": return "Assegno"
        if modpag == "MP03": return "Assegno circolare"
        if modpag == "MP04": return "Contanti c/o tesoreria"
        if modpag == "MP05": return "Bonifico bancario"
        if modpag == "MP06": return "Vaglia cambiario"
        if modpag == "MP07": return "Bollettino bancario"
        if modpag == "MP08": return "Carta di pagamento"
        if modpag == "MP09": return "RID"
        if modpag == "MP10": return "RID utenze"
        if modpag == "MP11": return "RID veloce"
        if modpag == "MP12": return "RIBA"
        if modpag == "MP13": return "MAV"
        if modpag == "MP14": return "Quitanza erario"
        if modpag == "MP15": return "Giroconto su conti di contab. scpeciale"
        if modpag == "MP16": return "Domiciliazione bancaria"
        if modpag == "MP17": return "Domiciliazione postale"
        if modpag == "MP18": return "Bollettino di c/c postale"
        if modpag == "MP19": return "SEPA Direct Debit"
        if modpag == "MP20": return "SEPA Direct Debit CORE"
        if modpag == "MP21": return "SEPA Direct Debit B2B"
        if modpag == "MP22": return "Trattenuta su somme gia' riscosse"
        return "??? %s" % modpag
    
    def get_descriz_iban(self):
        if len(self.scadenze) == 0:
            return ''
        iban = self.scadenze[0].iban
        return iban or ''
    
    def get_descriz_scadenza(self, num, col):
        if len(self.scadenze) <= num:
            return ''
        value = getattr(self.scadenze[num], col)
        if value:
            if col == 'impscad':
                value = adb.DbTable.sepnvi(value)
            if col == 'datscad':
                value = adb.DbTable.dita(value)
        return value
    
    def get_descriz_imposta(self, num, col):
        if len(self.totiva) <= num:
            return ''
        aliqiva = getattr(self.totiva[num], 'aliqiva')
        natura = getattr(self.totiva[num], 'natura')
        imponib = getattr(self.totiva[num], 'imponib')
        imposta = getattr(self.totiva[num], 'imposta')
        if ('%.2f' % aliqiva).endswith('.00'):
            aliqiva = int(aliqiva)
        if col == 'aliqiva':
            return str(aliqiva)
        if col == 'descriz':
            if not natura:
                desc = 'IVA %s%%' % aliqiva
            else:
                if natura == "N1": desc = "ESCLUSO EX ART 15"
                if natura == "N2": desc = "NON SOGGETTO"
                if natura == "N3": desc = "NON IMPONIBILE"
                if natura == "N4": desc = "ESENTE"
                if natura == "N5": desc = "REGIME DEL MARGINE"
                if natura == "N6": desc = "INVERS.CONTABILE (REV.CHARGE)"
                if natura == "N7": desc = "ASSOLTA IN ALTRO PAESE UE"
                rifnorm = getattr(self.totiva[num], 'rifnorm')
                if rifnorm:
                    desc = '%s - %s' % (desc, rifnorm)
            return desc
            
        if col == 'imponib':
            return adb.DbTable.sepnvi(imponib)
        if col == 'imposta':
            return adb.DbTable.sepnvi(imposta)
        return "???"
    
    def get_qta_prezzo_decimals(self):
        ndq = 0
        ndp = 2
        for r in self.righe:
            if r.qta:
#                 t = Decimal(str(r.qta)).as_tuple()
#                 if t.digits[1] != 0:
#                     ndq = max(ndq, abs(t.exponent))
                ndq = max(ndq, len(str(r.qta))-str(r.qta).index('.')+1)
            if r.prezzo:
#                 t = Decimal(str(r.prezzo)).as_tuple()
#                 if t.digits[1] != 0:
#                     ndp = max(ndp, abs(t.exponent))
                try:
                    ndp = max(ndp, len(str(r.prezzo))-(str(r.prezzo).index('.')+1))
                except:
                    pass
        return ndq, ndp
    
    def get_totale_imponibile(self):
        ti = 0
        for i in self.totiva:
            ti += (i.imponib or 0)
        return ti
    
    def get_totale_imposta(self):
        ti = 0
        for i in self.totiva:
            ti += (i.imposta or 0)
        return ti
    
    def get_totale_imposta_split(self):
        ti = 0
        for i in self.totiva:
            if i.esigiva == "S":
                ti += (i.imposta or 0)
        return ti
    
    def get_totale_dare(self):
        return self.totdoc - self.get_totale_imposta_split() - (self.ritacc or 0)

class _FTEL_Body(object):
    
    numriga = None
    codart = None
    descriz = None
    qta = None
    unimis = None
    prezzo = None
    sconto_pe1 = sconto_pe2 = sconto_pe3 = sconto_pe4 = sconto_pe5 = sconto_pe6 = None
    sconto_val = None
    totale = None
    aliqiva = None
    
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
        return ''
    
    def get_descriz_aliqiva(self):
        aliqiva = self.aliqiva
        if not aliqiva:
            return '0'
        if aliqiva.is_integer():
            aliqiva = int(aliqiva)
        return str(aliqiva)

class _FTEL_RigaIva(object):
    
    aliqiva = None
    imponib = None
    imposta = None
    esigiva = None
    natura = None
    rifnorm = None

class _FTEL_RigaScadenza(object):
    
    condpag = None
    modpag = None
    datscad = None
    impscad = None
    banca = None
    iban = None
    abi = None
    cab = None
    bic = None

class _FTEL_Allegato(object):
    
    filename = None
    filetype = None
    descriz = None
    stream = None


class FTEL_Fornitore(_FTEL_Anag):
    regfisc = None
    
class FTEL_Cliente(_FTEL_Anag):
    pass


class FTEL(object):
    
    formato = None
    
    anag_fornit = None
    anag_cliente = None
    docs = None
    
    def __init__(self, filename=None, stream=None):
        self.anag_fornit = FTEL_Fornitore()
        self.anag_cliente = FTEL_Cliente()
        self.docs = []
        self.init_dom(filename, stream)
    
    def init_dom(self, filename=None, stream=None):
        
        object.__init__(self)
        if filename:
            f = open(filename, 'r')
        elif stream:
            f = StringIO(stream)
        else:
            raise Exception
        dom = minidom.parse(f)
        f.close()
        
        for node in dom.childNodes:
            if node.nodeName.endswith('FatturaElettronica'):
                self.dom_ftel = node
                break
        if self.dom_ftel is None:
            raise Exception("Non trovo tag FatturaElettronica")
        
        self.dom_head = self.dom_ftel.getElementsByTagName('FatturaElettronicaHeader')[0]
        self.dom_body = self.dom_ftel.getElementsByTagName('FatturaElettronicaBody')
    
    def get_value(self, node, chain, conv=None, index=0):
        try:
            for name in chain.split('|'):
                node = node.getElementsByTagName(name)[index]
                index = 0
            value = node.firstChild.nodeValue
            if callable(conv):
                value = conv(value)
            return value
        except:
            return None


class FTEL_Doc(FTEL):
    
    def __init__(self, *args, **kwargs):
        
        load_attachments = kwargs.pop('load_attachments', True)
        FTEL.__init__(self, *args, **kwargs)
        
        def h(*v):
            return self.get_value(self.dom_head, *v)
        
        self.formato = h('DatiTrasmissione|FormatoTrasmissione')
        
        def read_anag(anag, tipo):
            
            def _h(x):
                return h(x % tipo)
            
            cp_desc = _h(r'%s|DatiAnagrafici|Anagrafica|Denominazione')
            cp_nome = _h(r'%s|DatiAnagrafici|Anagrafica|Nome')
            cp_cogn = _h(r'%s|DatiAnagrafici|Anagrafica|Cognome')
            
            anag.nome = cp_nome
            anag.cognome = cp_cogn
            if cp_desc:
                anag.descriz = cp_desc
            else:
                anag.descriz = '%s %s' % (cp_cogn, cp_nome)
            
            anag.regfisc =   _h(r'%s|DatiAnagrafici|Anagrafica|RegimeFiscale')
            
            anag.paese =     _h(r'%s|DatiAnagrafici|IdFiscaleIVA|IdPaese')
            anag.piva =      _h(r'%s|DatiAnagrafici|IdFiscaleIVA|IdCodice')
            anag.codfisc =   _h(r'%s|DatiAnagrafici|CodiceFiscale')
            
            anag.indirizzo = _h(r'%s|Sede|Indirizzo')
            anag.civico =    _h(r'%s|Sede|NumeroCivico')
            anag.cap =       _h(r'%s|Sede|CAP')
            anag.citta =     _h(r'%s|Sede|Comune')
            anag.prov =      _h(r'%s|Sede|Provincia')
            anag.numtel =    _h(r'%s|Contatti|Telefono')
            anag.numfax =    _h(r'%s|Contatti|Fax')
            anag.email =     _h(r'%s|Contatti|Email')
        
        read_anag(self.anag_fornit, 'CedentePrestatore')
        read_anag(self.anag_cliente, 'CessionarioCommittente')
        
        for body in self.dom_body:
            
            dgen = body.getElementsByTagName('DatiGenerali')[0]
            ddet = body.getElementsByTagName('DatiBeniServizi')[0]
            
            def g(*v): 
                return self.get_value(dgen, *v)
            
            self.docs.append(_FTEL_Head())
            h = self.docs[-1]
            
            h.tipdoc = g('DatiGeneraliDocumento|TipoDocumento')
            h.divisa = g('DatiGeneraliDocumento|Divisa')
            h.datdoc = g('DatiGeneraliDocumento|Data', stod)
            h.numdoc = g('DatiGeneraliDocumento|Numero')
            h.totdoc = g('DatiGeneraliDocumento|ImportoTotaleDocumento', float)
            h.ritacc = g('DatiGeneraliDocumento|DatiRitenuta|ImportoRitenuta', float)
            h.bollov = g('DatiGeneraliDocumento|DatiBollo|ImportoBollo', float)
            
            h.oa_num = g('DatiOrdineAcquisto|IdDocumento')
            h.oa_dat = g('DatiOrdineAcquisto|Data', stod)
            h.oa_cig = g('DatiOrdineAcquisto|CodiceCIG')
            h.oa_cup = g('DatiOrdineAcquisto|CodiceCUP')
            
            for det in ddet.getElementsByTagName('DettaglioLinee'):
                
                def d(*v, **w):
                    return self.get_value(det, *v, **w)
                
                h.righe.append(_FTEL_Body())
                r = h.righe[-1]
                
                r.numriga =     d('NumeroLinea')
                r.codart =      d('CodiceArticolo|CodiceValore')
                r.descriz =     d('Descrizione')
                r.qta =         d('Quantita', float)
                r.unimis =      d('UnitaMisura')
                r.prezzo =      d('PrezzoUnitario', float)
                r.sconto_pe1 =  d('ScontoMaggiorazione|Percentuale', float, index=0)
                r.sconto_pe2 =  d('ScontoMaggiorazione|Percentuale', float, index=1)
                r.sconto_pe3 =  d('ScontoMaggiorazione|Percentuale', float, index=2)
                r.sconto_pe4 =  d('ScontoMaggiorazione|Percentuale', float, index=3)
                r.sconto_pe5 =  d('ScontoMaggiorazione|Percentuale', float, index=4)
                r.sconto_pe6 =  d('ScontoMaggiorazione|Percentuale', float, index=5)
                r.sconto_val =  d('ScontoMaggiorazione|Importo', float)
                r.totale =      d('PrezzoTotale', float)
                r.aliqiva =     d('AliquotaIVA', float)
            
            _totdoc = 0
            
            for tot in ddet.getElementsByTagName('DatiRiepilogo'):
                
                def i(*v):
                    return self.get_value(tot, *v)
                
                h.totiva.append(_FTEL_RigaIva())
                t = h.totiva[-1]
                
                t.aliqiva = i('AliquotaIVA', float)
                t.imponib = i('ImponibileImporto', float)
                t.imposta = i('Imposta', float)
                t.esigiva = i('EsigibilitaIVA')
                t.natura = i('Natura')
                t.rifnorm = d('RiferimentoNormativo')
                
                _totdoc += (t.imponib + t.imposta)
            
            if h.totdoc is None:
                h.totdoc = _totdoc
            
            try:
                
                dp = body.getElementsByTagName('DatiPagamento')[0]
                
                condpag = self.get_value(dp, 'CondizioniPagamento')
                
                for detpag in dp.getElementsByTagName('DettaglioPagamento'):
                    
                    def r(*v):
                        return self.get_value(detpag, *v)
                    
                    h.scadenze.append(_FTEL_RigaScadenza())
                    s = h.scadenze[-1]
                    
                    s.condpag = condpag
                    s.modpag =  r('ModalitaPagamento')
                    s.datscad = r('DataScadenzaPagamento', stod)
                    if s.datscad is None:
                        gg = r('GiorniTerminiPagamento', int)
                        if gg:
                            s.datscad = h.datdoc + gg
                    s.impscad = r('ImportoPagamento', float)
                    s.banca =   r('IstitutoFinanziario')
                    s.iban =    r('IBAN')
                    s.abi =     r('ABI')
                    s.cab =     r('CAB')
                    s.bic =     r('BIC')
            except:
                pass
            
            if load_attachments:
                for att in body.getElementsByTagName('Allegati'):
                    
                    def s(*v):
                        return self.get_value(att, *v)
                    
                    a = s('Attachment')
                    if a:
                        a_stream = base64.b64decode(a)
                        
                        a_filename = s('NomeAttachment')
                        a_filetype = None
                        
                        ac = s('AlgoritmoCompressione') or ''
                        if a_filename.lower().endswith('.zip') or ac.lower() == 'zip' and not a_stream.startswith('%PDF'):
                            f = StringIO(a_stream)
                            z = zipfile.ZipFile(f)
                            for zfilename in z.namelist():
                                if zfilename.lower().endswith('.pdf'):
                                    z.read(zfilename)
                                    a_filename = zfilename
                                    a_stream = z.read(zfilename)
                                    a_filetype = 'PDF'
                                    break
                            z.close()
                        
                        if a_filename.lower().endswith('.pdf') or (s('FormatoAttachment') or '') == 'pdf':
                            a_filetype = 'PDF'
                        
                        if a_filetype:
                            h.allegati.append(_FTEL_Allegato())
                            a = h.allegati[-1]
                            a.filetype = a_filetype
                            a.filename = a_filename
                            a.descriz = s('DescrizioneAttachment')
                            a.stream = a_stream


def get_node_value(node):
    return node.firstChild.nodeValue


def stod(sd): #YYYY-MM-DD
    try:
        _y = int(sd[0:4])
        _m = int(sd[5:7])
        _d = int(sd[8:10])
        return datetime.date(_y, _m, _d)
    except:
        return None
