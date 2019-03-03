#!/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Name:         ftel/__init__.py
# Copyright:    (C) 2018 Evolvia S.r.l. <info@evolvia.srl>
# ------------------------------------------------------------------------------


xsl_filename = 'fatturapa_v1.2.xsl'

def get_xsl_stream():
    from ftel.vendite.fatturapa_v12_xsl import xsl
    return xsl
