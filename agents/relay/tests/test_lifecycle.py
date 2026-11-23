import os
import subprocess
import sys
import unittest

_PROBE = (
    "import signal, relay.lifecycle as lifecycle; "
    "print(signal.getsignal(signal.SIGTERM) is lifecycle._handle_signal)"
)


def _installs_on_import(**env: str) -> bool:
    result = subprocess.run(
        [sys.executable, "-c", _PROBE],
        env={**os.environ, **env},
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() == "True"


class SignalHandlerTests(unittest.TestCase):
    def test_import_installs_signal_handlers_by_default(self):
        self.assertTrue(_installs_on_import())

    def test_env_opts_out_of_signal_handlers(self):
        self.assertFalse(_installs_on_import(RELAY_SIGNAL_HANDLERS="0"))


if __name__ == "__main__":
    unittest.main()
