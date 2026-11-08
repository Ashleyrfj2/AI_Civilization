#!/bin/bash
# Run the skeleton twice with the same seed and compare outputs.
set -e
A=$(python3 -m ai_civilization.cli run --ticks 5 --seed 42 --db :memory:)
B=$(python3 -m ai_civilization.cli run --ticks 5 --seed 42 --db :memory:)
if [ "$A" = "$B" ]; then echo "DETERMINISTIC: outputs match"; else echo "MISMATCH"; echo "$A"; echo "$B"; exit 1; fi
