# Changelog

All notable changes to Lex Amoris are documented here.
This project follows [Semantic Versioning](https://semver.org/).

---

## [0.1.0] — 2026-03-24

### Added

- `lex_amoris.core.principles`: Seven foundational `Principle` dataclasses
  (Benevolence, Dignity, Reciprocity, Compassion, Truth, Forgiveness, Stewardship)
  with keyword-based `applies_to()` matching.
- `lex_amoris.core.framework`: `LexAmoris` class with `evaluate()` and
  `guidance()` methods.
- `lex_amoris.euystacio.entity`: `Euystacio` agent with `reflect()`,
  `applicable_principles()`, history management, and `clear_history()`.
- `lex_amoris.utils.helpers`: `format_reflection` and `list_principles_summary`
  formatting utilities.
- Full test suite (34 tests) under `tests/`.
- MkDocs documentation site with Material theme, deployed to GitHub Pages.
- GitHub Actions workflows for CI (lint + multi-version test matrix),
  GitHub Pages deployment, and tag-triggered releases.
