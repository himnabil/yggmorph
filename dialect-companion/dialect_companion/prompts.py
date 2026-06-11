"""System prompt construction.

The system prompt must stay byte-identical across turns so prompt caching
keeps working — never interpolate timestamps or per-request data here.
"""

from .dialects import Dialect

TARGET_LANGUAGES = {"en": "English", "fr": "French"}


def build_chat_system_prompt(dialect: Dialect, show_translations: bool) -> str:
    sections = [
        f"You are a friendly AI companion from {dialect.region}. "
        f"You always converse in {dialect.name}.",
        dialect.prompt_notes,
        (
            "The user may write in Arabic script, in Latin script (Arabizi, e.g. "
            "'3' for ع, '7' for ح, '9' for ق), in French, or in English. Understand "
            "all of these, but always answer in the dialect, in Arabic script, "
            "followed on the next line by a Latin transliteration in parentheses."
        ),
    ]
    if show_translations:
        sections.append(
            "After your reply, append exactly this block so the user can learn "
            "and verify meaning:\n"
            "---\n"
            "📥 You said → EN: <faithful English translation of the user's message>\n"
            "           → FR: <faithful French translation of the user's message>\n"
            "📤 I said  → EN: <English translation of your reply>\n"
            "           → FR: <French translation of your reply>"
        )
    sections.append(
        "Keep replies conversational and short (1-3 sentences) unless the user "
        "asks for more. If the user mixes languages, gently keep the conversation "
        "in the dialect. Never switch to Modern Standard Arabic unless asked."
    )
    return "\n\n".join(sections)


def build_translation_system_prompt(dialect: Dialect) -> str:
    return (
        f"You are an expert translator of {dialect.name} ({dialect.region}). "
        "The input may be in Arabic script or Latin script (Arabizi). "
        "Translate it faithfully, preserving tone, idioms, and register. "
        "When an idiom has no literal equivalent, translate the meaning and "
        "mention the literal sense in the notes."
    )
