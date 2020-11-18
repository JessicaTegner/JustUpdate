import os
import stat
import sys

from justupdate.core.base import get_platform_name_short
from justupdate.core.base import JustUpdateConstants
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor
from justupdate.core.executor import CommandType

def prepare_template(version):
	config = Config()
	config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
	cmd = getattr(sys.modules[__name__], f"_prepare_template_{get_platform_name_short()}")
	return cmd(version, config)

def _prepare_template_win(version, config):
	f = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "win", "template.nsi"))
	data = f.read()
	f.close()
	data = data.replace("%JustUpdateRepository%", JustUpdateConstants.REPO_FOLDER)
	data = data.replace("%APP_NAME%", config.get("app_name"))
	data = data.replace("%APP_AUTHOR%", config.get("app_author"))
	data = data.replace("%VERSION%", version.to_string())
	data = data.replace("%COMPLIANT_VERSION%", version.to_nsis_compliant())
	return data

def _prepare_template_mac(version, config):
	# update the Info.plist
	template_plist = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "template.plist"), encoding="utf-8")
	data = template_plist.read()
	template_plist.close()
	data = data.replace("%JustUpdateRepository%", JustUpdateConstants.REPO_FOLDER)
	data = data.replace("%APP_NAME%", config.get("app_name"))
	data = data.replace("%APP_AUTHOR%", config.get("app_author"))
	data = data.replace("%VERSION%", version.to_string())
	data = data.replace("%COMPLIANT_VERSION%", version.to_mac_compliant())
	app_plist = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "dist", "{}.app".format(config.get("app_name")), "Contents", "Info.plist"), "w", encoding="utf-8")
	app_plist.write(data)
	app_plist.close()
	del data
	# update the postinstall script.
	postinstall = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts", "postinstall.sh"), encoding="utf-8")
	data = postinstall.read()
	postinstall.close()
	data = data.replace("%JustUpdateRepository%", JustUpdateConstants.REPO_FOLDER)
	data = data.replace("%APP_NAME%", config.get("app_name"))
	data = data.replace("%APP_AUTHOR%", config.get("app_author"))
	data = data.replace("%VERSION%", version.to_string())
	data = data.replace("%COMPLIANT_VERSION%", version.to_mac_compliant())
	postinstall = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts", "postinstall.sh"), "w", encoding="utf-8")
	postinstall.write(data)
	postinstall.close()
