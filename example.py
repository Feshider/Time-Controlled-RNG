import tcrng



tcrng.StartSeedGeneration()           # This is important for randomness. Start thread for seed generation.

print(tcrng.Rand512bitHex())          # This print random 512-bit Hex.
print(tcrng.RandBool())               # This print random bool value.
print(tcrng.RandInt(0, 255))          # This print random integer in range 0 and 255 including both values.
print(tcrng.RandKey(32))              # This print random 32-char key consist of chars or base64 charset.
print(tcrng.RandBytes(8))             # This print random 8-byte bytearray object.
print(tcrng.RandListOfInt(10, 0, 10)) # This print random 10-items leght list consist of integers before 0 and 10 including both values.

tcrng.StopSeedGeneration()            # This stop thread for seed generation.
