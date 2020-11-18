import logging
import sys

from justupdate import __version__
from justupdate.cli import commands
from justupdate.cli.helper import get_parser
from justupdate.cli.helper import setup_logging
from justupdate.cli.helper import setup_logging_debug

def _real_main(args):
	parser = get_parser()
	args, extra = parser.parse_known_args(args)
	if args.debug:
		setup_logging_debug()
	else:
		setup_logging()
	logging.info(f"JustUpdate - {__version__}.")
	if args.debug:
		logging.info("Debug mode on.")
	result = dispatch_command(args, extra)
	if result == False:
		parser.print_help()
		sys.exit()

def dispatch_command(args, extra=None):
	if args.command is None:
		return False
	cmd_str = "_cmd_" + args.command.replace("-", "_")
	if hasattr(commands, cmd_str):
		cmd = getattr(commands, cmd_str)
		return cmd(args, extra)

def main(args=None):
	try:
		_real_main(args)
	except KeyboardInterrupt:
		# abborted by user
		print("\n")
		log.warning("Abborted by user.")
	except Exception as err:
		print(err)
		logging.error(err)
		logging.debug(err, exc_info=True)

if __name__ == "__main__":
	main(sys.argv[1:])
