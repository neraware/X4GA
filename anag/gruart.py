#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         anag/gruart.py
# Author:       Fabio Cassini <fabio.cassini@gmail.com>
# Copyright:    (C) 2011 Astra S.r.l. C.so Cavallotti, 122 18038 Sanremo (IM)
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

import awc.layout.gestanag as ga
import anag.gruart_wdr as wdr

from awc.controls.linktable import EVT_LINKTABCHANGED

from Env import Azienda
bt = Azienda.BaseTab


import stormdb as adb
import report as rpt

import wx.grid as gl
import awc.controls.dbgrid as dbglib


FRAME_TITLE = "Gruppi merce"


class GruArtSearchResultsGrid(ga.SearchResultsGrid):
    
    def GetDbColumns(self):
        _NUM = gl.GRID_VALUE_NUMBER
        _STR = gl.GRID_VALUE_STRING
        _DAT = gl.GRID_VALUE_DATETIME
        cn = lambda x: self.db._GetFieldIndex(x)
        tab = self.tabalias
        return (( 35, (cn('catart_codice'),  "Cod.",      _STR, True)),
                (240, (cn('catart_descriz'), "Categoria", _STR, True)),
                ( 35, (cn('gruart_codice'),  "Cod.",      _STR, True)),
                (240, (cn('gruart_descriz'), "Gruppo",    _STR, True)),
                (  1, (cn('catart_id'),      "#cat",      _STR, True)),
                (  1, (cn('gruart_id'),      "#gru",      _STR, True)),
            )
    
    def SetColumn2Fit(self):
        self.SetFitColumn(3)


# ------------------------------------------------------------------------------


class GruArtPanel(ga.AnagPanel):
    """
    Gestione tabella Gruppi merce.
    """
    def __init__(self, *args, **kwargs):
        ga.AnagPanel.__init__(self, *args, **kwargs)
        self.SetDbSetup( Azienda.BaseTab.tabelle[
                         Azienda.BaseTab.TABSETUP_TABLE_GRUART ] )
        self.SetDbOrderColumns((
            #ordinamento bilancio: sezione,cod.mastro,cod.conto,sottoconto
            #sottoconto x descrizione se cli/for, altrimenti codice
            ("Inventario", ('catart.codice',
                            'gruart.codice')),
            ("Codice",      ('gruart.codice',)),
            ("Descrizione", ('gruart.descriz',)),
        ))
        
        self._sqlrelcol = ", catart.id, catart.codice, catart.descriz"
        self._sqlrelfrm =\
            " INNER JOIN %s AS catart ON %s.id_catart=catart.id"\
            % ( bt.TABNAME_CATART, bt.TABNAME_GRUART )
        self.db_tabprefix = "%s." % bt.TABNAME_GRUART
        
        self._valfilters['catart'] = ['catart.codice', None, None]
        self._hasfilters = True
        
        self.db_report = "Gruppi merce"

    def InitAnagCard(self, parent):
        p = wx.Panel( parent, -1)
        wdr.GruArtCardFunc( p, True )
        return p

    def GetSearchResultsGrid(self, parent):
        grid = GruArtSearchResultsGrid(parent, ga.ID_SEARCHGRID, 
                                       self.db_tabname, self.GetSqlColumns())
        return grid
    
    def GetDbPrint(self):
        db = adb.DbTable(self.db_tabname, writable=False)
        db.AddOrder("catart.codice")
        return db

    def GetSpecializedSearchPanel(self, parent):
        p = wx.Panel(parent, -1)
        wdr.GruArtSpecSearchFunc(p)
        return p


# ------------------------------------------------------------------------------


class GruArtFrame(ga._AnagFrame):
    """
    Frame Gestione tabella Gruppi merce.
    """
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        ga._AnagFrame.__init__(self, *args, **kwargs)
        self.LoadAnagPanel(GruArtPanel(self, -1))


# ------------------------------------------------------------------------------


class GruArtDialog(ga._AnagDialog):
    """
    Dialog Gestione tabella Gruppi merce.
    """
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        ga._AnagDialog.__init__(self, *args, **kwargs)
        self.LoadAnagPanel(GruArtPanel(self, -1))
