import logging
from logging.config import dictConfig
import time
import argparse

def setup_logging():
	logging.getLogger().name = "JustFuckingUpdate"
	current_time = time.strftime("%Y:%m:%d-%H:%M:%S")
	logging_config = dict(
	version = 1,
	formatters = {
		'f': {'format':
			  '%(name)s %(levelname)-2s %(message)s | %(asctime)s'}
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
	add_build_parser(subparser)
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

def add_build_parser(subparsers):
	build_parser = subparsers.add_parser("build", help="Produce a build with PyInstaller from a python file or JustFuckingUpdate spec file.")
	build_parser.add_argument("--app-version", dest="app_version", required=True)

def add_spec_parser(subparsers):
	spec_parser = subparsers.add_parser("make-spec", help="Produce a JustFuckingUpdate spec file (modified from PyInstaller).")
