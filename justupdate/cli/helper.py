import logging
from logging.config import dictConfig
import time
import argparse

def setup_logging():
	logging.getLogger().name = "JustUpdate"
	current_time = time.strftime("%H:%M:%S")
	logging_config = dict(
	version = 1,
	formatters = {
		'f': {'format':
			  f'{current_time} %(name)s %(levelname)-2s %(message)s'}
		},
	handlers = {
		'h': {'class': 'logging.StreamHandler',
			  'formatter': 'f',
			  'level': logging.DEBUG}
		},
		root = {
		'handlers': ['h'],
		'level': logging.DEBUG,
		},
)
	dictConfig(logging_config)

def get_parser():
	parser = _make_parser()
	subparser = _make_subparser(parser)
	add_version_parser(subparser)
	add_init_parser(subparser)
	add_clean_parser(subparser)
	add_build_parser(subparser)
	add_commit_parser(subparser)
	add_spec_parser(subparser)
	return parser

def _make_parser():
	parser = argparse.ArgumentParser()
	return parser

def _make_subparser(parser):
	subparsers = parser.add_subparsers(help="commands", dest="command")
	return subparsers

def add_version_parser(subparsers):
	version_parser = subparsers.add_parser("version", help="Show version")

def add_init_parser(subparsers):
	init_parser = subparsers.add_parser("init", help="Initialize a JustUpdate repository at the current location.")

def add_clean_parser(subparsers):
	clean_parser = subparsers.add_parser("clean", help="Delete the JustUpdate repository at this location.")

def add_build_parser(subparsers):
	build_parser = subparsers.add_parser("build", help="Produce a build with PyInstaller from a python file or JustUpdate spec file.")

def add_commit_parser(subparsers):
	commit_parser = subparsers.add_parser("commit", help="Commit the produced build created with the build command.")
	commit_parser.add_argument("app-version")

def add_spec_parser(subparsers):
	spec_parser = subparsers.add_parser("make-spec", help="Produce a JustUpdate spec file (modified from PyInstaller).")
