# Copyright 2025-2026 tersesquirrel-dev <tersesquirrel@gmail.com>
#


import logging
from pathlib import Path
from subprocess import run
import sys

from zim.plugins import PluginClass
from zim.actions import action
from zim.errors import Error

from zim.gui.pageview import PageViewExtension
from zim.notebook import NotebookExtension


logger = logging.getLogger('zim.plugins.validate-page')


class ValidatePagePlugin(PluginClass):

	plugin_info = {
		'name': _('Validate Page'), # T: plugin name
		'description': _('''\
This plugin allows creation of python scripts to validate pages.
'''), # T: plugin description
		'author': 'TerseSquirrel',
		'help': 'Plugins:Validate Page',
	}

	def validate_page(self, source_file):
		'''Validate a page of text'''
		
		if source_file:
			validation_script = Path(source_file).with_name('validation.py')

			if validation_script.exists():
				run([sys.executable, str(validation_script), source_file], check=True)
					
class ValidatePagePageViewExtension(PageViewExtension):

	@action(_('_Validate Page')) # T: menu item
	def validate_page(self):
		'''Action called by the menu item or key binding,
		when on the page to validate.
		'''

		source_file = str(self.pageview.page.source_file)

		self.plugin.validate_page(source_file)
