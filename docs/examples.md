# Usage Examples

This page collects practical recipes showing how Lex Amoris can be applied to
real-world scenarios.

---

## Example 1 — Quick guidance on an interpersonal conflict

```python
from lex_amoris import LexAmoris

fw = LexAmoris()
print(fw.guidance(
    "My colleague wronged me and I am struggling to move on."
))
```

Output:

```
Lex Amoris guidance for the situation described:
  • [Compassion] Meet suffering with empathy and practical mercy.
  • [Forgiveness] Release resentment and restore relationship where genuine repentance exists.
```

---

## Example 2 — Agent-based reflection with history

```python
from lex_amoris.euystacio import Euystacio

agent = Euystacio()

situations = [
    "I need to tell the truth even though it will hurt someone.",
    "I want to help a stranger who has no one to support them.",
    "I must protect the environment for future generations.",
]

for s in situations:
    agent.reflect(s)

print(f"Total reflections stored: {len(agent.history)}")
for entry in agent.history:
    print(entry)
    print()
```

---

## Example 3 — Building a custom framework

```python
from lex_amoris import LexAmoris
from lex_amoris.core.principles import Principle, DIGNITY, TRUTH

# A lightweight framework focused on professional ethics
professional_fw = LexAmoris(principles=[DIGNITY, TRUTH])
professional_fw.add_principle(Principle(
    name="Confidentiality",
    description="Protect private information entrusted to you.",
    keywords=["private", "confidential", "secret", "data", "information"],
))

print(professional_fw.guidance(
    "A client shared confidential data and I must decide how to handle it."
))
```

---

## Example 4 — Listing applicable principles

```python
from lex_amoris import LexAmoris
from lex_amoris.utils.helpers import list_principles_summary

fw = LexAmoris()
applicable = fw.evaluate("I want to support and care for my community")
print(list_principles_summary(applicable))
```

Output:

```
 1. Benevolence: Actively will and seek the genuine good of every person.
 2. Stewardship: Care for the common good — relationships, communities, ...
```

---

## Example 5 — Principle introspection

```python
from lex_amoris.core.principles import CORE_PRINCIPLES

for p in CORE_PRINCIPLES:
    print(f"{p.name:15s}  keywords: {', '.join(p.keywords)}")
```
