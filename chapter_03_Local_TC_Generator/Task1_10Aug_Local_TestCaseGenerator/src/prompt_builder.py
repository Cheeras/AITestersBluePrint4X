"""Builds the final LLM prompt from the template, requirements, and rules."""
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "templates", "testcase_creator.md")

RULES_PATH = os.path.join(
    PROJECT_ROOT, "..", "..", "..",
    "chapter_01_LLMBasics", "ANTI-HALLUCINATION.rules.md"
)


class PromptBuilder:
    """Combines the test-case template with real requirements."""

    def __init__(self, template_path=None, rules_path=None):
        self.template_path = template_path or TEMPLATE_PATH
        self.rules_path = rules_path or RULES_PATH

    def _read_template(self) -> str:
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    def _read_rules(self) -> str:
        try:
            with open(self.rules_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return (
                "## Anti-Hallucination Rule\n"
                "Use ONLY the provided requirements. "
                "Do NOT assume undocumented behavior. "
                "If information is missing, state 'Not specified'."
            )

    def _estimate_test_count(self, requirements: str) -> int:
        """Heuristic: ~1 test case per 50 words of requirement text."""
        words = len(requirements.split())
        count = max(5, words // 50)
        return min(count, 30)  # cap at 30

    def build(
        self,
        requirements: str,
        feature: str = "Login Module",
        test_count: int = None,
    ) -> str:
        """
        Build the final prompt.

        Args:
            requirements: The feature requirements text.
            feature: Name of the feature under test.
            test_count: Override auto-estimate; None = auto.
        """
        template = self._read_template()
        num = test_count or self._estimate_test_count(requirements)
        rules = self._read_rules()

        prompt = (
            template
            .replace("[NUMBER]", str(num))
            .replace("[FEATURE]", feature)
            .replace("[PASTE REQUIREMENTS HERE]", requirements)
        )

        # Append anti-hallucination rules
        prompt += f"\n\n{rules}"
        return prompt