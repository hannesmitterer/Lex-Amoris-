# Core Principles

Lex Amoris organises ethical reasoning around **seven foundational principles**.
Each principle is a `Principle` dataclass instance with a name, a description,
and a set of keywords that allow the framework to identify which principles are
relevant to any described situation.

---

## 1 · Benevolence

> *Actively will and seek the genuine good of every person.*

Benevolence is the root of all the other principles.  It asks not merely that
we avoid harm, but that we **actively pursue the flourishing** of those around
us.  It is the positive face of love.

**Keywords:** good, help, benefit, welfare, care, support

---

## 2 · Dignity

> *Recognise and honour the intrinsic worth of every human being, regardless of circumstance.*

Every person carries an inalienable worth that cannot be earned or forfeited.
Dignity demands that we treat every individual as an **end in themselves**, never
as a mere means.

**Keywords:** worth, respect, dignity, value, person, human

---

## 3 · Reciprocity

> *Give as you would receive; hold others to the same standard as yourself.*

Reciprocity is the principle of fairness and mutuality.  It extends the
golden rule into the framework: genuine love does not apply double standards.

**Keywords:** fair, equal, reciprocal, mutual, exchange, justice

---

## 4 · Compassion

> *Meet suffering with empathy and practical mercy.*

Compassion moves beyond feeling sorry for another's pain to **acting in
response** to it.  It integrates emotional empathy with concrete help.

**Keywords:** suffer, pain, grief, need, mercy, empathy, compassion

---

## 5 · Truth

> *Speak and act with honesty; authentic love cannot be grounded in deception.*

A love that manipulates or deceives is a contradiction in terms.  Truth
protects the dignity of the other by giving them **accurate information** with
which to make genuine choices.

**Keywords:** honest, truth, sincere, transparent, open, trust

---

## 6 · Forgiveness

> *Release resentment and restore relationship where genuine repentance exists.*

Forgiveness is not the erasure of accountability; it is the **refusal to let
past wrongs define the future**.  It creates space for redemption and
reconciliation.

**Keywords:** forgive, pardon, reconcile, restore, wrong, hurt

---

## 7 · Stewardship

> *Care for the common good — relationships, communities, and the natural world — as a sacred trust.*

Love is not only interpersonal.  Stewardship extends it to the collective:
**protecting and sustaining** the shared goods on which human flourishing depends.

**Keywords:** community, environment, common, steward, protect, sustain

---

## Using Principles in Code

```python
from lex_amoris.core.principles import DIGNITY, CORE_PRINCIPLES

# Check whether a principle applies to a situation
print(DIGNITY.applies_to("I must respect every person I meet"))  # True

# Iterate all core principles
for p in CORE_PRINCIPLES:
    print(p)
```
