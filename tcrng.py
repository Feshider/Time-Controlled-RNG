# Copyright 2016 Michal Paulenka <paulenkamichal@gmail.com>
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
from time import localtime
from time import strftime
from hashlib import sha512

__all__ = ["StartSeedGeneration", "StopSeedGeneration", "Rand512bitHex", "RandInt", "RandBool", "RandKey", "RandBytes",
           "RandListOfInt", "__version__", "__author__"]

__doc__ = "This module is time based random number generator, provide six functions for generation random data. " \
          "The most important thing is call StartSeedGeneration() on start program. This is important for random " \
          "output of functions."

__version__ = "0.9"

__author__ = "Feshider"


class TCRNG:
    formating_chars = "aAbBcdHIjmMpSUwWxXyYz"  # 51090942171709440000 permutations
    key_charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
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
    def StartSeedGeneration():
        TCRNG.generating_seed = True
        t = Thread(target=TCRNG.GenerateSeed)
        t.start()
        try:
            f = open("internal_state.txt", "r")
            content = f.read()
            if content != "":
                for c in content:
                    if c not in TCRNG.formating_chars:
                        f.close()
                        return
                TCRNG.formating_chars = content
        except IOError:
            pass
        else:
            f.close()


    @staticmethod
    def StopSeedGeneration():
        TCRNG.generating_seed = False
        try:
            f = open("internal_state.txt", "w")
            f.seek(0)
            f.truncate()
        except IOError:
            f = open("internal_state.txt", "w+")
        finally:
            f.write(TCRNG.formating_chars)
            f.close()

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
    def Rand512bitHex(show):
        if not TCRNG.generating_seed and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        TCRNG.ShufTimeFormChars()
        fs = ""
        for ch in TCRNG.formating_chars:
            fs += "%" + ch
        return sha512(strftime(fs, localtime())).hexdigest()

    @staticmethod
    def RandBool(show):
        if not TCRNG.generating_seed and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")
        return True if int(TCRNG.Rand512bitHex(show=False), 16) % 2 == 0 else False

    @staticmethod
    def RandInt(_min, _max, show):
        if not TCRNG.generating_seed and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")

        rand = ""
        m = (_max + 1) - _min
        i = 1
        while True:
            rand += TCRNG.Rand512bitHex(show=False)
            if m <= (2 ** (512 * i)):
                return (int(rand, 16) % m) + _min
            i += 1

    @staticmethod
    def RandKey(length, show=True):
        if not TCRNG.generating_seed and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")

        key = ""
        while True:
            temp = bin(int(TCRNG.Rand512bitHex(show=False), 16))[2:].zfill(512)[:510]
            temp = [temp[i:i + 6] for i in range(0, len(temp), 6)]
            for c in temp:
                key += TCRNG.key_charset[int(c, 2)]
            if len(key) == length:
                return key
            elif len(key) > length:
                return key[:length]

    @staticmethod
    def RandBytes(size, show):
        if not TCRNG.generating_seed and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")

        size *= 2
        rand = ""
        while True:
            rand += TCRNG.Rand512bitHex(show=False)
            if len(rand) == size:
                return bytearray.fromhex(rand)
            elif len(rand) > size:
                return bytearray.fromhex(rand[:size])

    @staticmethod
    def RandListOfInt(length, _min, _max, show):
        if not TCRNG.generating_seed and show:
            print(" !WARNING! Seed generator not running. Function return less random value.")

        ls = []
        for i in range(length):
            ls.append(TCRNG.RandInt(_min, _max, show=False))
        return ls


def StartSeedGeneration():
    """This function start thread for seed generation. Its important for randomness. If exist file "internal_state.txt",
    in module directory, module load permutation of formatting chars from this file."""
    TCRNG.StartSeedGeneration()


def StopSeedGeneration():
    """This function stop thread for seed generation. When call this function module save actually permutation of
    TCRNG.StopSeedGeneration()


def Rand512bitHex(show=True):
    """Return random 512-bit Hex value."""
    return TCRNG.Rand512bitHex(show)


def RandBool(show=True):
    """Return random bool value."""
    return TCRNG.RandBool(show)


def RandInt(_min, _max, show=True):
    """Return random integer in range _min and _max (including min and max)."""
    return TCRNG.RandInt(_min, _max, show)


def RandKey(length, show=True):
    """Return random key in defined length consist of chars of base64 charset"""
    return TCRNG.RandKey(length, show)


def RandBytes(size, show=True):
    """Return random bytearray in defined size."""
    return TCRNG.RandBytes(size, show)


def RandListOfInt(length, _min, _max, show=True):
    """Return a list of defined length consist of integers in a defined range."""
    return TCRNG.RandListOfInt(length, _min, _max, show)
