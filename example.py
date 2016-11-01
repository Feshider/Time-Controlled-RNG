from tcrng import TCRNG


TCRNG.StartGeneratingSeed()  # This is important for randomness. Start thread for seed generation.

print(TCRNG.RandBool())   # This print random bool value.
print(TCRNG.RandInt(8))   # This print random 8-bit integer.
print(TCRNG.RandKey(32))  # This print random 32-char key consist of chars or base64 charset

TCRNG.StopGeneratingSeed()  # This stop thread for seed generation.
