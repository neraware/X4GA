#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         contab/solpag.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2017 Neraware <fc@neraware.com>
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


import wx
import awc.controls.dbgrid as dbglib

import awc.controls.windows as aw

import contab.dbtables as dbc
import anag.lib as alib
from anag.clienti import ClientiDialog

import Env
from contab.pdcint import ScadenzarioColorsGridMixin,\
    ScadenzarioColorsPanelMixin
from contab.pdcint_wdr import PdcScadenzarioColorsFunc
from wx.grid import EVT_GRID_CELL_LEFT_DCLICK
from contab.pcf import PcfDialog
from awc.controls.linktable import EVT_LINKTABCHANGED
from magazz.dbtables import SendMailInfo, DocMag
bt = Env.Azienda.BaseTab
stdcolor = Env.Azienda.Colours

import stormdb as adb

import contab.solpag_wdr as wdr

from string import Template
from comm.comsmtp import SendDocumentMail

import report as rpt

FRAME_TITLE = "Solleciti di pagamento"


class RiepilogoClientiTable(adb.DbTable):
    
    def __init__(self):
        adb.DbTable.__init__(self, 'pcf', fields=None)
        _cau = self.AddJoin('cfgcontab', 'caus', idLeft='id_caus', fields=None)
        _mpa = self.AddJoin('modpag', idLeft='id_modpag', fields=None)
        _pdc = self.AddJoin('pdc', idLeft='id_pdc', fields=None)
        _tpa = _pdc.AddJoin('pdctip', 'tipana', idLeft='id_tipo', fields=None)
        _cli = _pdc.AddJoin('clienti', 'anag', idLeft='id', fields=None)
        self.AddBaseFilter("tipana.tipo='C'")
        self.AddBaseFilter("pcf.imptot<>pcf.imppar")
        self.AddBaseFilter("pcf.datscad<'%s'" % Env.DateTime.today())
        self.AddGroupOn('pdc.id',         'pdc_id')
        self.AddGroupOn('pdc.codice',     'pdc_codice')
        self.AddGroupOn('pdc.descriz',    'pdc_descriz')
        self.AddGroupOn('pdc.codice',     'anag_codice')
        self.AddGroupOn('pdc.descriz',    'anag_descriz')
        self.AddGroupOn('anag.indirizzo', 'anag_indirizzo')
        self.AddGroupOn('anag.cap',       'anag_cap')
        self.AddGroupOn('anag.citta',     'anag_citta')
        self.AddGroupOn('anag.prov',      'anag_prov')
        self.AddGroupOn('anag.codfisc',   'anag_codfisc')
        self.AddGroupOn('anag.piva',      'anag_piva')
        self.AddGroupOn('anag.docsemail', 'anag_email')
        self.AddGroupOn('anag.numtel',    'anag_numtel')
        self.AddGroupOn('anag.numfax',    'anag_numfax')
        self.AddGroupOn('anag.ctt1nome',  'anag_contatto')
        self.AddTotalOf('pcf.imptot', 'imptot')
        self.AddTotalOf('pcf.imppar', 'imppar')
        self.AddTotalOf('COALESCE(pcf.imptot, 0)-COALESCE(imppar, 0)', 'saldo')
        self.AddOrder('pdc.descriz')
        self.Reset()


evt_CLIENTECHANGED = wx.NewEventType()
EVT_CLIENTECHANGED = wx.PyEventBinder(evt_CLIENTECHANGED, 0)

class ClienteChangedEvent(wx.PyCommandEvent):
    
    id_pdc = None
    
    def __init__(self):
        wx.PyCommandEvent.__init__(self, evt_CLIENTECHANGED)

    def SetIdPdc(self, val):
        self.id_pdc = val

    def GetIdPdc(self):
        return self.id_pdc

evt_RELOAD_DATA = wx.NewEventType()
EVT_RELOAD_DATA = wx.PyEventBinder(evt_RELOAD_DATA, 0)

class ReloadDataEvent(wx.PyCommandEvent):
    
    def __init__(self):
        wx.PyCommandEvent.__init__(self, evt_RELOAD_DATA)


class RiepilogoClientiGrid(dbglib.ADB_Grid):
    
    def __init__(self, parent, dbtot):
        
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbtot, can_edit=False, can_insert=False, on_menu_select='row')
        self.dbtot = dbtot
        
        NI, ND = Env.Azienda.BaseTab.VALINT_INTEGERS, Env.Azienda.BaseTab.VALINT_DECIMALS
        
        self.AddColumn(dbtot, 'pdc_codice', 'Cod.', col_width=50)
        self.AddColumn(dbtot, 'pdc_descriz', 'Cliente', col_width=100, is_fittable=True)
        self.AddColumn(dbtot, 'total_saldo', 'Scaduto', col_type=self.TypeFloat(NI, ND))
        self.AddColumn(dbtot, 'anag_email', 'Indirizzo', col_width=200)
        self.AddColumn(dbtot, 'pdc_id', '#pdc', col_width=1)
        
        self._col_email = dbtot._GetFieldIndex('anag_email')
        
        self.CreateGrid()
        
#         self.AppendContextMenuVoice('Scheda categoria', self.OnSchedaCatArt)
#         self.AppendContextMenuVoice('Elimina sconto', self.OnDeleteRow)
    
    def GetAttr(self, row, col, rscol, attr):
        attr = dbglib.ADB_Grid.GetAttr(self, row, col, rscol, attr)
        rs = self.dbtot.GetRecordset()
        if 0 <= row < len(rs):
            if len((rs[row][self._col_email] or '').strip()) == 0:
                attr.SetTextColour('red')
        return attr
    
    def OnRowSelected(self, event):
        row = event.GetRow()
        tot = self.dbtot
        if 0 <= row < tot.RowsCount():
            tot.MoveRow(row)
            id_pdc = tot.pdc_id
        else:
            id_pdc = None
        evt = ClienteChangedEvent()
        evt.SetIdPdc(id_pdc)
        self.GetEventHandler().AddPendingEvent(evt)
        event.Skip()


class PartiteScaduteClienteTable(dbc.Pcf):
    
    def _AddPcfJoins(self, pcf=None):
        dbc.Pcf._AddPcfJoins(self, pcf=pcf)
        self['pdc'].AddJoin('clienti', 'anag', idLeft='id')
        self.AddBaseFilter("tipana.tipo='C'")
        self.AddBaseFilter("pcf.imptot<>pcf.imppar")
        self.AddField('COALESCE(pcf.imptot, 0) - COALESCE(pcf.imppar, 0)', 'saldo')


class PartiteScaduteClienteGrid(dbglib.ADB_Grid, ScadenzarioColorsGridMixin):
     
    def __init__(self, parent, dbpcf):
         
        dbglib.ADB_Grid.__init__(self, parent, db_table=dbpcf, can_edit=True, can_insert=False, on_menu_select='row')
        ScadenzarioColorsGridMixin.__init__(self, dbpcf)
        
        self.dbpcf = dbpcf
        self.id_pdc = None
         
        pcf = dbpcf
        cau = pcf.caus
        mpa = pcf.modpag
        
        def ci(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        NI, ND = bt.VALINT_INTEGERS, bt.VALINT_DECIMALS
        
        self.COL_DATSCA = self.AddColumn(pcf, 'datscad', 'Scadenza', col_type=self.TypeDate())
        
        self.COL_CAUCOD = self.AddColumn(cau, 'codice',  'Caus.', col_width=40, is_editable=False, 
                                         linktable_info={'class':   alib.LinkTableCauContab,
                                                         'col_id':  ci(pcf, 'id_caus'),
                                                         'col_cod': ci(cau, 'codice'),
                                                         'col_des': ci(cau, 'descriz')})
        
        self.COL_NUMDOC = self.AddColumn(pcf, 'numdoc',  'Num.', col_width=60)
        self.COL_DATDOC = self.AddColumn(pcf, 'datdoc',  'Data', col_type=self.TypeDate())
        
        self.COL_MPACOD = self.AddColumn(mpa, 'codice',  'M/Pag.', col_width=40, is_editable=False, 
                                        linktable_info={'class':   alib.LinkTableModPag,
                                                        'col_id':  ci(pcf, 'id_modpag'),
                                                        'col_cod': ci(mpa, 'codice'),
                                                        'col_des': ci(mpa, 'descriz')})
        
        self.COL_SALDO =  self.AddColumn(pcf, 'saldo',     'Saldo', col_type=self.TypeFloat(NI, ND))
        
        self.COL_NOSOLL = self.AddColumn(pcf, 'no_sollec', 'Escludi', col_type=self.TypeCheck(), col_width=60, is_editable=True)
        
        self.COL_CAUDES = self.AddColumn(cau, 'descriz',   'Causale', col_width=140, is_fittable=True)
        self.COL_MPADES = self.AddColumn(mpa, 'descriz',   'Mod.pagamento', col_width=140)
        
        self.COL_IMPTOT = self.AddColumn(pcf, 'imptot',    'Importo', col_type=self.TypeFloat(NI, ND))
        self.COL_IMPPAR = self.AddColumn(pcf, 'imppar',    'Paregg.', col_type=self.TypeFloat(NI, ND))
        
        self.COL_SOLDT1 = self.AddColumn(pcf, 'soll1data', 'Sollecito1', col_type=self.TypeDate())
        self.COL_SOLDT2 = self.AddColumn(pcf, 'soll2data', 'Sollecito2', col_type=self.TypeDate())
        self.COL_SOLDT3 = self.AddColumn(pcf, 'soll3data', 'Sollecito3', col_type=self.TypeDate())
        
        self.COL_NOTE =   self.AddColumn(pcf, 'note', 'Note', col_width=300)
        
        self.COL_PCF_ID = self.AddColumn(pcf, 'id', '#pcf', col_width=1)
        
        self.CreateGrid()
    
    def GetAttr(self, *args, **kwargs):
        rs = self.dbpcf.GetRecordset()
        return ScadenzarioColorsGridMixin.ScadenzarioColorsGetAttr(self, rs, *args, **kwargs)
    
    def _SwapCheckValue(self, row, col):
        checked = dbglib.ADB_Grid._SwapCheckValue(self, row, col)
        if col == self.COL_NOSOLL:
            pcf = self.dbpcf
            pcf.MoveRow(row)
            cmd = "UPDATE pcf SET no_sollec=%s WHERE id=%s" % (int(checked), pcf.id)
            pcf._info.db.Execute(cmd)
            self.GetEventHandler().AddPendingEvent(ReloadDataEvent())
        return checked


class GiorniScadenzaException(Exception):
    pass

class SollecitiPagamentoPanel(aw.Panel, ScadenzarioColorsPanelMixin):
    
    _id_pdc = None
    _template = None
    _livello = None
    
    def __init__(self, *args, **kwargs):
        
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.SollecitiPagamentoFunc(self)
        cn = self.FindWindowByName
        
        self.dbtot = RiepilogoClientiTable()
        self.gridtot = RiepilogoClientiGrid(cn('pangridtot'), self.dbtot)
        
        self.dbpcf = PartiteScaduteClienteTable()
        self.gridpcf = PartiteScaduteClienteGrid(cn('pangridpcf'), self.dbpcf)
        
        PdcScadenzarioColorsFunc(cn('pancolors'))
        ScadenzarioColorsPanelMixin.__init__(self, self.gridpcf)
        
        cn('ggscad').SetValue(bt.GGSSOLPAG or 0)
        
        self.Bind(EVT_GRID_CELL_LEFT_DCLICK, self.OnClienteOpenDialog, self.gridtot)
        self.Bind(EVT_GRID_CELL_LEFT_DCLICK, self.OnPcfOpenDialog, self.gridpcf)
        
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBoxChanged)
        self.Bind(EVT_LINKTABCHANGED, self.OnUpdateClienti)
        
        self.Bind(EVT_RELOAD_DATA, self.OnUpdateClienti)
        self.Bind(EVT_CLIENTECHANGED, self.OnUpdatePartiteCliente)
        
        for name, func in (('butupdate', self.OnUpdateClienti),
                           ('butemail', self.OnSendMail),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def OnClienteOpenDialog(self, event):
        tot = self.dbtot
        tot.MoveRow(event.GetRow())
        dlg = ClientiDialog(self, onecodeonly=tot.pdc_id)
        dlg.OneCardOnly(tot.pdc_id)
        dlg.ShowModal()
        dlg.Destroy()
        self.UpdateClienti()
    
    def OnPcfOpenDialog(self, event):
        pcf = self.dbpcf
        row = event.GetRow()
        if 0 <= row < pcf.RowsCount():
            pcf.MoveRow(row)
            id_pcf = pcf.id
            dlg = PcfDialog(self)
            dlg.SetPcf(id_pcf)
            update = (dlg.ShowModal() in (1,2))
            dlg.Destroy()
            if update:
                self._id_pdc = pcf.id_pdc
                self.UpdateClienti()
        event.Skip()
    
    def OnCheckBoxChanged(self, event):
        name = event.GetEventObject().GetName()
        cn = self.FindWindowByName
        for p in 'esc ins rib rid'.split():
            if   name == '%s0'%p: cn('%s1'%p).SetValue(False); cn('%s2'%p).SetValue(False)
            elif name == '%s1'%p: cn('%s0'%p).SetValue(False); cn('%s2'%p).SetValue(False)
            elif name == '%s2'%p: cn('%s0'%p).SetValue(False); cn('%s1'%p).SetValue(False)
        self.UpdateClienti()
    
    def OnUpdateClienti(self, event):
        try:
            self.UpdateClienti()
        except GiorniScadenzaException:
            aw.awu.MsgDialog(self, "Definire numero giorni scadenza", style=wx.ICON_ERROR)
        except:
            self.gridtot.ChangeData([])
            self.gridpcf.ChangeData([])
        event.Skip()
    
    def ApplyFilters(self, dbt):
        
        cn = self.FindWindowByName
        
        dbt.ClearFilters()
        
        id_tipsol = cn('id_tipsol').GetValue()
        if id_tipsol is None:
            dbt.AddFilter('FALSE')
        else:
            
            dbt.AddFilter('(COALESCE(pcf.imptot, 0)-COALESCE(pcf.imppar, 0))>0')
            
            ggscad = cn('ggscad').GetValue()
            if ggscad == 0:
                raise GiorniScadenzaException
            
            date = Env.DateTime.today() - Env.DateTime.DateTimeDelta(days=ggscad)
            dbt.AddFilter("pcf.datscad<='%s'" % date.isoformat())
            
            tipsol = adb.DbTable('tipsolpag')
            tipsol.Get(id_tipsol)
            self._template = tipsol.template
            self._livello = tipsol.livello
            if cn('livx').IsChecked():
                if tipsol.livello == 1:
                    dbt.AddFilter('(pcf.soll1data IS NULL AND pcf.soll2data IS NULL AND pcf.soll3data IS NULL)')
                elif tipsol.livello == 2:
                    dbt.AddFilter('(pcf.soll1data IS NOT NULL AND pcf.soll2data IS NULL AND pcf.soll3data IS NULL)')
                elif tipsol.livello == 3:
                    dbt.AddFilter('(pcf.soll1data IS NOT NULL AND pcf.soll2data IS NOT NULL AND pcf.soll3data IS NULL)')
                else:
                    dbt.AddFilter('FALSE')
            
            sca1, sca2 = cn('datsca1').GetValue(), cn('datsca2').GetValue()
            doc1, doc2 = cn('datdoc1').GetValue(), cn('datdoc2').GetValue()
            
            sd1, sd2 = '', ''
            if sca1: sd1 = sca1.isoformat()
            if sca2: sd2 = sca2.isoformat()
            if sd1 or sd2:
                f = ''
                if sd1 == sd2:
                    f = 'pcf.datscad="%s"' % sd1
                elif sd1 and sd2:
                    f = 'pcf.datscad>="%s" AND pcf.datscad<="%s"' % (sd1, sd2)
                elif sd1:
                    f = 'pcf.datscad>="%s"' % sd1
                elif sd2:
                    f = 'pcf.datscad<="%s"' % sd2
                if f:
                    dbt.AddFilter(f)
            
            sd1, sd2 = '', ''
            if doc1: sd1 = doc1.isoformat()
            if doc2: sd2 = doc2.isoformat()
            if sd1 or sd2:
                f = ''
                if sd1 == sd2:
                    f = 'pcf.datdoc="%s"' % sd1
                elif sd1 and sd2:
                    f = 'pcf.datdoc>="%s" AND pcf.datdoc<="%s"' % (sd1, sd2)
                elif sd1:
                    f = 'pcf.datdoc>="%s"' % sd1
                elif sd2:
                    f = 'pcf.datdoc<="%s"' % sd2
                if f:
                    dbt.AddFilter(f)
            
            if cn('esc0').IsChecked():
                dbt.AddFilter('(pcf.no_sollec IS NULL OR pcf.no_sollec<>1)')
            elif cn('esc2').IsChecked():
                dbt.AddFilter('pcf.no_sollec=1')
            
            if cn('ins0').IsChecked():
                dbt.AddFilter('(pcf.insoluto IS NULL OR pcf.insoluto<>1)')
            elif cn('ins2').IsChecked():
                dbt.AddFilter('pcf.insoluto=1')
            
            if cn('rib0').IsChecked():
                dbt.AddFilter('pcf.riba IS NULL OR pcf.riba<>1')
            elif cn('rib2').IsChecked():
                dbt.AddFilter('pcf.riba=1')
            
            if cn('rid0').IsChecked():
                dbt.AddFilter('modpag.tipo<>"I"')
            elif cn('rid2').IsChecked():
                dbt.AddFilter('modpag.tipo="I"')
            
            id_agente = cn('id_agente').GetValue()
            if id_agente:
                dbt.AddFilter('anag.id_agente=%s', id_agente)
            
            id_zona = cn('id_zona').GetValue()
            if id_zona:
                dbt.AddFilter('anag.id_zona=%s', id_zona)
            
            id_status = cn('id_status').GetValue()
            if id_status:
                dbt.AddFilter('anag.id_status=%s', id_status)
            
            id_categ = cn('id_categ').GetValue()
            if id_categ:
                dbt.AddFilter('anag.id_categ=%s', id_categ)
    
    def UpdateClienti(self):
        tot = self.dbtot
        self.ApplyFilters(tot)
        wx.BeginBusyCursor()
        try:
            tot.Retrieve()
            self.gridtot.ChangeData(tot.GetRecordset())
            lastrow = None
            rs = tot.GetRecordset()
            for r in range(len(rs)):
                if rs[r][0] == self._id_pdc:
                    lastrow = r
                    break
            if lastrow is not None:
                self.gridtot.SelectRow(lastrow)
                tot.MoveRow(lastrow)
            self.UpdatePartiteCliente(id_pdc=self._id_pdc)
            self.FindWindowByName('butemail').SetLabel('Spedisci %d email' % tot.RowsCount())
            self.Layout()
        finally:
            wx.EndBusyCursor()
    
    def OnUpdatePartiteCliente(self, event):
        self.UpdatePartiteCliente()
        event.Skip()
    
    def UpdatePartiteCliente(self, id_pdc=None):
        tot = self.dbtot
        if id_pdc is None:
            row = self.gridtot.GetSelectedRows()[0]
            if 0 <= row < tot.RowsCount():
                id_pdc = tot.pdc_id
        if id_pdc is not None:
            pcf = self.dbpcf
            self.ApplyFilters(pcf)
            wx.BeginBusyCursor()
            try:
                pcf.AddFilter('pcf.id_pdc=%s' % id_pdc)
                pcf.Retrieve()
                self.gridpcf.ChangeData(pcf.GetRecordset())
            finally:
                wx.EndBusyCursor()
        else:
            self.gridpcf.ChangeData([])
    
    def OnSendMail(self, event):
        msg = "Confermi la spedizione di %d email ?" % self.dbtot.RowsCount()
        if aw.awu.MsgDialog(self, msg, style=wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT) == wx.ID_YES:
            self.SendMail()
            event.Skip()
    
    def SendMail(self):
        
        d = {}
        def fill(dbt, prefix=None):
            for name in dbt.GetAllColumnsNames():
                col = name
                if prefix:
                    col = '%s_%s' % (prefix, col)
                v = getattr(dbt, name)
                if isinstance(v, Env.DateTime.Date):
                    v = dbt.dita(v)
                elif isinstance(v, float):
                    v = dbt.sepnvi(v).rjust(12)
                d[col] = v
            for name in dbt._info.relTab:
                fill(dbt[name], '%s_%s' % (prefix, name))
        
        pcf = PartiteScaduteClienteTable()
        self.ApplyFilters(pcf)
        
        wait = aw.awu.WaitDialog(self, "Spedizione email in corso...", maximum=self.dbtot.RowsCount())
        wx.BeginBusyCursor()
        try:
            
            numsend = 0
            for n, tot in enumerate(self.dbtot):
                
                email = tot.anag_email or 'fabio.cassini@gmail.com'
                if len(email) == 0:
                    continue
                
                wait.SetMessage(tot.pdc_descriz)
                
                pcf.Retrieve('pcf.id_pdc=%s' % tot.pdc_id)
                
                fill(tot)
                
                if "^^" in self._template:
                    tmpl_text, tmpl_scad = self._template.split("^^")
                else:
                    tmpl_text = self._template
                    tmpl_scad = "$pcf_caus_descriz"
                
                tmpl_scad = tmpl_scad.replace('\n', '')
                p = []
                t = Template(tmpl_scad)
                for _ in pcf:
                    fill(pcf, 'pcf')
                    d['pcf_caus_descriz'] = (d['pcf_caus_descriz'] or '').ljust(20)
                    d['pcf_modpag_descriz'] = (d['pcf_modpag_descriz'] or '').ljust(20)
                    d['pcf_numdoc'] = (d['pcf_numdoc'] or '').rjust(5)
                    p.append(t.substitute(**d))
                d['partite'] = '\n'.join(p)
                
                t = Template(tmpl_text)
                txt = t.substitute(**d)
                
                sei = SendMailInfo()
                if bt.MAGDEMSENDDESC and bt.MAGDEMSENDADDR:
                    sender = '%s <%s>' % (bt.MAGDEMSENDDESC, bt.MAGDEMSENDADDR)
                else:
                    sender = None
                if not sender:
                    raise Exception("Manca l'indicazione del mittente della mail. Verificare il setup.")
                
                sei.sendto = "%s <%s>" % (tot.anag_descriz, tot.anag_email)
                sei.message = txt
                
                scad = adb.DbTable('contab_s', 'scad')
                scad.AddJoin('contab_h', 'reg', idLeft='id_reg')
                scad.AddFilter('reg.id_regiva IS NOT NULL')
                scad.Retrieve('scad.id_pcf IN (%s)' % ','.join(map(str, [p.id for p in pcf])))
                id_regs = []
                for _ in scad:
                    if not scad.id_reg in id_regs:
                        id_regs.append(scad.id_reg)
                
                pdf_attach = []
                if id_regs:
                    docs = DocMag()
                    docs.Retrieve('doc.id_reg IN (%s)' % ','.join(map(str, id_regs)))
                    docs._info.anag = docs.GetAnag()
                    pathname = '+Solleciti %s' % Env.Azienda.Login.dataElab.year#docs.GetPrintPathName()
                    filename = "Documenti sollecito %s - %s" % (tot.pdc_codice, self._livello)
                    r = rpt.Report(self, docs, docs.config.toolprint, noMove=True, output="STORE", 
                                   changepathname=pathname, changefilename=filename,)
                    if r.usedReport:
                        try:
                            pdf_attach.append(r.usedReport.GetFileName())
                        except:
                            pass
                
                sm = SendDocumentMail()
                sendto = sei.sendto
                if not sendto.startswith("<") and sendto.endswith(">"):
                    _, sendto = sendto[:-1].split("<")
                
                sendto = email
                
                sended = sm.send(SendFrom=sender,
                                 SendTo=sendto,#sei.sendto,
                                 Subject="Sollecito di pagamento",
                                 Message=sei.message,
                                 Attachments=pdf_attach)
                if sended:
                    cmd = "UPDATE pcf SET soll%sdata='%s' WHERE id IN (%s)" % (self._livello, 
                                                                               Env.Azienda.Login.dataElab,
                                                                               ','.join([str(p.id) for p in pcf]))
                    pcf._info.db.Execute(cmd)
                    sm.storicizza('Sollecito pagamento', tot.pdc_id, None, sm.error or "OK")
                    numsend += 1
                else:
                    raise Exception(sm.error)
                
                wait.SetValue(n)
            
            aw.awu.MsgDialog(self, "Sono state inviate %d email" % numsend, style=wx.ICON_INFORMATION)
            self.UpdateClienti()
            
        except KeyError, e:
            aw.awu.MsgDialog(self, "Valore non identificato:\n%s"  % ' '.join(e.args), style=wx.ICON_ERROR)
        
        finally:
            wx.EndBusyCursor()
            wait.Destroy()


class SollecitiPagamentoFrame(aw.Frame):
    """
    Frame Solleciti Pagamento
    """
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.AddSizedPanel(SollecitiPagamentoPanel(self, -1))
        self.CenterOnScreen()
