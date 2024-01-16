#!/bin/bash

mv tests/27_goto.py tests/27_goto.hide
mv tests/09_long.py tests/09_long.hide
mv tests/34_context.py tests/34_context.hide

black -l 132 .

mv tests/27_goto.hide tests/27_goto.py
mv tests/09_long.hide tests/09_long.py
mv tests/34_context.hide tests/34_context.py


find . -regex '.*\.\(cpp\|hpp\|cc\|cxx\)' -exec clang-format --style=GNU -i {} \;
