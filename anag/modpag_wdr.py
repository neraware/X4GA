# -*- coding: UTF-8 -*-

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: modpag.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxPython modules
import wx
import wx.grid
import wx.animate

# Custom source
from anag.basetab import AnagCardPanel
from anag.lib import LinkTableCassaBanca, LinkTableCauContab

from awc.controls.radiobox import RadioBox
from awc.controls.checkbox import CheckBox
from awc.controls.numctrl import NumCtrl

from anag.basetab import WorkZoneNotebook

import Env
bt = Env.Azienda.BaseTab


class FatturaPaTipoPagamentoRadioBox(RadioBox):

    def __init__(self, *args, **kwargs):
        RadioBox.__init__(self, *args, **kwargs)
        self.SetDataLink(values=["-", "TP01", "TP02", "TP03"])


class FatturaPaModoPagamentoRadioBox(RadioBox):

    def __init__(self, *args, **kwargs):
        RadioBox.__init__(self, *args, **kwargs)
        self.SetDataLink(values=["-", "MP01", "MP02", "MP03", "MP04", "MP05", "MP06", "MP07", "MP08", "MP09", "MP10", "MP11", "MP12", "MP13", "MP14", "MP15", "MP16", "MP17", "MP18", "MP19", "MP20", "MP21"])



# Window functions

ID_ANAGMAIN = 16000
ID_WORKZONE = 16001

def ModPagCardFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = AnagCardPanel(parent)
    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item3 = WorkZoneNotebook( parent, ID_WORKZONE, wx.DefaultPosition, [200,160], 0 )
    item2 = item3
    
    item4 = wx.Panel( item3, -1 )
    ModPagCardDatiFunc(item4, False)
    item3.AddPage( item4, "Dati" )

    item5 = wx.Panel( item3, -1 )
    ModPagCardFatturaPaFunc(item5, False)
    item3.AddPage( item5, "Fattura PA" )

    item0.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item0.AddGrowableCol( 0 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

ID_LBL_SEARCHRESULTS = 16002
ID_FILT_RIBA = 16003

def ModPagSpecSearchFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.StaticText( parent, ID_LBL_SEARCHRESULTS, "Mostra solo le mod.pagamento di tipo:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTRE )
    item1.SetForegroundColour( wx.BLACK )
    item1.SetBackgroundColour( wx.GREEN )
    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item2 = wx.RadioBox( parent, ID_FILT_RIBA, "Tipologia", wx.DefaultPosition, wx.DefaultSize, 
        ["Ri.Ba.","Non Ri.Ba."] , 1, wx.RA_SPECIFY_ROWS )
    item0.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item0.AddGrowableCol( 0 )

    item0.AddGrowableRow( 5 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

ID_TIPOMP = 16004
ID_CONGAR = 16005
ID_CONTRASS = 16006
ID_ASKBANCA = 16007
ID_ASKSPESE = 16008
ID_TEXT = 16009
ID_NUMSCAD = 16010
ID_FINEMESE0 = 16011
ID_FINEMESE = 16012
ID_MODOCALC = 16013
ID_PERIODI = 16014
ID_TXT_NUMSCAD = 16015
ID_TXT_GGEXTRA = 16016
ID_GEM01 = 16017
ID_GEM02 = 16018
ID_GEM03 = 16019
ID_GEM04 = 16020
ID_GEM05 = 16021
ID_GEM06 = 16022
D_GEM07 = 16023
ID_GEM08 = 16024
ID_GEM09 = 16025
ID_GEM10 = 16026
ID_GEM11 = 16027
ID_GEM12 = 16028
ID_PDCPI = 16029
ID_CAUPI = 16030
ID_GG01 = 16031
ID_GG02 = 16032
ID_GG03 = 16033
ID_GG04 = 16034
ID_GG05 = 16035
ID_GG06 = 16036
ID_GG07 = 16037
ID_GG08 = 16038
ID_GG09 = 16039
ID_GG10 = 16040
ID_GG11 = 16041
ID_GG12 = 16042
ID_GG13 = 16043
ID_GG14 = 16044
ID_GG15 = 16045
ID_GG16 = 16046
ID_GG17 = 16047
ID_GG18 = 16048
ID_GG19 = 16049
ID_GG20 = 16050
ID_GG21 = 16051
ID_GG22 = 16052
ID_GG23 = 16053
ID_GG24 = 16054
ID_GG25 = 16055
ID_GG26 = 16056
ID_GG27 = 16057
ID_GG28 = 16058
ID_GG29 = 16059
ID_GG30 = 16060
ID_GG31 = 16061
ID_GG32 = 16062
ID_GG33 = 16063
ID_GG34 = 16064
ID_GG35 = 16065
ID_GG36 = 16066
ID_SC1NOEFF = 16067
ID_SC1IVA = 16068
ID_PERCSC1 = 16069

def ModPagCardDatiFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item2 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item3 = RadioBox( parent, ID_TIPOMP, "Tipologia", wx.DefaultPosition, wx.DefaultSize, 
        ["Contanti/Assegni","Bonifico","Ricevuta Bancaria","RID","Cambiale","Altro"] , 1, wx.RA_SPECIFY_COLS )
    item2.Add( item3, 0, wx.GROW|wx.LEFT|wx.TOP, 5 )

    item4 = RadioBox( parent, ID_CONGAR, "Con garanzia:", wx.DefaultPosition, wx.DefaultSize, 
        ["Si","No"] , 1, wx.RA_SPECIFY_ROWS )
    item4.SetName( "congar" )
    item2.Add( item4, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item6 = wx.StaticBox( parent, -1, "" )
    item5 = wx.StaticBoxSizer( item6, wx.VERTICAL )
    
    item7 = CheckBox( parent, ID_CONTRASS, "Contrassegno", wx.DefaultPosition, wx.DefaultSize, 0 )
    item7.SetName( "contrass" )
    item5.Add( item7, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item8 = CheckBox( parent, ID_ASKBANCA, "Richiedi banca", wx.DefaultPosition, wx.DefaultSize, 0 )
    item8.SetName( "askbanca" )
    item5.Add( item8, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item9 = CheckBox( parent, ID_ASKSPESE, "Richiedi spese", wx.DefaultPosition, wx.DefaultSize, 0 )
    item9.SetName( "askspese" )
    item5.Add( item9, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item2.Add( item5, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item2.AddGrowableCol( 0 )

    item2.AddGrowableRow( 1 )

    item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item10 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item12 = wx.StaticBox( parent, -1, "Partite" )
    item11 = wx.StaticBoxSizer( item12, wx.HORIZONTAL )
    
    item13 = wx.StaticText( parent, ID_TEXT, "Numero di scadenze:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item11.Add( item13, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item14 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item14.SetName("numscad")
    item11.Add( item14, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    item11.Add( [ 20, 20 ] , 0, wx.ALIGN_CENTER, 5 )

    item15 = CheckBox( parent, ID_FINEMESE0, "Vai a fine mese e calcola", wx.DefaultPosition, wx.DefaultSize, 0 )
    item15.SetName( "finemese0" )
    item11.Add( item15, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item16 = CheckBox( parent, ID_FINEMESE, "Porta ogni scadenza a fine mese", wx.DefaultPosition, wx.DefaultSize, 0 )
    item16.SetName( "finemese" )
    item11.Add( item16, 0, wx.ALIGN_CENTER|wx.LEFT, 5 )

    item10.Add( item11, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item17 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item18 = RadioBox( parent, ID_MODOCALC, "Tipo di calcolo", wx.DefaultPosition, wx.DefaultSize, 
        ["Sintetico","Dettagliato","Nessuno: pag.imm."] , 1, wx.RA_SPECIFY_COLS )
    item17.Add( item18, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.BOTTOM, 5 )

    item19 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item20 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item21 = RadioBox( parent, ID_PERIODI, "Periodi:", wx.DefaultPosition, wx.DefaultSize, 
        ["Mesi","Giorni"] , 1, wx.RA_SPECIFY_COLS )
    item20.Add( item21, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item23 = wx.StaticBox( parent, -1, "Calcolo sintetico" )
    item22 = wx.StaticBoxSizer( item23, wx.VERTICAL )
    
    item24 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item25 = wx.StaticText( parent, ID_TEXT, "Periodi a prima scadenza:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
    item24.Add( item25, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item26 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item26.SetName("mesi1")
    item24.Add( item26, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item27 = wx.StaticText( parent, ID_TEXT, "Periodi tra scadenze:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
    item24.Add( item27, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item28 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item28.SetName("mesitra")
    item24.Add( item28, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item22.Add( item24, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item20.Add( item22, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item20.AddGrowableCol( 1 )

    item19.Add( item20, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item30 = wx.StaticBox( parent, -1, "Slittamento scadenze" )
    item29 = wx.StaticBoxSizer( item30, wx.VERTICAL )
    
    item31 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item32 = wx.StaticText( parent, ID_TEXT, "Giorni extra per ogni scadenza:", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
    item31.Add( item32, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item33 = NumCtrl(parent, ID_TXT_GGEXTRA, integerWidth=2, allowNegative=False, groupDigits=False); item33.SetName("ggextra")
    item31.Add( item33, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )

    item34 = wx.StaticText( parent, ID_TEXT, "Giorni extra in base al mese:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item31.Add( item34, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP|wx.BOTTOM, 5 )

    item31.AddGrowableCol( 2 )

    item29.Add( item31, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT, 5 )

    item35 = wx.FlexGridSizer( 2, 0, 0, 0 )
    
    item36 = wx.StaticText( parent, ID_TEXT, "1", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item36, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item37 = wx.StaticText( parent, ID_TEXT, "2", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item37, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item38 = wx.StaticText( parent, ID_TEXT, "3", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item38, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item39 = wx.StaticText( parent, ID_TEXT, "4", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item39, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item40 = wx.StaticText( parent, ID_TEXT, "5", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item40, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item41 = wx.StaticText( parent, ID_TEXT, "6", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item41, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item42 = wx.StaticText( parent, ID_TEXT, "7", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item42, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item43 = wx.StaticText( parent, ID_TEXT, "8", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item43, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item44 = wx.StaticText( parent, ID_TEXT, "9", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item44, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item45 = wx.StaticText( parent, ID_TEXT, "10", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item45, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item46 = wx.StaticText( parent, ID_TEXT, "11", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item46, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item47 = wx.StaticText( parent, ID_TEXT, "12", wx.DefaultPosition, wx.DefaultSize, 0 )
    item35.Add( item47, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item48 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item48.SetName("gem01")
    item35.Add( item48, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item49 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item49.SetName("gem02")
    item35.Add( item49, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item50 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item50.SetName("gem03")
    item35.Add( item50, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item51 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item51.SetName("gem04")
    item35.Add( item51, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item52 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item52.SetName("gem05")
    item35.Add( item52, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item53 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item53.SetName("gem06")
    item35.Add( item53, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item54 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item54.SetName("gem07")
    item35.Add( item54, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item55 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item55.SetName("gem08")
    item35.Add( item55, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item56 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item56.SetName("gem09")
    item35.Add( item56, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item57 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item57.SetName("gem10")
    item35.Add( item57, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item58 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item58.SetName("gem11")
    item35.Add( item58, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item59 = NumCtrl( parent, integerWidth=2, allowNegative=False, groupDigits=False); item59.SetName("gem12")
    item35.Add( item59, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item29.Add( item35, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 5 )

    item19.Add( item29, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item19.AddGrowableCol( 0 )

    item17.Add( item19, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item17.AddGrowableCol( 0 )

    item17.AddGrowableCol( 1 )

    item17.AddGrowableCol( 2 )

    item10.Add( item17, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item61 = wx.StaticBox( parent, -1, "Incasso/Pagamento immediato" )
    item60 = wx.StaticBoxSizer( item61, wx.VERTICAL )
    
    item62 = wx.FlexGridSizer( 0, 2, 0, 0 )
    
    item63 = wx.StaticText( parent, ID_TEXT, "Cassa/Banca:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item62.Add( item63, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item64 = LinkTableCassaBanca(parent, ID_PDCPI ); item64.SetDataLink( bt.TABNAME_PDC, "id_pdcpi", None); item64.SetObligatory(True)
    item62.Add( item64, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item65 = wx.StaticText( parent, ID_TEXT, "Causale:", wx.DefaultPosition, wx.DefaultSize, 0 )
    item62.Add( item65, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item66 = LinkTableCauContab(parent, ID_CAUPI ); item66.SetDataLink('cfgcontab', "id_caupi", None)
    item62.Add( item66, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item62.AddGrowableCol( 1 )

    item60.Add( item62, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item10.Add( item60, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item10.AddGrowableCol( 0 )

    item1.Add( item10, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item1.AddGrowableCol( 0 )

    item1.AddGrowableCol( 1 )

    item0.Add( item1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item67 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item69 = wx.StaticBox( parent, -1, "Calcolo dettagliato" )
    item68 = wx.StaticBoxSizer( item69, wx.VERTICAL )
    
    item70 = wx.FlexGridSizer( 0, 12, 0, 0 )
    
    item71 = wx.StaticText( parent, ID_TEXT, "1", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item71, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item72 = wx.StaticText( parent, ID_TEXT, "2", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item72, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item73 = wx.StaticText( parent, ID_TEXT, "3", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item73, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item74 = wx.StaticText( parent, ID_TEXT, "4", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item74, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item75 = wx.StaticText( parent, ID_TEXT, "5", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item75, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item76 = wx.StaticText( parent, ID_TEXT, "6", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item76, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item77 = wx.StaticText( parent, ID_TEXT, "7", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item77, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item78 = wx.StaticText( parent, ID_TEXT, "8", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item78, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item79 = wx.StaticText( parent, ID_TEXT, "9", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item79, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item80 = wx.StaticText( parent, ID_TEXT, "10", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item80, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item81 = wx.StaticText( parent, ID_TEXT, "11", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item81, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item82 = wx.StaticText( parent, ID_TEXT, "12", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item82, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item83 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item83.SetName("gg01")
    item70.Add( item83, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item84 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item84.SetName("gg02")
    item70.Add( item84, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item85 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item85.SetName("gg03")
    item70.Add( item85, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item86 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item86.SetName("gg04")
    item70.Add( item86, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item87 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item87.SetName("gg05")
    item70.Add( item87, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item88 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item88.SetName("gg06")
    item70.Add( item88, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item89 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item89.SetName("gg07")
    item70.Add( item89, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item90 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item90.SetName("gg08")
    item70.Add( item90, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item91 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item91.SetName("gg09")
    item70.Add( item91, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item92 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item92.SetName("gg10")
    item70.Add( item92, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item93 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item93.SetName("gg11")
    item70.Add( item93, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item94 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item94.SetName("gg12")
    item70.Add( item94, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item95 = wx.StaticText( parent, ID_TEXT, "13", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item95, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item96 = wx.StaticText( parent, ID_TEXT, "14", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item96, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item97 = wx.StaticText( parent, ID_TEXT, "15", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item97, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item98 = wx.StaticText( parent, ID_TEXT, "16", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item98, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item99 = wx.StaticText( parent, ID_TEXT, "17", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item99, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item100 = wx.StaticText( parent, ID_TEXT, "18", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item100, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item101 = wx.StaticText( parent, ID_TEXT, "19", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item101, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item102 = wx.StaticText( parent, ID_TEXT, "20", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item102, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item103 = wx.StaticText( parent, ID_TEXT, "21", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item103, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item104 = wx.StaticText( parent, ID_TEXT, "22", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item104, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item105 = wx.StaticText( parent, ID_TEXT, "23", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item105, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item106 = wx.StaticText( parent, ID_TEXT, "24", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item106, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item107 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item107.SetName("gg13")
    item70.Add( item107, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item108 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item108.SetName("gg14")
    item70.Add( item108, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item109 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item109.SetName("gg15")
    item70.Add( item109, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item110 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item110.SetName("gg16")
    item70.Add( item110, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item111 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item111.SetName("gg17")
    item70.Add( item111, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item112 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item112.SetName("gg18")
    item70.Add( item112, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item113 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item113.SetName("gg19")
    item70.Add( item113, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item114 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item114.SetName("gg20")
    item70.Add( item114, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item115 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item115.SetName("gg21")
    item70.Add( item115, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item116 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item116.SetName("gg22")
    item70.Add( item116, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item117 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item117.SetName("gg23")
    item70.Add( item117, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item118 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item118.SetName("gg24")
    item70.Add( item118, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item119 = wx.StaticText( parent, ID_TEXT, "25", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item119, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item120 = wx.StaticText( parent, ID_TEXT, "26", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item120, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item121 = wx.StaticText( parent, ID_TEXT, "27", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item121, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item122 = wx.StaticText( parent, ID_TEXT, "28", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item122, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item123 = wx.StaticText( parent, ID_TEXT, "29", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item123, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item124 = wx.StaticText( parent, ID_TEXT, "30", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item124, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item125 = wx.StaticText( parent, ID_TEXT, "31", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item125, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item126 = wx.StaticText( parent, ID_TEXT, "32", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item126, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item127 = wx.StaticText( parent, ID_TEXT, "33", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item127, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item128 = wx.StaticText( parent, ID_TEXT, "34", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item128, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item129 = wx.StaticText( parent, ID_TEXT, "35", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item129, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item130 = wx.StaticText( parent, ID_TEXT, "36", wx.DefaultPosition, wx.DefaultSize, 0 )
    item70.Add( item130, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item131 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item131.SetName("gg25")
    item70.Add( item131, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item132 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item132.SetName("gg26")
    item70.Add( item132, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item133 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item133.SetName("gg27")
    item70.Add( item133, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item134 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item134.SetName("gg28")
    item70.Add( item134, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item135 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item135.SetName("gg29")
    item70.Add( item135, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item136 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item136.SetName("gg30")
    item70.Add( item136, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item137 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item137.SetName("gg31")
    item70.Add( item137, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item138 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item138.SetName("gg32")
    item70.Add( item138, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item139 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item139.SetName("gg33")
    item70.Add( item139, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item140 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item140.SetName("gg34")
    item70.Add( item140, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item141 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item141.SetName("gg35")
    item70.Add( item141, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item142 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item142.SetName("gg36")
    item70.Add( item142, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT, 5 )

    item68.Add( item70, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item67.Add( item68, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.BOTTOM, 5 )

    item144 = wx.StaticBox( parent, -1, "Opzioni prima scadenza" )
    item143 = wx.StaticBoxSizer( item144, wx.VERTICAL )
    
    item145 = CheckBox( parent, ID_SC1NOEFF, "Escludi effetto", wx.DefaultPosition, wx.DefaultSize, 0 )
    item145.SetName( "sc1noeff" )
    item143.Add( item145, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item146 = CheckBox( parent, ID_SC1IVA, "Importo pari a tot.IVA", wx.DefaultPosition, wx.DefaultSize, 0 )
    item146.SetName( "sc1iva" )
    item143.Add( item146, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item147 = wx.FlexGridSizer( 1, 0, 0, 0 )
    
    item148 = wx.StaticText( parent, ID_TEXT, "Importo pari al", wx.DefaultPosition, wx.DefaultSize, 0 )
    item147.Add( item148, 0, wx.ALIGN_CENTER|wx.LEFT|wx.TOP, 5 )

    item149 = NumCtrl( parent, integerWidth=3, allowNegative=False, groupDigits=False); item149.SetName("sc1perc")
    item147.Add( item149, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 5 )

    item143.Add( item147, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

    item150 = wx.StaticText( parent, ID_TEXT, "% del totale documento", wx.DefaultPosition, wx.DefaultSize, 0 )
    item143.Add( item150, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT, 5 )

    item67.Add( item143, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.BOTTOM, 5 )

    item67.AddGrowableCol( 1 )

    item67.AddGrowableRow( 0 )

    item0.Add( item67, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL, 5 )

    item0.AddGrowableCol( 0 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

ID_TIPORATE = 16070
ID_MODPAG = 16071

def ModPagCardFatturaPaFunc( parent, call_fit = True, set_sizer = True ):
    item0 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item1 = wx.FlexGridSizer( 0, 1, 0, 0 )
    
    item2 = FatturaPaTipoPagamentoRadioBox( parent, ID_TIPORATE, "Tipologia:", wx.DefaultPosition, wx.DefaultSize, 
        ["N/C - Non classificato","TP01 - Pagamento a rate","TP02 - Pagamento completo","TP03 - Anticipo"] , 1, wx.RA_SPECIFY_ROWS )
    item2.SetName( "ftel_tippag" )
    item1.Add( item2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.RIGHT|wx.TOP, 5 )

    item3 = FatturaPaModoPagamentoRadioBox( parent, ID_MODPAG, "Tipologia:", wx.DefaultPosition, wx.DefaultSize, 
        ["N/C - Non classificato","MP01 - Contanti","MP02 - Assegno","MP03 - Assegno circolare","MP04 - Contanti presso Tesoreria","MP05 - Bonifico","MP06 - Vaglia cambiario","MP07 - Bollettino bancario","MP08 - Carta di pagamento","MP09 - RID","MP10 - RID utenze","MP11 - RID veloce","MP12 - RIBA","MP13 - MAV","MP14 - Quietanza erario","MP15 - Giroconto su conti di contabilità speciale","MP16 - Domiciliazione bancaria","MP17 - Domiciliazione postale","MP18 - Bollettino di c/c postale","MP19 - SEPA Direct Debit","MP20 - SEPA Direct Debit CORE","MP21 - SEPA Direct Debit B2B","MP22 - Trattenuta su somme gia' riscosse","MP23 - PagoPA"] , 2, wx.RA_SPECIFY_COLS )
    item3.SetName( "ftel_modpag" )
    item1.Add( item3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    item1.AddGrowableCol( 0 )

    item0.Add( item1, 0, 0, 5 )

    if set_sizer == True:
        parent.SetSizer( item0 )
        if call_fit == True:
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

# Toolbar functions

# Bitmap functions


# End of generated file
