# Lex Amoris — Euystacio Framework

!!! tip "Interactive Dashboard Available"
    **[🚀 Launch Kosymbiosis Dashboard →](../dashboard.html)**
    
    Experience the live interface with real-time monitoring of the four foundational modules, Schumann Resonance (7.83 Hz), S-ROI status, and more.

**Lex Amoris** (Latin: *Law of Love*) is an ethical and relational framework
built on the principle that **authentic love** — understood as *willing the
genuine good of the other* — is the foundational law governing meaningful human
interaction and decision-making.

The **Euystacio** edition ships a Python package that lets you reason about
real-world situations through the lens of seven core principles, and embodies
that reasoning in the `Euystacio` agent.

---

## Why Lex Amoris?

Traditional ethical frameworks tend to locate moral authority in duty, utility,
or virtue alone.  Lex Amoris argues that each of these is a *derivative* of
love rightly understood.  By placing love at the centre, the framework offers:

- **Integration** — duty, care, and virtue are unified rather than competing.
- **Motivation** — love gives agents an intrinsic reason to act well.
- **Relationality** — it keeps the *other* at the heart of every decision.

---

## Quick Start

Install the package:

```bash
pip install lex-amoris
```

Use the framework directly:

```python
from lex_amoris import LexAmoris

fw = LexAmoris()
print(fw.guidance("I must respect the dignity of every person"))
```

Or delegate to the Euystacio agent:

```python
from lex_amoris.euystacio import Euystacio

agent = Euystacio()
print(agent.reflect("How should I treat a person who is suffering?"))
```

---

## Package Layout

| Module | Purpose |
|--------|---------|
| `lex_amoris.core.principles` | Seven foundational `Principle` objects |
| `lex_amoris.core.framework`  | `LexAmoris` — evaluate situations and produce guidance |
| `lex_amoris.euystacio.entity`| `Euystacio` agent — reflect, history |
| `lex_amoris.utils.helpers`   | Formatting utilities |

Navigate the **Guide** section to learn more about each component.
