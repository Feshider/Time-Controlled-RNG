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


from threading import Thread
from time import localtime, strftime
from binascii import crc32


class TCRNG:
    formating_chars = "aAbBcdHIjmMpSUwWxXyYz"
    seed = 6
    generating_seed = False

    @staticmethod
    def GenerateSeed():
        i = 0
        while TCRNG.generating_seed:
            if i > 19:
                i = 1
                TCRNG.seed = i
            else:
                i += 1
                TCRNG.seed = i

    @staticmethod
    def StartGeneratingSeed():
        # This function must be call at start program
        TCRNG.generate_seed = True
        t = Thread(target=TCRNG.GenerateSeed)
        t.start()

    @staticmethod
    def StopGeneratingSeed():
        TCRNG.generate_seed = False

    @staticmethod
    def Rotate(strg, n):
        return strg[n:] + strg[:n]

    @staticmethod
    def ShufTimeFormChars():
        seed = TCRNG.seed
        start = 0
        sharp = []
        brk = False
        while True:
            row = []
            for i in range(start, start + seed):
                row.append(TCRNG.formating_chars[i])
                if TCRNG.formating_chars[i] == TCRNG.formating_chars[-1]:
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
        TCRNG.formating_chars = TCRNG.Rotate(temp, 1 if (TCRNG.seed % 2) == 0 else -1)

    @staticmethod
    def Random32bitHex():
        TCRNG.ShufTimeFormChars()
        fs = ""
        for ch in TCRNG.formating_chars:
            fs += "%" + ch
        return "%08x" % (crc32(strftime(fs, localtime())) % 4294967296)

    @staticmethod
    def RandBool():
        # Return random Bool value.
        if not TCRNG.generating_seed:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        return True if int(TCRNG.Random32bitHex(), 16) % 2 == 0 else False

    @staticmethod
    def RandInt(size_in_bites):
        # Return random n-bit integer
        if not TCRNG.generating_seed:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        integer = ""
        for i in range(0, size_in_bites):
            if TCRNG.RandBool():
                integer += "1"
            else:
                integer += "0"
        return int(integer, base=2)
