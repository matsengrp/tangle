#!/bin/bash
# Yes, bash.

diff <(sort rooted-symmetric/tangle$1.idx) <(sort rooted-asymmetric/tangle$1.idx) > rooted$1.diff
