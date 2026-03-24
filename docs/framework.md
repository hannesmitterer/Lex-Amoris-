# The LexAmoris Framework

The `LexAmoris` class is the central engine of the framework.  It holds a
collection of principles and exposes two high-level operations:

| Method | Description |
|--------|-------------|
| `evaluate(situation)` | Returns the list of `Principle` objects that apply to the described situation |
| `guidance(situation)` | Returns a human-readable guidance string |

---

## Creating a Framework Instance

```python
from lex_amoris import LexAmoris

# Default instance — all seven core principles
fw = LexAmoris()

# Custom instance — only the principles you choose
from lex_amoris.core.principles import DIGNITY, TRUTH
fw_custom = LexAmoris(principles=[DIGNITY, TRUTH])
```

---

## Evaluating a Situation

`evaluate()` performs keyword matching against the situation text and returns
every principle whose keywords appear in it.

```python
applicable = fw.evaluate("I need to be honest about what I did wrong")
for p in applicable:
    print(p.name)
# Truth
# Forgiveness
```

!!! note
    `evaluate()` raises `ValueError` if the situation string is empty or
    contains only whitespace.

---

## Generating Guidance

`guidance()` wraps `evaluate()` and formats the result as a readable paragraph:

```python
text = fw.guidance("Someone is suffering and needs support")
print(text)
# Lex Amoris guidance for the situation described:
#   • [Benevolence] Actively will and seek the genuine good of every person.
#   • [Compassion] Meet suffering with empathy and practical mercy.
```

When no principle matches, a general love-centred statement is returned:

```python
text = fw.guidance("The speed of light is approximately 3×10⁸ m/s")
print(text)
# Lex Amoris guidance: Approach this situation with love —
# seek the good of every person involved.
```

---

## Adding Custom Principles

```python
from lex_amoris.core.principles import Principle

fw.add_principle(Principle(
    name="Hospitality",
    description="Welcome the stranger as you would welcome a friend.",
    keywords=["stranger", "welcome", "guest", "host"],
))
```

---

## Looking Up a Principle by Name

```python
p = fw.get_principle("Forgiveness")
print(p)  # [Forgiveness] Release resentment and restore relationship ...
```

Returns `None` if the name is not found (lookup is case-insensitive).
