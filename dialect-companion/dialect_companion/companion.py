"""Core companion logic: streaming chat and structured translation."""

from typing import Iterator

import anthropic
from pydantic import BaseModel, Field

from .dialects import Dialect
from .prompts import build_chat_system_prompt, build_translation_system_prompt

MODEL = "claude-opus-4-8"


class Translation(BaseModel):
    detected_input: str = Field(description="The input as understood, normalized to Arabic script")
    standard_arabic: str = Field(description="Modern Standard Arabic rendering")
    english: str = Field(description="Faithful English translation")
    french: str = Field(description="Faithful French translation")
    notes: str = Field(description="Brief notes on idioms, loanwords, or ambiguity; empty if none")


class Companion:
    def __init__(self, dialect: Dialect, show_translations: bool = True):
        self.client = anthropic.Anthropic()
        self.dialect = dialect
        self.show_translations = show_translations
        self.messages: list[dict] = []

    @property
    def _system(self) -> list[dict]:
        return [
            {
                "type": "text",
                "text": build_chat_system_prompt(self.dialect, self.show_translations),
                "cache_control": {"type": "ephemeral"},
            }
        ]

    def chat(self, user_text: str) -> Iterator[str]:
        """Send a user message and yield the reply as it streams."""
        self.messages.append({"role": "user", "content": user_text})
        chunks: list[str] = []
        with self.client.messages.stream(
            model=MODEL,
            max_tokens=64000,
            thinking={"type": "adaptive"},
            output_config={"effort": "low"},
            system=self._system,
            messages=self.messages,
        ) as stream:
            for text in stream.text_stream:
                chunks.append(text)
                yield text
            final = stream.get_final_message()

        if final.stop_reason == "refusal":
            self.messages.pop()
            yield "\n[The model declined to answer this message.]"
            return

        self.messages.append({"role": "assistant", "content": "".join(chunks)})

    def translate(self, text: str) -> Translation:
        """One-shot structured translation of dialect text."""
        response = self.client.messages.parse(
            model=MODEL,
            max_tokens=16000,
            thinking={"type": "adaptive"},
            system=build_translation_system_prompt(self.dialect),
            messages=[{"role": "user", "content": f"Translate this:\n\n{text}"}],
            output_format=Translation,
        )
        if response.stop_reason == "refusal":
            raise RuntimeError("The model declined to translate this text.")
        return response.parsed_output
