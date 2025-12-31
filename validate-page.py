# Copyright 2025-2026 tersesquirrel-dev <tersesquirrel@gmail.com>
#


import logging

from zim.plugins import PluginClass
from zim.actions import action
from zim.errors import Error

from zim.gui.pageview import PageViewExtension


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

	ERROR_START = '\t!!! ERROR: '
	ERROR_END = ' !!!'

	def strip_errors(self, text):
		'''Strip error messages from text'''
		while True:
			start_index = text.find(self.ERROR_START)
			if start_index == -1:
				break
			end_index = text.find(self.ERROR_END, start_index)
			if end_index == -1:
				break
			text = text[:start_index] + text[end_index + len(self.ERROR_END):]
		
		return text

	def validate_page(self, text):
		'''Validate a page of text'''
		text = text.replace('red', 'red\t!!! ERROR: should be number !!!')

		return text

class ValidatePagePageViewExtension(PageViewExtension):

	@action(_('_Validate Page')) # T: menu item
	def validate_page(self):
		'''Action called by the menu item or key binding,
		when on the page to validate.
		'''
		pageview = self.pageview
		textview = pageview.textview
		buffer = textview.get_buffer()
		start, end = buffer.get_bounds()
		text = start.get_text(end)

		# TODO: Preserve formatting for text
		# TODO: Stip old errors before adding new ones
		
		text = self.plugin.strip_errors(text)
		text = self.plugin.validate_page(text)

		with buffer.user_action:
			buffer.set_text(text)
