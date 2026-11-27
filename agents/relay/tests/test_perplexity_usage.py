import unittest

from relay.core import (
    USAGE_CACHE_READ_INPUT_TOKENS,
    USAGE_INPUT_TOKENS,
    USAGE_OUTPUT_TOKENS,
    USAGE_REASONING_TOKENS,
    USAGE_TOTAL_INPUT_TOKENS,
    USAGE_TOTAL_TOKENS,
    USAGE_UNCACHED_INPUT_TOKENS,
)
from relay.providers.perplexity.events import perplexity_cost_usd, perplexity_usage


class PerplexityUsageTests(unittest.TestCase):
    def test_cache_read_input_tokens(self):
        cases = [
            ("modern", {"cache_read_input_tokens": 800}, 800),
            ("legacy", {"cached_tokens": 800}, 800),
            ("modern_precedence", {"cache_read_input_tokens": 800, "cached_tokens": 300}, 800),
            ("explicit_zero", {"cache_read_input_tokens": 0, "cached_tokens": 800}, 0),
            ("null_modern", {"cache_read_input_tokens": None, "cached_tokens": 800}, 800),
            ("empty_details", {}, 0),
            ("null_details", None, 0),
        ]
        for name, details, cached_tokens in cases:
            with self.subTest(name=name):
                usage = perplexity_usage(
                    {
                        "usage": {
                            "input_tokens": 1000,
                            "output_tokens": 100,
                            "total_tokens": 1100,
                            "input_tokens_details": details,
                            "output_tokens_details": {"reasoning_tokens": 50},
                        }
                    }
                )
                self.assertEqual(
                    usage,
                    {
                        USAGE_INPUT_TOKENS: 1000,
                        USAGE_TOTAL_INPUT_TOKENS: 1000,
                        USAGE_UNCACHED_INPUT_TOKENS: 1000 - cached_tokens,
                        USAGE_CACHE_READ_INPUT_TOKENS: cached_tokens,
                        USAGE_OUTPUT_TOKENS: 100,
                        USAGE_TOTAL_TOKENS: 1100,
                        USAGE_REASONING_TOKENS: 50,
                    },
                )

    def test_missing_input_details(self):
        usage = perplexity_usage({"usage": {"input_tokens": 1000}})
        self.assertEqual(usage[USAGE_CACHE_READ_INPUT_TOKENS], 0)
        self.assertEqual(usage[USAGE_UNCACHED_INPUT_TOKENS], 1000)

    def test_missing_usage(self):
        self.assertEqual(perplexity_usage({}), {})

    def test_server_total_cost_takes_precedence(self):
        for total_cost in (0, 0.123):
            with self.subTest(total_cost=total_cost):
                response = {
                    "usage": {
                        "input_tokens": 1000,
                        "input_tokens_details": {"cache_read_input_tokens": 800},
                        "cost": {"total_cost": total_cost},
                    }
                }
                self.assertEqual(
                    perplexity_cost_usd("openai/gpt-5.5", perplexity_usage(response), response),
                    total_cost,
                )


if __name__ == "__main__":
    unittest.main()
