"""Tests for the Lex Amoris Framework — Euystacio edition."""

import pytest

from lex_amoris import LexAmoris, Principle
from lex_amoris.core.principles import BENEVOLENCE, CORE_PRINCIPLES, DIGNITY
from lex_amoris.euystacio import Euystacio
from lex_amoris.utils.helpers import format_reflection, list_principles_summary

# ── Principle tests ────────────────────────────────────────────────────────


class TestPrinciple:
    def test_str_representation(self):
        p = Principle(name="Test", description="A test principle.")
        assert "[Test]" in str(p)
        assert "A test principle." in str(p)

    def test_applies_to_matching_keyword(self):
        p = Principle(name="X", description="desc", keywords=["help", "care"])
        assert p.applies_to("I want to help someone today")

    def test_applies_to_case_insensitive(self):
        p = Principle(name="X", description="desc", keywords=["HELP"])
        assert p.applies_to("help me please")

    def test_applies_to_no_match(self):
        p = Principle(name="X", description="desc", keywords=["love"])
        assert not p.applies_to("the weather is fine today")

    def test_applies_to_empty_keywords(self):
        p = Principle(name="X", description="desc")
        assert not p.applies_to("anything")


# ── LexAmoris framework tests ──────────────────────────────────────────────


class TestLexAmoris:
    def test_default_principles_loaded(self):
        fw = LexAmoris()
        assert len(fw.principles) == len(CORE_PRINCIPLES)

    def test_custom_principles(self):
        p = Principle(name="Custom", description="custom desc", keywords=["x"])
        fw = LexAmoris(principles=[p])
        assert len(fw.principles) == 1
        assert fw.principles[0].name == "Custom"

    def test_get_principle_found(self):
        fw = LexAmoris()
        p = fw.get_principle("Benevolence")
        assert p is not None
        assert p.name == "Benevolence"

    def test_get_principle_case_insensitive(self):
        fw = LexAmoris()
        p = fw.get_principle("benevolence")
        assert p is not None

    def test_get_principle_not_found(self):
        fw = LexAmoris()
        assert fw.get_principle("Nonexistent") is None

    def test_add_principle(self):
        fw = LexAmoris()
        before = len(fw.principles)
        fw.add_principle(Principle(name="Extra", description="extra"))
        assert len(fw.principles) == before + 1

    def test_add_principle_type_error(self):
        fw = LexAmoris()
        with pytest.raises(TypeError):
            fw.add_principle("not a principle")

    def test_evaluate_returns_applicable(self):
        fw = LexAmoris()
        results = fw.evaluate("I want to help someone in need")
        names = [p.name for p in results]
        assert "Benevolence" in names
        assert "Compassion" in names

    def test_evaluate_empty_situation_raises(self):
        fw = LexAmoris()
        with pytest.raises(ValueError):
            fw.evaluate("")

    def test_evaluate_whitespace_only_raises(self):
        fw = LexAmoris()
        with pytest.raises(ValueError):
            fw.evaluate("   ")

    def test_guidance_with_matching_situation(self):
        fw = LexAmoris()
        text = fw.guidance("I must respect the dignity of every person")
        assert "Lex Amoris guidance" in text
        assert "Dignity" in text

    def test_guidance_with_no_match(self):
        fw = LexAmoris()
        text = fw.guidance("abstract mathematical theorem")
        assert "love" in text.lower()

    def test_principles_property_returns_copy(self):
        fw = LexAmoris()
        original_count = len(fw.principles)
        fw.principles.append(Principle(name="X", description="y"))
        assert len(fw.principles) == original_count


# ── Euystacio agent tests ──────────────────────────────────────────────────


class TestEuystacio:
    def test_default_name(self):
        agent = Euystacio()
        assert agent.name == "Euystacio"

    def test_custom_name(self):
        agent = Euystacio(name="Aria")
        assert agent.name == "Aria"

    def test_str_representation(self):
        agent = Euystacio()
        assert "Euystacio" in str(agent)

    def test_uses_provided_framework(self):
        fw = LexAmoris()
        agent = Euystacio(framework=fw)
        assert agent.framework is fw

    def test_creates_default_framework(self):
        agent = Euystacio()
        assert isinstance(agent.framework, LexAmoris)

    def test_reflect_returns_string(self):
        agent = Euystacio()
        result = agent.reflect("How should I treat a person who is suffering?")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_reflect_records_history(self):
        agent = Euystacio()
        assert len(agent.history) == 0
        agent.reflect("A situation involving honesty")
        assert len(agent.history) == 1

    def test_reflect_accumulates_history(self):
        agent = Euystacio()
        agent.reflect("First situation")
        agent.reflect("Second situation")
        assert len(agent.history) == 2

    def test_history_is_copy(self):
        agent = Euystacio()
        agent.reflect("A situation")
        h = agent.history
        h.append("tampered")
        assert len(agent.history) == 1

    def test_clear_history(self):
        agent = Euystacio()
        agent.reflect("A situation")
        agent.clear_history()
        assert len(agent.history) == 0

    def test_applicable_principles(self):
        agent = Euystacio()
        principles = agent.applicable_principles("I must forgive someone who hurt me")
        names = [p.name for p in principles]
        assert "Forgiveness" in names


# ── Utility helper tests ───────────────────────────────────────────────────


class TestHelpers:
    def test_format_reflection_contains_agent_name(self):
        result = format_reflection("Alice", "A situation", "Some guidance")
        assert "Alice" in result

    def test_format_reflection_contains_situation(self):
        result = format_reflection("Alice", "A hard situation", "Some guidance")
        assert "A hard situation" in result

    def test_format_reflection_contains_guidance(self):
        result = format_reflection("Alice", "A situation", "Key guidance here")
        assert "Key guidance here" in result

    def test_list_principles_summary_empty(self):
        result = list_principles_summary([])
        assert "No principles" in result

    def test_list_principles_summary_numbered(self):
        result = list_principles_summary([BENEVOLENCE, DIGNITY])
        assert "1." in result
        assert "2." in result
        assert "Benevolence" in result
        assert "Dignity" in result
