#!/usr/bin/env python

import os
import struct
import sys

def read(path):
	with open(path, "rb") as f:
		return f.read()

def write(path, data):
	with open(path, "wb") as f:
		f.write(data)

def padding(data, size, pattern = '\0'):
	return data + pattern * (size - len(data))

def align(data, size, pattern = '\0'):
	return padding(data, (len(data) + (size - 1)) & ~(size - 1), pattern)

def gen_preloader(data):
	data = align(data, 512, '\xff')
	header = (padding(struct.pack("<12sII", "SF_BOOT", 1, 512), 512, '\xff') +
		  padding(struct.pack("<8sIIIIIIII", "BRLYT", 1, 2048, 2048 + len(data),
			0x42424242, 0x00010007, 2048, 2048 + len(data), 1) + '\0' * 140, 512, '\xff') +
		  '\0' * 1024)
	return header + data

def main(argv):
	input = argv[1]
	output = argv[2]
	write(output, gen_preloader(read(input)))

if __name__ == "__main__":
	main(sys.argv)
