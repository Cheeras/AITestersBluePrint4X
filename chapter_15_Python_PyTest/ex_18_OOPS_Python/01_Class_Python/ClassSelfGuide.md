# Understanding `self` in Python Classes

## What is `self`?

`self` is a **reference to the current instance** of the class. It's how a method knows **which object** called it.

---

## Think of it like this

When you write a regular function (no class), you pass data explicitly:

```python
def bark(name):
    print(f"{name} is barking")

bark("Tommy")  # You pass the name directly
```

But when you use a **class**, the object itself is automatically passed as the first argument — and by convention we call it `self`.

---

## Compare: Without `self` vs With `self`

### ❌ Regular functions (what you've done before)

```python
name = "Tommy"

def bark():
    print("Barking")

bark()  # No self needed
```

### ✅ Class methods (what you're learning now)

```python
class Dog:
    name = "Tommy"

    def bark(self):          # <-- self refers to the specific Dog instance
        print(self.name)     # <-- self.name accesses THAT instance's name

chow = Dog()   # chow is an instance
chow.bark()    # Python automatically passes chow as self
```

---

## Why does Python need `self`?

Because **one class can create many objects**, and each object has its own data:

```python
class Dog:
    name = None

    def bark(self):
        print(f"{self.name} says Woof!")

dog1 = Dog()
dog1.name = "Tommy"

dog2 = Dog()
dog2.name = "Bruno"

dog1.bark()  # Tommy says Woof!  (self = dog1)
dog2.bark()  # Bruno says Woof!   (self = dog2)
```

Without `self`, the method wouldn't know **which dog's name** to print.

---

## Key points to remember

| Concept | Explanation |
|---------|-------------|
| `self` is **not a keyword** | It's just a **convention** — you could name it `this` or `myself`, but everyone uses `self` |
| It's **always the first parameter** | In class methods, the first parameter is always the instance itself |
| You **don't pass it manually** | Python passes it automatically when you call `object.method()` |
| It gives access to **instance variables** | Like `self.name`, `self.breed`, `self.weight` |

---

## In your code (`122.py`)

```python
class Dog:
    name = None          # Class variable
    breed = None

    def bark(self):      # self = the specific dog that calls bark()
        print(self.name) # Accesses that dog's name

chow = Dog()             # chow is an instance
chow.name = "Chow"       # Set name on this instance
chow.bark()              # Python does: bark(chow) → self = chow
```

So `self.name` accesses the `name` of whichever `Dog` object calls `bark()`.

---

## Bottom line

Think of `self` as saying **"this object's"** — `self.name` = "this object's name". You only need it inside class methods, not in regular standalone functions.