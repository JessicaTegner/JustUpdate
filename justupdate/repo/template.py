import sys
import os
import stat

from justupdate.core.base import JustUpdateConstants, get_platform_name_short
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor, CommandType

def prepare_template(version):
	config = Config()
	config.load(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
	cmd = getattr(sys.modules[__name__], "_prepare_template_{}".format(get_platform_name_short()))
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
	template_plist = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "template.plist"), "r", encoding="utf-8")
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
	postinstall = open(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts", "postinstall.sh"), "r", encoding="utf-8")
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
	# make sure postinstall script are executable.
	#st = os.stat(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts", "postinstall.sh"))
	#os.chmod(os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts", "postinstall.sh"), st.st_mode | 0o111)
	executor = CommandExecutor()
	cmd = ["chmod", "x+", os.path.join(JustUpdateConstants.REPO_FOLDER, "templates", "mac", "scripts", "postinstall.sh")]
	result, stdout = executor.execute(cmd, CommandType.Raw)
	if result > 0:
		print(stdout)
		sys.exit()


