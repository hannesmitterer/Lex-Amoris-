# Lex Amoris — Euystacio Framework

**Lex Amoris** (Latin: *Law of Love*) is an ethical and relational framework
built on the principle that authentic love — understood as *willing the genuine
good of the other* — is the foundational law governing meaningful human
interaction and decision-making.

The **Euystacio** edition ships a Python package that lets you reason about
real-world situations through the lens of seven core principles, and embodies
that reasoning in the `Euystacio` agent.

---

## Core Principles

| # | Name | In a nutshell |
|---|------|---------------|
| 1 | **Benevolence** | Actively seek the good of every person |
| 2 | **Dignity** | Honour the intrinsic worth of every human being |
| 3 | **Reciprocity** | Give as you would receive |
| 4 | **Compassion** | Meet suffering with empathy and practical mercy |
| 5 | **Truth** | Authentic love cannot be grounded in deception |
| 6 | **Forgiveness** | Release resentment; restore relationship |
| 7 | **Stewardship** | Care for the common good as a sacred trust |

---

## Quick Start

```python
from lex_amoris import LexAmoris
from lex_amoris.euystacio import Euystacio

# Use the framework directly
framework = LexAmoris()
print(framework.guidance("I must respect the dignity of every person"))

# Or let Euystacio reflect on your behalf
agent = Euystacio(framework)
print(agent.reflect("How should I treat a person who is suffering?"))
```

---

## Package Layout

```
lex_amoris/
├── core/
│   ├── principles.py   # Seven core Lex Amoris principles
│   └── framework.py    # LexAmoris class (evaluate + guidance)
├── euystacio/
│   └── entity.py       # Euystacio agent (reflect + history)
└── utils/
    └── helpers.py      # Formatting utilities
tests/
└── test_framework.py   # Full test suite
```

---

## Kosymbiosis Dashboard

An interactive web dashboard visualizing the four foundational modules of the Lex Amoris framework:

- 🌳 **Terra / Habitat** — Bio-construction with natural materials
- 💧 **Acqua / Flusso** — AquaLibre Protocol for free water access
- ☀️ **Fuoco / Luce** — Solar sovereignty and autonomous energy
- 🌬️ **Aria / Verbo** — Truth propagation through resonant communication

**Features:**
- Real-time Schumann Resonance monitoring (7.83 Hz)
- S-ROI (Sovereign Return on Investment) status
- NSR (Non-Slavery Rule) firewall protection
- IPFS anchoring for immutability
- Seedbringer authentication link

**Access:** [View Dashboard](https://hannesmitterer.github.io/Lex-Amoris-/dashboard.html)

---

## Running Tests

```bash
pip install pytest
pytest
```

---

## License

GNU General Public License v3.0 — see [LICENSE](LICENSE).
