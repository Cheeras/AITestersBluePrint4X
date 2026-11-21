class MathClass:
    def add(self, a, b):              # First definition
        return a + b

    def add(self, a, b, c):           # Second definition — OVERRIDES!
        return a - b - c

m = MathClass()
print(m.add(10, 20))     # ❌ TypeError: add() missing 1 required positional argument: 'c'
print(m.add(10, 20, 30)) # → -40  (only the SECOND method exists!)