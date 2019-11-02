#!/usr/bin/python
# coding: utf-8
# for python 2.7 or 3.x

from __future__ import print_function  # for 3.x compatibility
import sys
import os
from ctypes import LittleEndianStructure, Union, sizeof, \
                   c_uint32, c_uint16, c_uint8
from curses.ascii import isprint

# Constants
BYTES_PER_LINE = 16

#############################################################################
#class BinaryData(LittleEndianUnion):
class BinaryData(Union):
  _fields_ = (
    ("u8_data", c_uint8 * BYTES_PER_LINE),
    ("u16_data", c_uint16 * 8),
    ("u32_data", c_uint32 * 4),
  )

  def printHexU8(self, num = BYTES_PER_LINE):
    assert(num <= BYTES_PER_LINE)
    for i in range(num):
      printf("%02x ", self.u8_data[i])

  def printHexU16(self, num = BYTES_PER_LINE / 2):
    assert(num <= BYTES_PER_LINE / 2)
    for i in range(num):
      printf("%04x ", self.u16_data[i])

  def printHexU32(self, num = BYTES_PER_LINE / 4):
    assert(num <= BYTES_PER_LINE / 4)
    for i in range(num):
      printf("%08x ", self.u32_data[i])

  def printHex(self, unit, num):
    assert(unit in {1, 2, 4})
    if unit == 1:
      printHexU8(num)
    elif unit == 2:
      printHexU16(num)
    else:
      printHexU32(num)

  def printASCII(self, num = BYTES_PER_LINE):
    for i in range(num):
      printf("%c", self.u8_data[i] if isprint(self.u8_data[i]) else ".")

assert(sizeof(BinaryData) == BYTES_PER_LINE)

#############################################################################
def main(argc, argv):
  if argc < 2:
    printf("Usage: %s file...\n", os.path.basename(argv[0]))
    sys.exit(1)
  offset = 0
  size = 0     # 0 is full-limit
  dump(offset, size, argv[1:])

def dump(offset, size, files):
  for file in files:
    with open(file, "rb") as fh:
      hexdump(fh, offset, size)

def hexdump(fh, offset, size):
  fh.seek(offset, os.SEEK_SET)
  if fh.tell() != offset:
    printf("seek error. (request=%08x, result=%08x)¥n", offset, fh.tell())
    return

  data = BinaryData()
  while True:
    read_bytes = fh.readinto(data)
    if read_bytes <= 0:
      break
    printf("%08x: ", offset)
    data.printHexU8()
    printf("    ")
    data.printASCII()
    printf("\n")
    offset += sizeof(data)

def printf(fmt, *args):
  if args:
    print(fmt % args, end="")
  else:
    print(fmt, end="")

def isAllSameVal(container, val):
  for item in container:
    if item != val:
      return False
  return True

if __name__ == '__main__':
  main(len(sys.argv), sys.argv)
