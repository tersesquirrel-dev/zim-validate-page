# Copyright 2025-2026 tersesquirrel-dev <tersesquirrel@gmail.com>
#


import logging
from pathlib import Path
from shutil import which
from subprocess import run, CalledProcessError
import sys

from zim.plugins import PluginClass
from zim.actions import action
from zim.errors import Error

from zim.gui.pageview import PageViewExtension
from zim.notebook import NotebookExtension


logger = logging.getLogger('zim.plugins.validate-page')
logger.setLevel(logging.DEBUG)


def find_validation_script(source_path):
	'''Search for validation.py in parent directories recursively'''
	current = source_path.parent

	while current != current.parent:
		validation_script = current / 'validation.py'
		if validation_script.exists():
			logger.debug(f'Found validation script at {validation_script}')
			return validation_script

		# stop if we're at the root of the wiki
		if any(current.glob('*.zim')):
			logger.debug(f'No validation script found up to wiki root at {current}')
			return None

		current = current.parent

	return None


class ValidatePagePlugin(PluginClass):

	plugin_info = {
		'name': _('Validate Page'), # T: plugin name
		'description': _('''\
This plugin allows creation of python scripts to validate pages.
'''), # T: plugin description
		'author': 'TerseSquirrel',
		'help': 'Plugins:Validate Page',
	}

class ValidatePagePageViewExtension(PageViewExtension):

	#def __init__(self, plugin, window):
	#	PageViewExtension.__init__(self, plugin, window)
	#	self.ui = window

	@action(_('_Validate Page')) # T: menu item
	def validate_page(self):
		'''Action called by the menu item or key binding,
		when on the page to validate.
		'''

		page = self.pageview.page
		source_file = str(page.source_file)

		logger.debug(f'Validating page: {source_file}')

		if source_file:
			source_path = Path(source_file)

			validation_script = find_validation_script(source_path)

			if validation_script:
				try:
					def find_python():
						return (
							which("py") or      # Windows launcher
							which("python3") or
							which("python")
						)

					python = find_python()
					if not python:
						logger.error("No Python interpreter found in system PATH.")
						raise Error("No Python interpreter found in system PATH.")

					self.pageview.save_page()

					logger.debug(f'Executing validation script: {validation_script}')
					logger.debug(f'With source file: {source_file}')
					logger.debug(f'Using Python executable: {python}')
					logger.debug(f'In working directory: {Path(validation_script).parent}')

					result = run([python, str(validation_script), source_file],
								  capture_output=True, text=True, check=True,
								  cwd=Path(validation_script).parent)
					self.pageview.reload_page()

					# Log execution details
					logger.debug(f'Return code: {result.returncode}')

					if result.stdout:
						logger.info(f'Script stdout: {result.stdout.strip()}')
					else:
						logger.debug('No stdout from script')

					if result.stderr:
						logger.error(f'Script stderr: {result.stderr.strip()}')
					else:
						logger.debug('No stderr from script')

				except CalledProcessError as e:
					logger.error("Validation script failed (%s)", validation_script)
					logger.error("Return code: %s", e.returncode)

					if e.stdout:
						logger.error("Stdout: %s", e.stdout.strip())
					if e.stderr:
						logger.error("Stderr: %s", e.stderr.strip())

				except Exception as e:
					logger.error(f'Error executing validation script {validation_script}: {e}')