"""Registry of supported Arabic dialects.

Each dialect carries a description that is injected into the system prompt so
the model anchors itself in the right regional variety. Adding a new dialect
is just adding an entry here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Dialect:
    key: str
    name: str
    region: str
    prompt_notes: str


DIALECTS: dict[str, Dialect] = {
    "oran": Dialect(
        key="oran",
        name="Oran Algerian Arabic (Wahrani)",
        region="Oran, western Algeria",
        prompt_notes=(
            "Speak the western Algerian dialect of Oran (الوهرانية / Wahrani). "
            "Authentic markers to use naturally: heavy French borrowings "
            "(e.g. 'normal', 'ça va', 'direct'), Spanish loanwords typical of Oran "
            "(e.g. 'bogado' for lawyer, 'sberdina' for sneaker, 'calentica'), "
            "the 'ntina' second-person pronoun, words like 'wah' (yes), "
            "'kayen' (there is), 'chghol' (like/as if), 'ghaya' (fine/great), "
            "'derwak' (now), 'bezzaf' (a lot), 'wechraki' / 'wech rak' greetings. "
            "Keep the tone warm and playful, like a friend from Oran."
        ),
    ),
    "algiers": Dialect(
        key="algiers",
        name="Algiers Algerian Arabic (Dziri)",
        region="Algiers, central Algeria",
        prompt_notes=(
            "Speak the central Algerian dialect of Algiers (Dziri). "
            "Use typical markers like 'kifash', 'wesh', 'saha', 'bessah', "
            "frequent French code-switching, and the relaxed urban Algiers tone."
        ),
    ),
    "constantine": Dialect(
        key="constantine",
        name="Constantine Algerian Arabic",
        region="Constantine, eastern Algeria",
        prompt_notes=(
            "Speak the eastern Algerian dialect of Constantine, with its Tunisian-leaning "
            "vocabulary and pronunciation (e.g. 'tawa' for now), while staying clearly Algerian."
        ),
    ),
}

DEFAULT_DIALECT = "oran"


def get_dialect(key: str) -> Dialect:
    try:
        return DIALECTS[key.lower()]
    except KeyError:
        available = ", ".join(sorted(DIALECTS))
        raise SystemExit(f"Unknown dialect '{key}'. Available: {available}")
