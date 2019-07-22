import os

from justupdate.core.base import JustUpdateConstants, get_platform_name_short
from justupdate.core.config import Config

def prepare_template(version):
	config = Config()
	config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
	if get_platform_name_short() == "win":
		return _prepare_template_win(version, config)
	if get_platform_name_short() == "mac":
		return _prepare_template_mac()

def _prepare_template_win(version, config):
	f = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "win", "template.nsi"))
	data = f.read()
	f.close()
	data = data.replace("%JustUpdateRepository%", JustUpdateConstants.REPO_FOLDER)
	data = data.replace("%APP_NAME%", config.get("app_name"))
	data = data.replace("%APP_AUTHOR%", config.get("app_author"))
	data = data.replace("%VERSION%", version.to_nsis_compliant())
	data = data.replace("%PRETTY_VERSION%", version.to_string())
	return data

def _prepare_template_mac():
	pass

