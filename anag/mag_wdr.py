# -*- coding: UTF-8 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: mag.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid
import wx.animate

# Custom source
from anag.basetab import AnagCardPanel

from awc.controls.linktable import LinkTable
from anag.pdc import PdcDialog

import anag.lib as alib

from Env import Azienda
bt = Azienda.BaseTab



# Window functions

ID_ANAGMAIN = 16000
ID_TEXT = 16001
ID_PDC = 16002
ID_PDCACQ = 16003
ID_PDCVEN = 16004
ID_PANGRIDRIM = 16005

def MagazzCardFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = AnagCardPanel(parent)
    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item2 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item3 = wx.StaticText( parent, ID_TEXT, "Anagrafica associata:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item2.Add( item3, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item4 = LinkTable(parent, ID_PDC ); item4.SetDataLink( bt.TABNAME_PDC, "id_pdc", PdcDialog ); item4.SetObligatory(True)
    item2.Add( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item5 = wx.StaticText( parent, ID_TEXT, "Conto di costo per acquisti:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item2.Add( item5, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item6 = alib.LinkTablePdcCosti(parent, ID_PDCACQ, 'id_pdcacq')
    item2.Add( item6, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item7 = wx.StaticText( parent, ID_TEXT, "Conto di ricavo per vendite:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item2.Add( item7, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item8 = alib.LinkTablePdcRicavi(parent, ID_PDCVEN, 'id_pdcven')
    item2.Add( item8, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item2.AddGrowableCol( 1 )

    item0.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item9 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item10 = wx.StaticText( parent, ID_TEXT, "Attenzione: i conti di costo/ricavo hanno la precedenza su qualsiasi altro automatismo", wx.DefaultPosition, wx.DefaultSize, 0 )
    item9.Add( item10, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item11 = wx.StaticText( parent, ID_TEXT, "Configurazione Registri Iva per causale con indirizzamento dinamico del registro", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.SetForegroundColour( wx.BLUE )
    item9.Add( item11, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item12 = wx.Panel( parent, ID_PANGRIDRIM, wx.DefaultPosition, [200,160], 0 )
    item9.Add( item12, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item9.AddGrowableCol( 0 )

    item9.AddGrowableRow( 2 )

    item0.Add( item9, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 2 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

# Toolbar functions

# Bitmap functions


# End of generated file
