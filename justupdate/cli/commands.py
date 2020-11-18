import logging
import os
import shutil

from justupdate import __version__
from justupdate.core.base import confirmation
from justupdate.core.base import get_platform_name_short
from justupdate.core.base import JustUpdateConstants
from justupdate.core.base import prompt
from justupdate.core.config import Config
from justupdate.core.executor import CommandExecutor
from justupdate.core.executor import CommandType
from justupdate.repo.builder import Builder
from justupdate.repo.committer import Committer
from justupdate.repo.uploader import UploadManager

def _cmd_version(args, extra=None):
	logging.info(f"JustUpdate version {__version__}.")

def _cmd_init(args, extra=None):
	if os.path.isfile(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju")) or os.path.isdir(JustUpdateConstants.REPO_FOLDER):
		logging.warning("A JustUpdate repository already exists at this location.")
		return True
	
	# setup a new repo.
	app_name = prompt("Application Name:", "MyAwezomeApp")
	app_author = prompt("Application Author:", "MyAwesomeCompany")
	update_url = prompt("Url to ping for updates:")
	client_config_dir = prompt("Where to place the client_config.py file (used by your application): ", default=".")
	
	if update_url.endswith("/") == False:
		update_url += "/"
	logging.info("Creating folder structure.")
	os.makedirs(JustUpdateConstants.REPO_FOLDER)
	logging.info("Creating config.")
	c = Config()
	c.set("app_name", app_name)
	c.set("app_author", app_author)
	c.set("update_url", update_url)
	c.save(os.path.join(JustUpdateConstants.REPO_FOLDER, "config.ju"))
	logging.info("Saving config.")
	logging.info("Copying templates.")
	shutil.copytree(os.path.join(JustUpdateConstants.MODULE_FOLDER, "templates"), os.path.join(JustUpdateConstants.REPO_FOLDER, "templates"))
	logging.info("Templates copied.")
	logging.info("Creating client config.")
	client_config_data = """class ClientConfig():
	app_name = "{}"
	app_author = "{}"
	update_url = "{}"
""".format(app_name, app_author, update_url)
	with open(os.path.join(client_config_dir, "client_config.py"), "w") as cc:
		cc.write(client_config_data)
	logging.info("Initialization done.")

def _cmd_clean(args, extra=None):
	if os.path.isdir(JustUpdateConstants.REPO_FOLDER) == False:
		logging.warning("No JustUpdate repository exists at this location.")
		return True
	
	# Make sure that the user really wants do delete the repository.
	confirm = confirmation("This will delete the current JustUpdate repository. Are you really sure you want to continue? ", "n")
	if confirm == False:
		logging.info("cancelled...")
		return True
	
	if confirm:
		logging.info("Cleaning repository.")
		logging.info("Deleting files.")
		shutil.rmtree(JustUpdateConstants.REPO_FOLDER)
		logging.info("Clean done.")
		return True

def _cmd_build(args, extra=None):
	builder = Builder()
	builder.clean()
	result = builder.build(args.spec_file, extra)
	if result == True:
		builder.post_build()

def _cmd_commit(args, extra=None):
	committer = Committer(args.app_version)
	if committer.insure_build_availability() == False:
		logging.error("No build for this platform found. please run \"justupdate build\".")
		return True
	committer.setup()
	logging.info(f"Starting commit process for build version {args.app_version} / {committer.version.to_human_readable()}.")
	logging.info("Producing executable")
	if committer.produce_executable() == False:
		# Something went wrong during the executable creation.
		return True
	if committer.create_metadata() == False:
		# something went wrong with metadata creation.
		return True
	committer.finalize()
	logging.info(f"Committed version {committer.version.to_string()}.")
	return True

def _cmd_upload(args, extra=None):
	upload_manager = UploadManager()
	if args.service is None: # no service specified. Show list of available services.
		logging.info("Available services:")
		for uploader_service_name in upload_manager.get_available_upload_services():
			logging.info("{} ({})".format(uploader_service_name, upload_manager.get_service_description(uploader_service_name)))
		return True
	service = upload_manager.get_upload_service(args.service)
	if service is None: # invalid service
		logging.error("Invalid service \"{}\". Available services are {}.".format(args.service, ", ".join(upload_manager.get_available_upload_services())))
	
	if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy")) == False or len(os.listdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))) == 0:
		logging.error("No builds waiting to be deployed. Please produce some builds first.")
		return True
	if os.path.isdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "archive")) == False:
		os.makedirs(os.path.join(JustUpdateConstants.REPO_FOLDER, "archive"))
	logging.info(f"Starting upload with {args.service} uploader service.")
	service = service(upload_manager)
	service.connect()
	files_to_upload = []
	deploy_folder = os.listdir(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy"))
	logging.info("Checking out files for upload.")
	# run the loop 2 times, one for exe's and pkg's and the other for .ju files.
	for file in deploy_folder:
		if os.path.isfile(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy", file)) == False:
			continue
		full_file = os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy", file)
		if full_file.endswith(".exe") or full_file.endswith(".pkg"):
			files_to_upload.append(full_file)
	for file in deploy_folder:
		if os.path.isfile(os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy", file)) == False:
			continue
		full_file = os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy", file)
		if full_file.endswith(".ju"):
			files_to_upload.append(full_file)
	logging.info(f"Files to upload: {files_to_upload}.")
	for _file in files_to_upload:
		logging.debug(f"Starting upload of {_file}.")
		service.upload_file(_file)
		logging.debug(f"Upload of file {_file} completed.")
	service.disconnect()
	logging.info("Upload done. Moving uploaded files to archive.")
	for item in deploy_folder:
		s = os.path.join(JustUpdateConstants.REPO_FOLDER, "deploy", item)
		d = os.path.join(JustUpdateConstants.REPO_FOLDER, "archive", item)
		shutil.move(s, d)
	logging.info("Done")
	return True

def _cmd_make_spec(args, extra=None):
	cmd = ["pyi-makespec", "--name", get_platform_name_short()] + extra + [args.scriptname]
	executor = CommandExecutor()
	result, stdout = executor.execute(cmd, CommandType.RAW)
	if result > 0: # error
		print(stdout)
		logging.error("Please correct the errors above and try again.")
	else:
		logging.info("Spec file written.")
	return True
