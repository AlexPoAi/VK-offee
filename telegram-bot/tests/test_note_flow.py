import asyncio
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace

from telegram.error import TimedOut

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

fake_rag_client = ModuleType("rag_client")
fake_rag_client.get_rag_client = lambda: SimpleNamespace()
sys.modules.setdefault("rag_client", fake_rag_client)

import bot  # noqa: E402


class TimeoutMessage:
    text = "📝 Заметка"

    async def reply_text(self, *_args, **_kwargs):
        raise TimedOut("simulated timeout")


class NoteFlowTests(unittest.TestCase):
    def test_note_button_sets_waiting_state_before_reply_success(self):
        context = SimpleNamespace(user_data={})
        update = SimpleNamespace(message=TimeoutMessage())

        asyncio.run(bot.handle_message(update, context))

        self.assertTrue(context.user_data.get("waiting_for_note"))

    def test_note_command_sets_waiting_state_before_reply_success(self):
        context = SimpleNamespace(user_data={})
        update = SimpleNamespace(message=TimeoutMessage())
        context.args = []

        asyncio.run(bot.note_command(update, context))

        self.assertTrue(context.user_data.get("waiting_for_note"))


if __name__ == "__main__":
    unittest.main()
