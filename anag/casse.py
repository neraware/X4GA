#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         anag/casse.py
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

import MySQLdb

from anag import pdcrel
from anag.pdcrel_wdr import *

from Env import Azienda
bt = Azienda.BaseTab


FRAME_TITLE = "Casse"


class CassePanel(pdcrel._PdcRelPanel):
    """
    Gestione della tabella casse.
    """
    def __init__(self, *args, **kwargs):
        
        self.pdctipo = "A"
        self.tabanag = Azienda.BaseTab.TABNAME_CASSE
        pdcrel._PdcRelPanel.__init__(self, *args, **kwargs)
        
        self.anag_db_columns = [ c for c in Azienda.BaseTab.tabelle\
                                 [bt.TABSETUP_TABLE_CASSE]\
                                 [bt.TABSETUP_TABLESTRUCTURE] ]
        
        self._Auto_AddKeys( { "pdctip_casse": True,
                              "bilmas_casse": True,
                              "bilcon_casse": True,
                              "bilcee_casse": bt.CONBILRCEE == 1, } )
        self.ReadAutomat()
        self._auto_pdctip = getattr(self, "_auto_pdctip_casse", None)
        self._auto_bilmas = getattr(self, "_auto_bilmas_casse", None)
        self._auto_bilcon = getattr(self, "_auto_bilcon_casse", None)
        self._auto_bilcee = getattr(self, "_auto_bilcee_casse", None)
        
        self.db_report = "Sottoconti Cassa"

    def InitAnagCard(self, parent):
        p = wx.Panel( parent, -1)
        CasseCardFunc( p, True )
        return p
    
    def GetLinkTableClass(self):
        import anag.lib as alib
        return alib.LinkTableCassa

    
# ------------------------------------------------------------------------------


class CasseFrame(pdcrel.ga._AnagFrame):
    """
    Frame Gestione tabella Casse.
    """
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        pdcrel.ga._AnagFrame.__init__(self, *args, **kwargs)
        self.LoadAnagPanel(CassePanel(self, -1))


# ------------------------------------------------------------------------------


class CasseDialog(pdcrel.ga._AnagDialog):
    """
    Dialog Gestione tabella Agenti.
    """
    def __init__(self, *args, **kwargs):
        if not kwargs.has_key('title') and len(args) < 3:
            kwargs['title'] = FRAME_TITLE
        pdcrel.ga._AnagDialog.__init__(self, *args, **kwargs)
        self.LoadAnagPanel(CassePanel(self, -1))
