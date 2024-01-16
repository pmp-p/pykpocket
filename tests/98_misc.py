a = 0

a += 2
assert a == 2

a -= 1
assert a == 1

a *= 2
assert a == 2

a //= 2
assert a == 1

a |= 0xFF
assert a == 0xFF

a &= 0x0F
assert a == 0x0F

a = 8

a %= 3
assert a == 2

a ^= 0xF0
assert a == 242


# incremental set
class A:
    pass


for i in range(ord("a"), ord("z") + 1):
    setattr(A, chr(i), i)

assert A.a == ord("a")
assert A.z == ord("z")
