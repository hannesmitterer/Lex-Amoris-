# The Euystacio Agent

`Euystacio` is the **practitioner figure** of the Lex Amoris framework.  Where
`LexAmoris` is an engine, Euystacio is the embodied agent that uses it — keeping
a record of every reflection it has made and presenting guidance in a structured,
timestamped format.

---

## Creating an Agent

```python
from lex_amoris.euystacio import Euystacio

# Default agent using the full core framework
agent = Euystacio()

# Custom name and custom framework
from lex_amoris import LexAmoris
from lex_amoris.core.principles import COMPASSION, DIGNITY

fw = LexAmoris(principles=[COMPASSION, DIGNITY])
agent = Euystacio(framework=fw, name="Aria")
```

---

## Reflecting on a Situation

`reflect()` calls the underlying framework, formats the result, and stores the
reflection in the agent's history.

```python
output = agent.reflect("How should I treat a person who is suffering?")
print(output)
```

Example output:

```
=== Reflection by Euystacio (2026-03-24 01:00 UTC) ===
Situation: How should I treat a person who is suffering?
------------------------------------------------------
Lex Amoris guidance for the situation described:
  • [Benevolence] Actively will and seek the genuine good of every person.
  • [Compassion] Meet suffering with empathy and practical mercy.
```

---

## Inspecting Applicable Principles

If you only need the principles (not the full reflection text):

```python
principles = agent.applicable_principles("I must protect the environment")
for p in principles:
    print(p.name)
# Stewardship
```

---

## Reflection History

Every call to `reflect()` is recorded:

```python
agent.reflect("First situation")
agent.reflect("Second situation")

print(len(agent.history))   # 2
print(agent.history[0])     # full text of the first reflection
```

The `history` property returns a **copy** of the list, so external mutations
do not affect the agent's internal state.

To erase the history:

```python
agent.clear_history()
print(len(agent.history))   # 0
```
