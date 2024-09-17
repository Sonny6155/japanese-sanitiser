import re

# Filters based on https://www.localizingjapan.com/blog/2012/01/20/regular-expressions-for-japanese-text/
# Some changes were made for precision required
# Using only built in re, Unicode block property syntax is not supported

INPUT_FILENAME = "data/lyrics.txt"
OUTPUT_FILENAME = "output/out.txt"

# The "acceptable" ranges
PUNC_RANGES = {
    "en": r"\u0020-\u002f\u003a-\u003f\u005b-\u0060\u007b-\u007e",
    "jp": (
        r"\u3000-\u301f" +  # CJK punc
        r"\u30fb\u30fc" +  # Katakana
        r"\uff01-\uff0f\uff1a-\uff20\uff3b-\uff40\uff5b-\uff60" +  # Full-width
        r"\uff61-\uff65\uff70\uff9e\uff9f"  # Half-width
    ),
}

TEXT_RANGES = {
    "en": "0-9A-Za-z",
    "jp": (
        r"\u3041-\u3096" +  # Hiragana
        r"\u30a1-\u30ef\u30f2-\u30f9" +  # Katakana
        r"\uff10-\uff19\uff21-\uff3a\uff41-\uff5a" +  # Full-width Latin
        r"\uff66-\uff6f\uff71-\uff9d" +  # Half-width katakana
        r"\u3400-\u4db5\u4e00-\u9fcb\uF900-\uFa6a"  # CJK unified (kanji)
    ),
}
# Rare "w-" are removed in both hiragana/katakana
# "v-" and small kana are sometimes still used in katakana, so only removed in hiragana

# Very rare/obsolete kana, rare/half-width punctuation
# May overlap the accepted ranges
WARNING_RANGES = {
    "unusual_hiragana": r"\u3090\u3091\u3094-\u3096\u3099-\u309f",
    "unusual_katakana": r"\u30f0\u30f1\u30ff",
    "half_katakana": r"\uff66-\uff6f\uff71-\uff9d",
    "unusual_jp_punc": r"\u30a0\uff61-\uff65\uff70\uff9e\uff9f",
    "cjk_radicals": r"\u2e80-\u2e99\u2e9b-\u2ef3",  # Supplements Kangxi
    "kangxi_radicals": r"\u2f00-\u2fd5",
    "iteration_marks": r"\u3005\u309d\u309e\u30fd\u30fe",
    "katakana_extensions": r"\u31f0-\u31ff",  # Ainu-only small katakana
    "jp_symbols": r"\u3220-\u3243\u3280-\u337f",
}
# Generally speaking, only dounojiten iteration mark is valid
# Kana iteration and similar should also be converted in formal writing

# optional warnings include if jp alphanumeric were used


def detect_language(text: str) -> None:
    print(
        "Punctuation language(s):", [
            lang
            for lang in PUNC_RANGES
            if re.search(f"[{PUNC_RANGES[lang]}]", text) is not None
        ]
    )
    print(
        "Text language(s):", [
            lang
            for lang in TEXT_RANGES
            if re.search(f"[{TEXT_RANGES[lang]}]", text) is not None
        ]
    )

    all_conditions = "\u000a" + "".join(
        [PUNC_RANGES[lang] for lang in PUNC_RANGES] +
        [TEXT_RANGES[lang] for lang in TEXT_RANGES]
    )
    unknown_chars = re.findall(f"[^{all_conditions}]", text)

    if len(unknown_chars) > 0:
        concated_chars = sorted(set("".join(unknown_chars)))
        print("Detected unlisted characters.")
        print("Unknown characters:", f"'{concated_chars}'")
        # If this displays nothing visible, then you should be very afraid...


def detect_issues(text: str) -> None:
    print(
        "Possible violations:", [
            flag
            for flag in WARNING_RANGES
            if re.search(f"[{WARNING_RANGES[flag]}]", text) is not None
        ]
    )


def detect_formatting(text: str) -> None:
    # Mainly useful if copypasting text
    if text.startswith("\n") or text.endswith("\n"):
        print("Detected start/end newline.")

    if "\n\n\n" in text:  # Assumes no \r
        print("Detected double newlines (after text).")

    if " " in text or "\u3000" in text:
        print("Detected spaces.")


def to_half_latin(text: str) -> str:
    # Only maps if direct ASCII match
    mapping = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
    mapping[0x3000] = 0x20  # CJK space is actually part of the punc block
    return text.translate(mapping)
    # Derived from: https://stackoverflow.com/questions/2422177/python-how-can-i-replace-full-width-characters-with-half-width-characters


def to_full_latin(text: str) -> str:
    # NOTE: Cannot map to chars like double bracket quotes
    mapping = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
    mapping[0x20] = 0x3000
    return text.translate(mapping)


if __name__ == "__main__":
    text = open(INPUT_FILENAME, "r", encoding="utf-8").read()

    # Detect-only
    print("Checking language...")
    detect_language(text)
    print("\nChecking for major issues...")
    detect_issues(text)
    print("\nChecking formatting...")
    detect_formatting(text)

    # Transpose
    # edited_text = text
    # edited_text = to_half_latin(edited_text)  # Imperfect handling for punc
    # might trim lines of invis chars at a later stage

    # with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
    #     f.write(edited_text)
    # print(f"\nWrote proposed changes to {OUTPUT_FILENAME}.")
