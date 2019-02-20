#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/vendite/export.py
# Copyright:    (C) 2018 Evolvia S.r.l. <info@evolvia.srl>
# ------------------------------------------------------------------------------

import os
from ftel.vendite.dbtables import FTEL_NOCODE
from anag.clienti import ClientiDialog
from wx.grid import EVT_GRID_CELL_LEFT_DCLICK, EVT_GRID_CELL_LEFT_CLICK
from stormdb.db import get_db
def open_dir(f):
    if os.sys.platform.startswith('win'):
        f = f.replace('/', '\\')
    return os.startfile(f)  # @UndefinedVariable

import wx
import awc.controls.windows as aw
import awc.controls.dbgrid as dbglib
from awc.controls.linktable import EVT_LINKTABCHANGED

import ftel.vendite.export_wdr as wdr
import ftel.vendite.dbtables as dbfe

import Env
import report as rpt


FRAME_TITLE = "Esportazione documenti in formato Fattura Elettronica"


class ExportGrid(dbglib.ADB_Grid):
    
    _canedit = True
    
    def __init__(self, parent, dbdoc):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbdoc,
                                 can_edit=True, can_insert=False, on_menu_select='row')
        
        doc = self.dbdoc = dbdoc
        tpd = doc.config
        pdc = doc.pdc
        cli = pdc.anag
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self._col_rfa = ci(doc, 'ftel_rifamm')
        self._col_num = ci(doc, 'ftel_numtrasm')
        self._col_oan = ci(doc, 'ftel_ordnum')
        self._col_oad = ci(doc, 'ftel_orddat')
        self._col_cig = ci(doc, 'ftel_codcig')
        self._col_cup = ci(doc, 'ftel_codcup')
        self._col_bol = ci(doc, 'ftel_bollovirt')
        self._col_tot = ci(doc, 'totimporto')
        self._col_tiv = ci(doc, 'totimposta')
        self._col_cdf = ci(pdc, 'ftel_codice')
        self._col_pec = ci(pdc, 'ftel_pec')
        self._col_sts = ci(doc, 'ftel_eeb_status')
        
        TYPEVAL = self.TypeFloat(Env.Azienda.BaseTab.VALINT_INTEGERS, Env.Azienda.BaseTab.VALINT_DECIMALS)
        
        if 'fe_sel' in doc.GetAllColumnsNames():
            self.COL_SELECT = self.AddColumn(doc, 'fe_sel', 'Sel.', col_width=30, col_type=self.TypeCheck())
        
        self.COL_TPDCOD = self.AddColumn(tpd, 'codice', 'Cod.', col_width=40)
        self.COL_TPDDES = self.AddColumn(tpd, 'descriz', 'Documento', col_width=110)
        
        self.tipsez = {}
        regcon = dbfe.adb.DbTable('contab_h', 'regcon')
        regcon.AddJoin('regiva')
        regcon.Reset()
        
        col_tipdoc = ci(doc, 'id_tipdoc')
        col_numdoc = ci(doc, 'numdoc')
        col_regcon = ci(doc, 'id_reg')
        def get_numdoc(row, col):
            rs = self.dbdoc.GetRecordset()
            id_tipdoc = rs[row][col_tipdoc]
            if not id_tipdoc in self.tipsez:
                id_regcon = rs[row][col_regcon]
                regcon.Get(id_regcon)
                self.tipsez[id_tipdoc] = regcon.regiva.numdocsez
            numdoc = rs[row][col_numdoc]
            numsez = self.tipsez[id_tipdoc]
            if numsez:
                numdoc = '%s/%s' % (numdoc, numsez)
            return numdoc
        
        self.COL_NUMDOC = self.AddColumn(doc, 'numdoc', 'Num.', col_width=70, 
                                         get_cell_func=get_numdoc)
        
        self.COL_DATDOC = self.AddColumn(doc, 'datdoc', 'Data', col_type=self.TypeDate())
        self.COL_PDCCOD = self.AddColumn(pdc, 'codice', 'Cod.', col_width=50)
        self.COL_PDCDES = self.AddColumn(pdc, 'descriz', 'Cliente', col_width=200, is_fittable=True)
        self.COL_CODFIS = self.AddColumn(cli, 'codfisc', 'Cod.Fiscale', col_width=140)
        self.COL_NAZION = self.AddColumn(cli, 'nazione', 'Naz.', col_width=50)
        self.COL_PARIVA = self.AddColumn(cli, 'piva', 'P.IVA', col_width=100)
        self.COL_TOTDOC = self.AddColumn(doc, 'totimporto', 'Tot.Documento', col_type=TYPEVAL)
        self.COL_BOLLOV = self.AddColumn(doc, 'ftel_bollovirt', 'Bollo', col_type=self.TypeFloat(3, Env.Azienda.BaseTab.VALINT_DECIMALS))
        self.COL_CODDES = self.AddColumn(pdc, 'ftel_codice', 'CDFE', col_width=70)
        self.COL_INDPEC = self.AddColumn(pdc, 'ftel_pec', 'PEC', col_width=180)
        if Env.Azienda.BaseTab.is_eeb_enabled():
            self.COL_MESSAG = self.AddColumn(doc, 'ftel_eeb_message', 'Errore', col_width=500)
        self.COL_NUMTRA = self.AddColumn(doc, 'ftel_numtrasm', 'N.Tras.', col_type=self.TypeInteger(5))
        self.COL_ID_DOC = self.AddColumn(doc, 'id', '#doc', col_width=1)
        self.COL_ID_PDC = self.AddColumn(pdc, 'id', '#pdc', col_width=1)
        
        self.CreateGrid()
        
        if not self._canedit:
            self.AddTotalsRow(self.COL_PDCDES, 'Totali', (ci(doc, 'ftel_bollovirt'),))
    
    def GetAttr(self, row, col, rscol, attr):
        attr = dbglib.ADB_Grid.GetAttr(self, row, col, rscol, attr)
        doc = self.dbdoc
        rs = doc.GetRecordset()
        if 0 <= row < len(rs):
            r = rs[row]
            colors = True
            if rscol == self._col_bol:
                if not r[self._col_bol] and not r[self._col_tiv]:
                    attr.SetBackgroundColour(doc.COLOR_DATI_MANCANTI)
                    colors = False
            elif rscol in (self._col_cdf, 
                         self._col_pec):
                if len(r[self._col_cdf] or '') == 0 and len(r[self._col_pec] or '') == 0:
                    attr.SetBackgroundColour(doc.COLOR_DATI_MANCANTI)
                    colors = False
            if colors:
                if r[self._col_sts] is None or r[self._col_sts].strip() == "":
                    attr.SetBackgroundColour(doc.STATUS_COLORS[doc.STATUS_XML_DA_GENERARE])
                elif r[self._col_sts] in doc.STATUS_COLORS:
                    attr.SetBackgroundColour(doc.STATUS_COLORS[r[self._col_sts]])
                else:
                    attr.SetBackgroundColour('red')
        return attr


class ExportPanel(aw.Panel):
    
    window_filler = wdr.FtelExportFunc
    report_name = "Documenti fattura elettronica"
    
    def __init__(self, parent):
        
        aw.Panel.__init__(self, parent)
        self.window_filler(self)
        cn = self.FindWindowByName
        
        if Env.Azienda.BaseTab.is_eeb_enabled():
            cn('butgen').SetLabel('Avvia trasmissione')
        
        self.dbdocs = dbfe.FatturaElettronica()
        self.dbdocs.AddField('0.0', 'fe_sel')
        self.dbdocs.Reset()
        
        self.gridocs = ExportGrid(cn('pangridocs'), self.dbdocs)
        
        self.dbpfe = dbfe.ProgrMagazz_FatturaElettronica()
        self.UpdateNumProgr()
        
        today = Env.Azienda.Login.dataElab
#         cn('data1').SetValue(Env.DateTime.Date(today.year, today.month, 1))
        cn('data1').SetValue(Env.DateTime.Date(today.year, 1, 1))
        cn('data2').SetValue(today)
        c = cn('id_pdc')
        if c:
            c.SetFilter('0')
        
        self.init_colors()
        
        def set_focus():
            self.FindWindowByName('data1').SetFocus()
        wx.CallAfter(set_focus)
        
#         self.UpdateData()
        
        self.gridocs.Bind(EVT_GRID_CELL_LEFT_CLICK, self.OnCellClicked)
        
        self.gridocs.Bind(EVT_GRID_CELL_LEFT_DCLICK, self.OnCellDoubleClicked)
#         for name in 'status_da_inviare status_in_lavorazione status_trasmessi'.split():
#             self.Bind(wx.EVT_CHECKBOX, self.OnUpdateData, cn(name))
        self.Bind(wx.EVT_CHECKBOX, self.OnUpdateData)
        
        for name, func in (('butsrc', self.OnUpdateData),
                           ('butprt', self.OnPrintData),
                           ('butgen', self.OnGeneraFile),):
            c = cn(name)
            if c:
                self.Bind(wx.EVT_BUTTON, func, c)
    
    def OnUpdateData(self, event):
        self.UpdateData()
    
    def OnCellClicked(self, event):
        event.Skip()
    
    def OnCellDoubleClicked(self, event):
        row, col = event.GetRow(), event.GetCol()
        doc = self.dbdocs
        doc.MoveRow(row)
        dlg = ClientiDialog(self, onecodeonly=doc.id_pdc)
        dlg.OneCardOnly(doc.id_pdc)
        dlg.CenterOnScreen()
        if col == self.gridocs.COL_CODDES:
            dlg.FindWindowByName('ftel_codice').SetFocus()
        elif col == self.gridocs.COL_INDPEC:
            dlg.FindWindowByName('ftel_pec').SetFocus()
        _reload = (dlg.ShowModal() > 0)
        dlg.Destroy()
        if _reload:
            self.UpdateData()
        event.Skip()
    
    def init_colors(self):
        d = self.dbdocs
        c = d.STATUS_COLORS
        cn = self.FindWindowByName
        cn('panel_status_x').SetBackgroundColour(c[d.STATUS_XML_DA_GENERARE])
        cn('panel_status_g').SetBackgroundColour(c[d.STATUS_XML_GENERATO])
        cn('panel_status_a').SetBackgroundColour(c[d.STATUS_ATTESA_ESITO])
        cn('panel_status_q').SetBackgroundColour(c[d.STATUS_IN_CODA_X_SDI])
        cn('panel_status_c').SetBackgroundColour(c[d.STATUS_CONSEGNATO])
        cn('panel_status_m').SetBackgroundColour(c[d.STATUS_MANCATACONS])
        cn('panel_status_e').SetBackgroundColour(c[d.STATUS_ERRORE])
        cn('panel_status_z').SetBackgroundColour(c[d.STATUS_PA_ACCETTATI])
        cn('panel_status_k').SetBackgroundColour(c[d.STATUS_PA_RIFIUTATI])
        cn('panel_status_t').SetBackgroundColour(c[d.STATUS_PA_DECOTERM])
    
    def OnPrintData(self, event):
        self.PrintData()
    
    def OnGeneraFile(self, event):
        if self.Validate():
            if self.GeneraFile():
                self.UpdateData()
    
    def Validate(self):
        err = False
        return True
    
    def UpdateNumProgr(self):
        cn = self.FindWindowByName
        self.dbpfe.Retrieve()
        cn('numprogr').SetValue((self.dbpfe.progrimp1 or 0) + 1)
    
    def _get_values(self):
        cn = self.FindWindowByName
        data1, data2 = map(lambda x: cn(x).GetValue(), 'data1 data2'.split())
        if data1 is None:
            err = 'Manca la data di partenza'
        elif data2 is None:
            err = 'Manca la data di fine'
        else:
            err = None
        if err:
            aw.awu.MsgDialog(self, "Dati errati:\n%s" % err, style=wx.ICON_ERROR)
            return None
        return data1, data2
    
    def UpdateData(self):
        cn = self.FindWindowByName
        self.UpdateNumProgr()
        _ = self._get_values()
        if _ is None:
            return False
        data1, data2 = _
        
        docs = self.dbdocs
        docs.ClearFilters()
        if Env.Azienda.BaseTab.FTEL_SOLITA:
            docs.AddFilter('(anag.nazione IS NULL OR anag.nazione="" OR anag.nazione="IT")')
        docs.AddFilter('doc.datdoc>=%s AND doc.datdoc<=%s', data1, data2)
        tipicli = cn('tipicli').GetValue()
        if tipicli == 'B':
            docs.AddFilter('(pdc.ftel_codice IS NULL OR LENGTH(pdc.ftel_codice)=7)')
        elif tipicli == 'P':
            docs.AddFilter('(pdc.ftel_codice IS NOT NULL AND LENGTH(pdc.ftel_codice)=6)')
        flags = []
        filter0 = ''
        enable = True
        if cn('status_x').IsChecked():
            filter0 = '(doc.ftel_eeb_status IS NULL OR doc.ftel_eeb_status="")'
            flags.append(docs.STATUS_XML_DA_GENERARE)
        if cn('status_g').IsChecked():
            flags.append(docs.STATUS_XML_GENERATO)
            enable = False
        if cn('status_aq').IsChecked():
            flags.append(docs.STATUS_ATTESA_ESITO)
            flags.append(docs.STATUS_IN_CODA_X_SDI)
            enable = False
        if cn('status_c').IsChecked():
            flags.append(docs.STATUS_CONSEGNATO)
            enable = False
        if cn('status_m').IsChecked():
            flags.append(docs.STATUS_MANCATACONS)
            enable = False
        if cn('status_e').IsChecked():
            flags.append(docs.STATUS_ERRORE)
        if cn('status_z').IsChecked():
            flags.append(docs.STATUS_PA_ACCETTATI)
        if cn('status_k').IsChecked():
            flags.append(docs.STATUS_PA_RIFIUTATI)
        if cn('status_t').IsChecked():
            flags.append(docs.STATUS_PA_DECOTERM)
        if flags:
            flt = 'doc.ftel_eeb_status IN (%s)' % ','.join(['"%s"' % f for f in flags])
            if filter0:
                flt = '%s OR %s' % (filter0, flt)
            docs.AddFilter(flt)
            e = not ('T' in flags or 'A' in flags or 'Z' in flags or 'T' in flags)
            cn('butgen').Enable(e)
            cn('numprogr').Enable(e)
        else:
            docs.AddFilter('FALSE')
            cn('butgen').Disable()
        docs.ClearOrders()
        docs.AddOrder('doc.datdoc')
        docs.AddOrder('doc.id_tipdoc')
        docs.AddOrder('doc.numdoc')
#         if Env.Azienda.Login.dataElab.year < 2019:
#             docs.AddFilter('(pdc.ftel_codice IS NOT NULL AND LENGTH(pdc.ftel_codice)=6)')
        wx.BeginBusyCursor()
        try:
            docs.Retrieve()
        finally:
            wx.EndBusyCursor()
        mp_err = []
        ai_err = []
        if not docs.IsEmpty():
            try:
                wait = aw.awu.WaitDialog(self, message="Controllo dati in corso", style=wx.ICON_INFORMATION)
                col_id = docs._GetFieldIndex('id', inline=True)
                docids = [r[col_id] for r in docs._info.rs]
                db = get_db()
                cmd = """
                    SELECT mpa.id, mpa.codice, mpa.descriz, mpa.ftel_tippag, mpa.ftel_modpag
                      FROM movmag_h doc
                      JOIN modpag mpa ON mpa.id=doc.id_modpag
                     WHERE doc.id IN (%s) AND (mpa.ftel_tippag IS NULL OR NOT mpa.ftel_tippag LIKE 'TP%%' OR
                                               mpa.ftel_modpag IS NULL OR NOT mpa.ftel_modpag LIKE 'MP%%')
                  GROUP BY mpa.id, mpa.codice, mpa.descriz, mpa.ftel_tippag, mpa.ftel_modpag
                  ORDER BY mpa.codice
                """ % (','.join(map(str, docids)))
                if not db.Retrieve(cmd):
                    aw.awu.MsgDialog(self, db.dbError.description, style=wx.ICON_ERROR)
                    enable = False
                mp_err = db.rs
                cmd = """
                    SELECT aliq.id, aliq.codice, aliq.descriz, aliq.ftel_natura
                      FROM movmag_b mov
                      JOIN movmag_h doc ON doc.id=mov.id_doc
                      JOIN aliqiva aliq ON aliq.id=mov.id_aliqiva
                     WHERE doc.id IN (%s) AND aliq.perciva=0 AND (aliq.ftel_natura IS NULL OR NOT aliq.ftel_natura LIKE 'N%%')
                  GROUP BY aliq.id, aliq.codice, aliq.descriz, aliq.ftel_natura
                  ORDER BY aliq.codice
                """ % (','.join(map(str, docids)))
                if not db.Retrieve(cmd):
                    aw.awu.MsgDialog(self, db.dbError.description, style=wx.ICON_ERROR)
                    enable = False
                ai_err = db.rs
            finally:
                wait.Destroy()
        if len(mp_err) > 0:
            msg = "Attenzione: le seguenti mod.pagamento sono da classificare:\n%s" % ','.join([mp[1] for mp in mp_err])
            aw.awu.MsgDialog(self, msg, style=wx.ICON_ERROR)
            enable = False
        if len(ai_err) > 0:
            msg = "Attenzione: le seguenti aliquote IVA sono da classificare:\n%s" % ','.join([ai[1] for ai in ai_err])
            aw.awu.MsgDialog(self, msg, style=wx.ICON_ERROR)
            enable = False
        e = cn('butgen').IsEnabled() and not docs.IsEmpty()
        cn('butgen').Enable(e)
        cn('numprogr').Enable(e)
        if enable and cn('selaut').IsChecked():
            col = docs._GetFieldIndex('fe_sel', inline=True)
            for r in docs.GetRecordset():
                r[col] = 1
        self.gridocs.ChangeData(docs.GetRecordset())
    
    def OnUpdateTotali(self, event):
        self.UpdateTotali()
        event.Skip()
    
    def UpdateTotali(self):
        cn = self.FindWindowByName
        reg = self.dbdocs.regcon
        wx.BeginBusyCursor()
        numdoc = totdoc = 0
        try:
            for doc in self.dbdocs:
                if reg.id != doc.id_reg:
                    reg.Get(doc.id_reg)
                if reg.config.pasegno == "D":
                    segno = +1
                else:
                    segno = -1
                totdoc += (doc.totimporto*segno)
                numdoc += 1
        finally:
            wx.EndBusyCursor()
        cn('docsel_num').SetValue(numdoc)
        cn('docsel_tot').SetValue(totdoc)
    
    def PrintData(self):
        rpt.Report(self, self.dbdocs, self.report_name)
    
    def GeneraFile(self):
        
        if self.dbdocs.IsEmpty():
            aw.awu.MsgDialog(self, "Nessun documento selezionato\nper la generazione del file")
            return False
        
        col = self.dbdocs._GetFieldIndex('id', inline=True)
        sel = self.dbdocs._GetFieldIndex('fe_sel', inline=True)
        docids = [r[col] for r in self.dbdocs._info.rs if r[sel]]
        
        msg = """Confermando, i %s documento saranno contrassegnati come trasmessi """\
              """ed il progressivo di trasmissione incrementerà di conseguenza.\n\n"""\
              """Confermi la generazione dei file da trasmettere?\n""" % len(docids)
        
        if aw.awu.MsgDialog(self, msg, style=wx.ICON_QUESTION | wx.YES_NO | wx.NO_DEFAULT) == wx.ID_YES:
            
            numprogr = self.FindWindowByName('numprogr').GetValue()
            
            path = None
            
            def firma_pa(pathname, filename):
                while True:
                    msg = "Il documento a PA necessita di firma elettronica.\nFirmare il file %s e confermare per effettuare l'invio.\n\nHai firmato il file ?" % filename
                    style = wx.ICON_QUESTION|wx.YES_NO|wx.YES_DEFAULT
                    r = aw.awu.MsgDialog(self, msg, "Documento a Pubblica Amministrazione", style=style)
                    filename_p7m = filename+'.p7m'
                    if r == wx.ID_YES:
                        if os.path.isfile(os.path.join(pathname, filename_p7m).replace('/', '\\')):
                            return filename_p7m
                        aw.awu.MsgDialog(self, "File firmato non trovato", style=wx.ICON_ERROR)
                    if r == wx.ID_NO:
                        msg = "Il file non firmato non può essere inviato.\nConfermi la gestione manuale dell'invio?"
                        if aw.awu.MsgDialog(self, msg, style=wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT) == wx.ID_YES:
                            return None
            
            void = 0
            wait = aw.awu.WaitDialog(self, title="Trasmissione in corso...", maximum=len(docids))
            try:
                doc = dbfe.FatturaElettronica()
                for n, xdoc in enumerate(self.dbdocs):
                    if xdoc.fe_sel:
                        if len(xdoc.pdc.ftel_codice or '') == 0 and len(xdoc.pdc.ftel_pec or '') == 0:
                            void += 1
                        else:
                            doc.Get(xdoc.id)
                            wait.SetMessage('%s n. %s del %s' % (doc.config.descriz,
                                                                 doc.numdoc,
                                                                 doc.datdoc.Format()))
                            path, _name = doc.ftel_make_files(numprogr, firma_pa)
                            numprogr += 1
                    wait.SetValue(n)
#             except Exception, e:
#                 aw.awu.MsgDialog(self, message=' '.join(map(str, e.args)), style=wx.ICON_ERROR)
            finally:
                wait.Destroy()
            if void:
                aw.awu.MsgDialog(self, '%d documenti non esportati per mancanza codice destinatario o pec' % void, 
                                 style=wx.ICON_WARNING)
            
            if path and not Env.Azienda.BaseTab.is_eeb_enabled():
                open_dir(path)
                aw.awu.MsgDialog(self, """File generati correttamente, provvedere al loro invio.""", style=wx.ICON_INFORMATION)
            
            self.UpdateData()
            
            return True
        
        return False


class ExportFrame(aw.Frame):
    
    Panel = ExportPanel
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = self.Panel(self)
        self.AddSizedPanel(self.panel)


def apri_cartella_files():
    open_dir(dbfe.FatturaElettronica.ftel_get_basepath())



def check_modpag():
    modpag = dbfe.adb.DbTable('modpag')
    modpag.AddFilter('modpag.ftel_tippag NOT LIKE "TP%" OR modpag.ftel_modpag NOT LIKE "MP%"')
    modpag.Retrieve()
    if not modpag.IsEmpty():
        aw.awu.MsgDialog(None, "Per procedere occorre configurare le modalità di pagamento secondo le classificazioni della fattura elettronica", style=wx.ICON_ERROR)
        return False
    return True


def check_aliqiva():
    aliqiva = dbfe.adb.DbTable('aliqiva')
    aliqiva.AddFilter('aliqiva.perciva=0 AND aliaiva.ftel_natira NOT LIKE "N%"')
    aliqiva.Retrieve()
    if not aliqiva.IsEmpty():
        aw.awu.MsgDialog(None, "Per procedere occorre configurare le modalità di pagamento secondo le classificazioni della fattura elettronica", style=wx.ICON_ERROR)
        return False
    return True
