# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('test')

import gtk
import logging
logger = logging.getLogger('test')

from test_lib import Window
from test.AboutTestDialog import AboutTestDialog
from test.PreferencesTestDialog import PreferencesTestDialog

# See test_lib.Window.py for more details about how this class works
class TestWindow(Window):
    __gtype_name__ = "TestWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(TestWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutTestDialog
        self.PreferencesDialog = PreferencesTestDialog

        # Code for other initialization actions should be added here.

