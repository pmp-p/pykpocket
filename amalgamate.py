import os

os.system("python3 prebuild.py")

with open("include/pocketpy/opcodes.h", "rt", encoding='utf-8') as f:
	OPCODES_TEXT = '\n' + f.read() + '\n'

pipeline = [
	["config.h", "export.h", "common.h", "memory.h", "vector.h", "str.h", "tuplelist.h", "namedict.h", "error.h", "lexer.h"],
	["obj.h", "dict.h", "codeobject.h", "frame.h"],
	["gc.h", "vm.h", "ceval.h", "expr.h", "compiler.h", "repl.h"],
	["_generated.h", "cffi.h", "bindings.h", "iter.h", "base64.h", "csv.h", "collections.h", "random.h", "re.h", "linalg.h", "easing.h", "io.h"],
	["pocketpy.h", "pocketpy_c.h"]
]

copied = set()
text = ""

import re
import shutil
import os
import sys
import time

if os.path.exists("amalgamated"):
	shutil.rmtree("amalgamated")
	time.sleep(0.5)
os.mkdir("amalgamated")

def remove_copied_include(text):
	text = text.replace("#pragma once", "")

	def _replace(m):
		key = m.group(1)
		if key.startswith("pocketpy/"):
			key = key[9:]
		if key in ["user_config.h", "box2dw.hpp", "cJSONw.hpp"]:
			return m.group(0)
		if key == "opcodes.h":
			return OPCODES_TEXT
		assert key in copied, f"include {key} not found"
		return ""

	text = re.sub(
		r'#include\s+"(.+)"\s*',
		_replace,
		text
	)
	return text

for seq in pipeline:
	for j in seq:
		print(j)
		with open("include/pocketpy/"+j, "rt", encoding='utf-8') as f:
			text += remove_copied_include(f.read()) + '\n'
			copied.add(j)
		j = j.replace(".h", ".cpp")
		if os.path.exists("src/"+j):
			with open("src/"+j, "rt", encoding='utf-8') as f:
				text += remove_copied_include(f.read()) + '\n'
				copied.add(j)

with open("amalgamated/pocketpy.h", "wt", encoding='utf-8') as f:
	final_text = \
r'''/*
 *  Copyright (c) 2023 blueloveTH
 *  Distributed Under The MIT License
 *  https://github.com/blueloveTH/pocketpy
 */

#ifndef POCKETPY_H
#define POCKETPY_H
''' + text + '\n#endif // POCKETPY_H'
	f.write(final_text)

shutil.copy("src2/main.cpp", "amalgamated/main.cpp")
with open("amalgamated/main.cpp", "rt", encoding='utf-8') as f:
	text = f.read()
text = text.replace('#include "pocketpy/pocketpy.h"', '#include "pocketpy.h"')
with open("amalgamated/main.cpp", "wt", encoding='utf-8') as f:
	f.write(text)

if sys.platform in ['linux', 'darwin']:
	ok = os.system("clang++ -o main amalgamated/main.cpp -O1 --std=c++17 -stdlib=libc++")
	if ok == 0:
		print("Test build success!")

print("amalgamated/pocketpy.h")

def sync(path):
	shutil.copy("amalgamated/pocketpy.h", os.path.join(path, "pocketpy.h"))
	with open(os.path.join(path, "pocketpy.cpp"), "wt", encoding='utf-8') as f:
		f.write("#include \"pocketpy.h\"\n")

sync("plugins/macos/pocketpy")
