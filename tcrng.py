# Copyright 2016 Michal Paulenka
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

####################################################
#     Time Controlled Random Number Generator      #
#                by Feshider 2016                  #
####################################################


from threading import Thread as _Thread
from time import localtime as _localtime
from time import strftime as _strftime
from binascii import crc32 as _crc32


class TCRNG:

    __formating_chars = "aAbBcdHIjmMpSUwWxXyYz"
    __seed = 6
    __generating_seed = False

    @staticmethod
    def __GenerateSeed():
        i = 0
        while TCRNG.__generating_seed:
            if i > 19:
                i = 1
                TCRNG.__seed = i
            else:
                i += 1
                TCRNG.__seed = i

    @staticmethod
    def StartGeneratingSeed():
        # This function must be call at start program
        TCRNG.__generating_seed = True
        t = _Thread(target=TCRNG.__GenerateSeed)
        t.start()

    @staticmethod
    def StopGeneratingSeed():
        TCRNG.__generating_seed = False

    @staticmethod
    def __Rotate(strg, n):
        return strg[n:] + strg[:n]

    @staticmethod
    def __ShufTimeFormChars():
        seed = TCRNG.__seed
        start = 0
        sharp = []
        brk = False
        while True:
            row = []
            for i in range(start, start + seed):
                row.append(TCRNG.__formating_chars[i])
                if TCRNG.__formating_chars[i] == TCRNG.__formating_chars[-1]:
                    sharp.append(row)
                    brk = True
                    break
            if brk:
                break
            sharp.append(row)
            start += seed
        temp = ""
        for r in range(0, len(sharp[0])):
            for c in range(0, len(sharp)):
                try:
                    temp += sharp[c][r]
                except IndexError:
                    pass
        TCRNG.__formating_chars = TCRNG.__Rotate(temp, 1 if (TCRNG.__seed % 2) == 0 else -1)

    @staticmethod
    def Random32bitHex():
        TCRNG.__ShufTimeFormChars()
        fs = ""
        for ch in TCRNG.__formating_chars:
            fs += "%" + ch
        return "%08x" % (_crc32(_strftime(fs, _localtime())) % 4294967296)

    @staticmethod
    def RandBool():
        # Return random Bool value.
        if not TCRNG.__generating_seed:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        return True if int(TCRNG.Random32bitHex(), 16) % 2 == 0 else False

    @staticmethod
    def RandInt(size_in_bites):
        # Return random n-bit integer
        if not TCRNG.__generating_seed:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        integer = ""
        for i in range(0, size_in_bites):
            if TCRNG.RandBool():
                integer += "1"
            else:
                integer += "0"
        return int(integer, base=2)
