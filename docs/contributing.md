# Contributing

Thank you for your interest in contributing to Lex Amoris!  This guide
describes how to set up your development environment and submit changes.

---

## Setting Up

1. **Fork** the repository on GitHub and clone your fork:

    ```bash
    git clone https://github.com/<your-username>/Lex-Amoris-.git
    cd Lex-Amoris-
    ```

2. **Create a virtual environment** and install in editable mode with all
   dev dependencies:

    ```bash
    python -m venv .venv
    source .venv/bin/activate      # Windows: .venv\Scripts\activate
    pip install -e ".[dev,docs]"
    ```

---

## Running Tests

```bash
pytest
```

All tests must pass before submitting a pull request.

---

## Linting

The project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting.

```bash
ruff check .         # lint
ruff format .        # auto-format
ruff format --check .  # check without modifying
```

---

## Building the Docs Locally

```bash
mkdocs serve
```

Then open <http://127.0.0.1:8000> in your browser.  Changes to any `docs/*.md`
file are hot-reloaded automatically.

---

## Submitting a Pull Request

1. Create a branch: `git checkout -b feat/my-change`
2. Make your changes, add tests, update docs if needed.
3. Ensure `pytest` and `ruff check .` both pass.
4. Push and open a pull request against `main`.

---

## Code of Conduct

This project follows the principles of Lex Amoris itself — please engage with
**benevolence**, **dignity**, and **truth** in all interactions.
