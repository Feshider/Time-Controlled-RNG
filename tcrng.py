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
from hashlib import sha512 as _sha512


class TCRNG:

    __formating_chars = "aAbBcdHIjmMpSUwWxXyYz"  # 51090942171709440000 permutations
    __key_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
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
    def Random512bitHex(show=True):
        # Return random 512-bit Hex value.
        if (not TCRNG.__generating_seed) and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        TCRNG.__ShufTimeFormChars()
        fs = ""
        for ch in TCRNG.__formating_chars:
            fs += "%" + ch
        return _sha512(_strftime(fs, _localtime())).hexdigest()

    @staticmethod
    def RandBool(show=True):
        # Return random Bool value.
        if (not TCRNG.__generating_seed) and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        return True if int(TCRNG.Random512bitHex(show=False), 16) % 2 == 0 else False

    @staticmethod
    def RandInt(size_in_bites, show=True):
        # Return random n-bit integer.
        if (not TCRNG.__generating_seed) and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        i = 512
        ret = ""
        while True:
            ret += bin(int(TCRNG.Random512bitHex(show=False), 16))[2:].zfill(512)
            i *= 2
            if i >= size_in_bites:
                break
        if size_in_bites == len(ret):
            return int(ret, 2)
        return int(ret[:size_in_bites], 2)

    @staticmethod
    def RandKey(length, show=True):
        # Return random n-leght key consist of chars of base64 charset
        if (not TCRNG.__generating_seed) and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")

        key = ""
        while True:
            temp = bin(int(TCRNG.Random512bitHex(show=False), 16))[2:].zfill(512)[:510]
            temp = [temp[i:i+6] for i in range(0, len(temp), 6)]
            for c in temp:
                key += TCRNG.__key_charset[int(c, 2)]
            if len(key) == length:
                return key
            elif len(key) > length:
                return key[:length]
