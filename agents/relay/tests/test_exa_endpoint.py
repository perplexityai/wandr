import asyncio
import json
import unittest
from unittest import mock

import httpx

from relay.core import RelayError
from relay.providers.exa import ExaAgentEndpoint


class ExaEndpointTests(unittest.TestCase):
    def test_failed_ultra_run_reports_its_cost_before_raising(self):
        created = []

        def handle(request):
            if request.method == "GET":
                return httpx.Response(200, json={"data": [], "hasMore": False})
            if request.url.path.endswith("/cancel"):
                return httpx.Response(200, json={})
            created.append(json.loads(request.content))
            return httpx.Response(
                200,
                json={"id": "run-1", "status": "failed", "costDollars": {"total": 1.5}},
            )

        client = httpx.AsyncClient
        events = []
        endpoint = ExaAgentEndpoint(model_name="ultra", api_key="test")
        with mock.patch.object(
            httpx,
            "AsyncClient",
            lambda **kwargs: client(transport=httpx.MockTransport(handle), **kwargs),
        ):
            with self.assertRaisesRegex(RelayError, "run-1 ended with status failed"):
                asyncio.run(endpoint.run("task", observer=events.append))

        self.assertEqual([payload["effort"] for payload in created], ["ultra"])
        self.assertEqual(
            [event.metadata["cost_usd"] for event in events if event.name == "endpoint.usage"],
            [1.5],
        )


if __name__ == "__main__":
    unittest.main()
