#!/usr/bin/python2
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         X.py
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

import sys, os

import glob

import stormdb as adb
adb.db.setlog(False)

import xpaths
config_base_path = xpaths.GetConfigPath()

if hasattr(sys, 'frozen'):
    
    a = 'setdefaultencoding'
    if hasattr(sys, a):
        getattr(sys, a)("utf-8")
    
    try:
        os.chdir(os.path.split(sys.argv[0])[0])
    except:
        pass
    
    sp = []
    
    pp = os.getenv('X4_PYTHONPATH')
    if pp:
        for p in pp.split(';'):
            sp.append(p)

    for _file in glob.glob(os.path.join(config_base_path, 'cust/*.zip')):
        sp.append(_file.replace('/', '\\'))
    
    for _file in glob.glob(os.path.join(config_base_path, 'plugin/*.zip')):
        sp.append(_file.replace('/', '\\'))
    
    for _file in glob.glob(os.path.join(config_base_path, 'addon/*.zip')):
        sp.append(_file.replace('/', '\\'))
    
    for n in range(len(sp)-1, -1, -1):
        sys.path.insert(0, sp[n])


stdmod = 10
modmod = 0

import wx
import awc.wxinit  # @UnusedImport

import xsplash

import impex  # @UnusedImport

import awc.controls.windows as aw
import awc.util as awu

dummy_app = wx.PySimpleApp()
dummy_app.splash = xsplash.XSplashScreen(stdmod)
dummy_app.splash.SetJob("Inizializzazione in corso...")
dummy_app.splash.Show()

from plib import test_ext_req, get_reqfail_msg, load_plugin, PluginException

try:
    #aggancio personalizzazione
    dummy_app.splash.SetJob("Caricamento personalizzazione...")
    import custapp
    import custver
    if hasattr(custver, '__min_compat_mod__'):
        import version
        version.__min_compat_mod__ = custver.__min_compat_mod__
    if not test_ext_req(custver):
        cap = "Questa versione di X4GA è obsoleta per %s!" % custapp.name
        msg = get_reqfail_msg("C", custapp.name, custver)
        aw.awu.MsgDialog(None, msg, cap, style=wx.ICON_ERROR)
except ImportError, e:
    if not 'custapp' in repr(e.args):
        awu.MsgDialog(None, "Errore di importazione modulo in caricamento personalizzazione:\n%s" % repr(e.args))
except Exception, e:
    awu.MsgDialog(None, "Errore in caricamento personalizzazione:\n%s" % repr(e.args))

import xapp

dummy_app.Destroy()

import Env

app = xapp.XApp(redirect=bool(not getattr(sys, 'frozen', True)) 
                               or Env.Azienda.params['redirect-output'])
app.splash = dummy_app.splash

adb.dbtable.DbInfo.GetEnv = classmethod(lambda *x: Env)

Env.SetConfigBasePath()

if not Env.InitSettings():
    if app.splash:
        app.splash.Destroy()
    awu.MsgDialog(None, "Problema di configurazione di X4GA, impossibile proseguire.", style=wx.ICON_ERROR)
    os.sys.exit(1)



if Env.Azienda.params['show-syspath']:
    wx.MessageBox('\n'.join(sys.path), 'sys.path')


def Main():
    
    try:
        import custrun  # @UnusedImport
    except ImportError:
        pass
    
    if hasattr(sys, 'frozen'):
        import erman
        def _exceptionhook(_type, err, traceback):
            erman.ErrorWarning(err, traceback)
        sys.excepthook = _exceptionhook
    
    import images
    icon = wx.EmptyIcon()
    prg = sys.argv[0]
    custicon = os.path.join(os.path.split(prg)[0], 'customized_icon.png')
    bmp = None
    if os.path.isfile(custicon):
        try:
            bmp = wx.Bitmap(custicon)
        except:
            pass
    if bmp is None:
        bmp = images.getIconBitmap()
    icon.CopyFromBitmap(bmp)
    aw.SetStandardIcon(icon)
    
    app.StartApp()
    app.MainLoop()
    
    prg = Env.Azienda.params['onexit-execute']
    if prg:
        db = Env.adb.db.__database__
        if db:
            try:
                prg = prg.replace('[sql_username]', db.username)
                prg = prg.replace('[sql_password]', db.password)
            except:
                pass
        parts = prg.split()
        prg = parts[0]
        try:
            if len(parts) == 1:
                os.execl(prg)
            else:
                os.execl(prg, *parts)
        except:
            pass
        
    os._exit(0)


# ------------------------------------------------------------------------------



def run():
    try:
        c, _ = os.path.split(__file__)
        os.chdir(c)
    except:
        pass
    Main()


if __name__ == '__main__':
    run()
