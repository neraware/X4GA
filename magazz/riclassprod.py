#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         magazz/listini.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2014 Fabio Cassini <fabio.cassini@gmail.com>
# ------------------------------------------------------------------------------

import wx
import magazz.listini_wdr as wdr
import magazz.dbtables as dbm

import awc.controls.windows as aw
import awc.controls.dbgrid as dbgrid
import anag.lib as alib


FRAME_TITLE = "Riclassificazione prodotti"


class RiclassProdGrid(dbgrid.ADB_Grid):
    
    def __init__(self, parent, dbpro):
        
        dbgrid.ADB_Grid.__init__(self, parent, db_table=dbpro, can_edit=True, can_insert=True, on_menu_select='row')
        
        self.dbscc = dbpro
        self.id_pdc = None
        
        pro = dbpro
        tip = pro.tipart
        cat = pro.catart
        gru = pro.gruart
        mar = pro.marart
        sts = pro.status
        frn = pro.fornit
        gpr = pro.gruprez
        
        def cn(tab, col):
            return tab._GetFieldIndex(col, inline=True)
        
        self.AddColumn(pro, 'selected', 'Sel', col_type=self.TypeCheck(), col_width=40)
        self.AddColumn(pro, 'codice', 'Codice', col_width=100)
        self.AddColumn(pro, 'descriz', 'Descrizione', col_width=240, is_fittable=True)
        
        self.AddColumn(tip, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableTipArt,
                                       'col_id':  cn(pro, 'id_tipart'),
                                       'col_cod': cn(tip, 'codice'),
                                       'col_des': cn(tip, 'descriz')})
        self.AddColumn(tip, 'descriz', 'Tipo', col_width=140)
        
        self.AddColumn(cat, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableCatArt,
                                       'col_id':  cn(pro, 'id_catart'),
                                       'col_cod': cn(cat, 'codice'),
                                       'col_des': cn(cat, 'descriz')})
        self.AddColumn(cat, 'descriz', 'Categoria', col_width=140)
        
        self.AddColumn(gru, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableGruArt,
                                       'col_id':  cn(pro, 'id_gruart'),
                                       'col_cod': cn(gru, 'codice'),
                                       'col_des': cn(gru, 'descriz')})
        self.AddColumn(gru, 'descriz', 'Gruppo', col_width=140)
        
        self.AddColumn(mar, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableMarArt,
                                       'col_id':  cn(pro, 'id_marart'),
                                       'col_cod': cn(mar, 'codice'),
                                       'col_des': cn(mar, 'descriz')})
        self.AddColumn(mar, 'descriz', 'Marca', col_width=140)
        
        self.AddColumn(frn, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableFornit,
                                       'col_id':  cn(pro, 'id_fornit'),
                                       'col_cod': cn(frn, 'codice'),
                                       'col_des': cn(frn, 'descriz')})
        self.AddColumn(frn, 'descriz', 'Fornitore', col_width=140)
        
        self.AddColumn(sts, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableStatArt,
                                       'col_id':  cn(pro, 'id_status'),
                                       'col_cod': cn(sts, 'codice'),
                                       'col_des': cn(sts, 'descriz')})
        self.AddColumn(sts, 'descriz', 'Status', col_width=140)
        
        self.AddColumn(gpr, 'codice',  'Cod.', col_width=40, is_editable=False, 
                       linktable_info={'class':   alib.LinkTableGruPrez,
                                       'col_id':  cn(pro, 'id_gruprez'),
                                       'col_cod': cn(gpr, 'codice'),
                                       'col_des': cn(gpr, 'descriz')})
        self.AddColumn(gpr, 'descriz', 'Gruppo Prezzi', col_width=140)
        
        self.AddColumn(tip, 'id', '#tip', col_width=1)
        self.AddColumn(cat, 'id', '#cat', col_width=1)
        self.AddColumn(gru, 'id', '#gru', col_width=1)
        self.AddColumn(mar, 'id', '#mar', col_width=1)
        self.AddColumn(sts, 'id', '#sts', col_width=1)
        self.AddColumn(frn, 'id', '#frn', col_width=1)
        self.AddColumn(gpr, 'id', '#gpr', col_width=1)
        
        self.CreateGrid()


class RiclassProdPanel(aw.Panel, aw.awu.LimitiFiltersMixin):
    
    def __init__(self, *args, **kwargs):
        
        aw.Panel.__init__(self, *args, **kwargs)
        wdr.RiclassProdFunc(self)
        
        cn = self.FindWindowByName
        
        aw.awu.LimitiFiltersMixin.__init__(self)
        
        self.dbpro = pro = dbm.Prodotti()
        pro.AddField('1.0', 'selected')
        pro.Reset()
        
        self.gridpro = RiclassProdGrid(cn('pangridpro'), self.dbpro)
        
        ALS = self.AddLimitiFiltersSequence
        ALS(pro, 'prod',   'codice')
        ALS(pro, 'prod',   'descriz')
        ALS(pro, 'status', 'id_status')
        ALS(pro, 'catart', 'id_catart')
        ALS(pro, 'gruart', 'id_gruart')
        ALS(pro, 'tipart', 'id_tipart')
        ALS(pro, 'fornit', 'id_fornit')
        ALS(pro, 'marart', 'id_marart')
        ALS(pro, 'gruprez', 'id_gruprez')
        
        cn = self.FindWindowByName
        
        for name, func in (('butupdate', self.OnUpdate),
                           ('butassign', self.OnAssign),):
            self.Bind(wx.EVT_BUTTON, func, cn(name))
    
    def OnUpdate(self, event):
        self.UpdateData()
        event.Skip()
    
    def OnAssign(self, event):
        
        pro = self.dbpro
        
        sc = pro._GetFieldIndex('selected', inline=True)
        nm = 0
        for n in xrange(pro.RowsCount()):
            if pro._info.rs[n][sc]:
                nm += 1
        if nm == 0:
            aw.awu.MsgDialog(self, "Selezionare almeno un prodotto da riclassificare", style=wx.ICON_INFORMATION)
            return False
        
        msg = "Confermi la riclassificazione di %d prodotti?" % nm
        if aw.awu.MsgDialog(self, msg, style=wx.ICON_QUESTION|wx.YES_NO|wx.NO_DEFAULT) != wx.ID_YES:
            return
        
        self.AssignNewValues()
        event.Skip()
    
    def TestLimits(self):
        do = False
        for _table, _alias, _column, _ctrl1, _ctrl2 in self.limseq:
            v1 = _ctrl1.GetValue()
            v2 = _ctrl2.GetValue()
            if v1 and v2:
                do = True
                break
        return do
    
    def LimitiFiltersApply(self, root=None):
        from awc.controls.linktable import LinkTable
        for table, alias, column, ctrl1, ctrl2 in self.limseq:
            if isinstance(ctrl1, LinkTable):
                if hasattr(ctrl1, 'filter_by_descriz'):
                    v1, v2 = ctrl1.GetValueDes(), ctrl2.GetValueDes()
                    field = 'descriz'
                else:
                    v1, v2 = ctrl1.GetValueCod(), ctrl2.GetValueCod()
                    field = 'codice'
            else:
                v1, v2 = ctrl1.GetValue(), ctrl2.GetValue()
                field = column
            if v1 or v2:
                if root is not None:
                    table = root
                if v1 == v2:
                    table.AddFilter("%s.%s=%%s" % (alias, field), v1)
                elif v1 and v2:
                    table.AddFilter("%s.%s>=%%s AND %s.%s<=%%s" % (alias, field, alias, field), v1, v2)
                elif v1:
                    table.AddFilter("%s.%s>=%%s" % (alias, field), v1)
                elif v2:
                    table.AddFilter("%s.%s<=%%s" % (alias, field), v2)
    
    def UpdateData(self):
        if not self.TestLimits():
            aw.awu.MsgDialog(self, "Limiti errati", style=wx.ICON_WARNING)
            return
        wx.BeginBusyCursor()
        try:
            pro = self.dbpro
            pro.ClearFilters()
            self.LimitiFiltersApply()
            pro.Retrieve()
            self.gridpro.ChangeData(self.dbpro.GetRecordset())
        finally:
            wx.EndBusyCursor()
    
    def AssignNewValues(self):
        
        cn = self.FindWindowByName
        
        new_tipart = cn('new_id_tipart').GetValue()
        new_catart = cn('new_id_catart').GetValue()
        new_gruart = cn('new_id_gruart').GetValue()
        new_marart = cn('new_id_marart').GetValue()
        new_status = cn('new_id_status').GetValue()
        new_fornit = cn('new_id_fornit').GetValue()
        new_gruprez = cn('new_id_gruprez').GetValue()
        
        if new_tipart is None\
       and new_catart is None\
       and new_gruart is None\
       and new_marart is None\
       and new_status is None\
       and new_fornit is None\
       and new_gruprez is None:
            aw.awu.MsgDialog(self, 'Impostare la nuova classificazione', style=wx.ICON_INFORMATION)
            return False
        
        pro = self.dbpro
        
        nmod = 0
        wx.BeginBusyCursor()
        try:
            for _ in pro:
                if not pro.selected:
                    continue
                if new_tipart is not None:
                    pro.id_tipart = new_tipart
                if new_catart is not None:
                    pro.id_catart = new_catart
                if new_gruart is not None:
                    pro.id_gruart = new_gruart
                if new_marart is not None:
                    pro.id_marart = new_marart
                if new_status is not None:
                    pro.id_status = new_status
                if new_fornit is not None:
                    pro.id_fornit = new_fornit
                if new_gruprez is not None:
                    pro.id_gruprez = new_gruprez
                nmod += 1
            pro.Save()
        finally:
            wx.EndBusyCursor()
        aw.awu.MsgDialog(self, "Sono stati riclassificati %d prodotti." % nmod, style=wx.ICON_INFORMATION)
        return True


class RiclassProdFrame(aw.Frame):
    
    def __init__(self, *args, **kwargs):
        if not 'title' in kwargs:
            kwargs['title'] = FRAME_TITLE
        aw.Frame.__init__(self, *args, **kwargs)
        self.panel = RiclassProdPanel(self)
        self.AddSizedPanel(self.panel)
