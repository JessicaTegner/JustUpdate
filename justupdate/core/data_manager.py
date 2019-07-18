import hashlib
import zlib

def calculate_checksum(filename, chunk_size=2048):
	checksum = hashlib.sha512()
	f = open(filename, "rb")
	while True:
		data = f.read(chunk_size)
		if not data:
			break
		checksum.update(data)
	f.close()
	return checksum.hexdigest()

def open_file(*args):
	f = open(*args)
	data = b""
	while True:
		d = f.read(1024)
		if not d:
			break
		data += d
	f.close()
	return data

def open_file_unicode(*args):
	f = open(*args)
	data = ""
	while True:
		d = f.read(1024)
		if not d:
			break
		data += d
	f.close()
	return data

def compress(data, compression_level=6):
	if not isinstance(data, bytes):
		data = data.encode()
	return zlib.compress(data, level=compression_level)

def decompress(data):
	if not isinstance(data, bytes):
		data = data.encode()
	return zlib.decompress(data)
