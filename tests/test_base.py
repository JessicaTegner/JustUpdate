"""These tests test the functionality in justupdate/core/base.py"""

from . import util
import platform

from justupdate.core.base import get_platform_name_short
def test_platform_names():
	platform_name = platform.system()
	
	if platform_name == "Windows":
		assert get_platform_name_short() == "win"
	if platform_name == "Darwin":
		assert get_platform_name_short() == "mac"

