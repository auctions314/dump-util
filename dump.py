#!/usr/bin/python
# coding: utf-8
# for python 2.7 or 3.2

from __future__ import print_function  # for 3.x compatibility
import os
from argparse import ArgumentParser
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
      self.printHexU8(num)
    elif unit == 2:
      self.printHexU16(num)
    else:
      self.printHexU32(num)

  def printASCII(self, num = BYTES_PER_LINE):
    for i in range(num):
      printf("%c", self.u8_data[i] if isprint(self.u8_data[i]) else ".")

assert(sizeof(BinaryData) == BYTES_PER_LINE)

#############################################################################
def main():
  parser = ArgumentParser()
  parser.add_argument("files", nargs="+", metavar="file")
  parser.add_argument("--version", action="version", version="0.1")
  parser.add_argument("-v", "--verbose", action="store_true")
  parser.add_argument("-s", "--skip", metavar="offset", default="0", type=int)
  parser.add_argument("-n", "--num", metavar="length", default="-1", type=int)
  args = parser.parse_args()
  dump(args.skip, args.num, args.verbose, args.files)

def dump(offset, size, verbose, files):
  for file in files:
    with open(file, "rb") as fh:
      filesize = os.path.getsize(file)
      if verbose:
        printf("%s: %dbytes\n", file, filesize)
      hexdump(fh, offset, filesize if size < 0 else size)
      printf("\n")

def hexdump(fh, offset, size):
  fh.seek(offset, os.SEEK_SET)
  data = BinaryData()
  while size > 0:
    read_bytes = fh.readinto(data)
    if read_bytes <= 0:
      break
    n = min([read_bytes, size]) 
    printf("%08x: ", offset)
    data.printHex(1, n)
    printf("    " + "   " * (sizeof(data) - n))
    data.printASCII(n)
    printf("\n")
    offset += sizeof(data)
    size -= n

def printf(fmt, *args):
  if args:
    print(fmt % args, end="")
  else:
    print(fmt, end="")

if __name__ == '__main__':
  main()
