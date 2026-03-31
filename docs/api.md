# API Reference

## `lex_amoris.core.principles`

### `Principle`

```python
@dataclass
class Principle:
    name: str
    description: str
    keywords: list[str] = []
```

| Member | Type | Description |
|--------|------|-------------|
| `name` | `str` | Short identifier |
| `description` | `str` | Human-readable explanation |
| `keywords` | `list[str]` | Terms used for keyword matching |
| `applies_to(situation)` | `bool` | Returns `True` if any keyword appears in *situation* (case-insensitive) |
| `__str__()` | `str` | `"[name] description"` |

### Pre-built principle constants

| Constant | Name |
|----------|------|
| `BENEVOLENCE` | Benevolence |
| `DIGNITY` | Dignity |
| `RECIPROCITY` | Reciprocity |
| `COMPASSION` | Compassion |
| `TRUTH` | Truth |
| `FORGIVENESS` | Forgiveness |
| `STEWARDSHIP` | Stewardship |
| `CORE_PRINCIPLES` | `list[Principle]` containing all seven |

---

## `lex_amoris.core.framework`

### `LexAmoris`

```python
class LexAmoris:
    def __init__(self, principles: list[Principle] | None = None) -> None: ...
```

| Method / Property | Returns | Description |
|-------------------|---------|-------------|
| `principles` | `list[Principle]` | Read-only copy of active principles |
| `get_principle(name)` | `Principle \| None` | Look up by name (case-insensitive) |
| `add_principle(principle)` | `None` | Append a custom principle |
| `evaluate(situation)` | `list[Principle]` | Applicable principles; raises `ValueError` if empty |
| `guidance(situation)` | `str` | Human-readable guidance string |

---

## `lex_amoris.euystacio.entity`

### `Euystacio`

```python
class Euystacio:
    def __init__(
        self,
        framework: LexAmoris | None = None,
        name: str = "Euystacio",
    ) -> None: ...
```

| Method / Property | Returns | Description |
|-------------------|---------|-------------|
| `name` | `str` | Agent name |
| `framework` | `LexAmoris` | Underlying framework |
| `reflect(situation)` | `str` | Timestamped reflection; recorded in history |
| `applicable_principles(situation)` | `list[Principle]` | Delegates to `framework.evaluate()` |
| `history` | `list[str]` | Read-only copy of past reflections |
| `clear_history()` | `None` | Erase all stored reflections |

---

## `lex_amoris.utils.helpers`

### `format_reflection(agent_name, situation, guidance) → str`

Wraps a reflection into a structured block with a UTC timestamp, a separator
line, and the guidance text.

### `list_principles_summary(principles) → str`

Returns a numbered list of principle names and descriptions, or
`"No principles to display."` if the list is empty.
