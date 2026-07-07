from morse_encoder import MorseEncoder
from keyer import Keyer

encoder = MorseEncoder()
keyer = Keyer(18)

patterns = encoder.encode_text("CQ TEST")

print(patterns)

for pattern in patterns:

    keyer.queue_pattern(pattern)

print()

while keyer.busy():

    print(keyer.get_next_pattern())