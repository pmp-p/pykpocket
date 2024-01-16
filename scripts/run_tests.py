import os
import sys
import time


class WorkDir:
    def __init__(self, next):
        self.prev = os.getcwd()
        self.next = next

    def __enter__(self):
        os.chdir(self.next)

    def __exit__(self, *args, **kwargs):
        os.chdir(self.prev)


def test_file(filepath, cpython=False):
    if cpython:
        x, y = os.path.split(filepath)
        with WorkDir(x):
            return os.system("python3 " + y) == 0
    if sys.platform == "win32":
        return os.system("main.exe " + filepath) == 0
    else:
        return os.system("./main " + filepath) == 0


def test_dir(path):
    print("Testing directory:", path)
    for filename in sorted(os.listdir(path)):
        if not filename.endswith(".py"):
            continue
        filepath = os.path.join(path, filename)
        print("> " + filepath, flush=True)

        if path == "benchmarks/":
            _0 = time.time()
            if not test_file(filepath, cpython=True):
                print("cpython run failed")
                continue
            _1 = time.time()
            if not test_file(filepath):
                exit(1)
            _2 = time.time()
            print(f"  cpython:  {_1 - _0:.6f}s (100%)")
            print(f"  pocketpy: {_2 - _1:.6f}s ({(_2 - _1) / (_1 - _0) * 100:.2f}%)")
        else:
            if not test_file(filepath):
                print("-" * 50)
                print("TEST FAILED! Press any key to continue...")
                input()


print("CPython:", str(sys.version).replace("\n", ""))
print("System:", "64-bit" if sys.maxsize > 2**32 else "32-bit")

if len(sys.argv) == 2:
    assert "benchmark" in sys.argv[1]
    d = "benchmarks/"
else:
    d = "tests/"
test_dir(d)
print("ALL TESTS PASSED")
