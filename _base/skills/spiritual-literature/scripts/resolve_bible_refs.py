#!/usr/bin/env python3
"""Resolve Bible references in a Markdown file against the local Synodal Bible.

Reads <input.md>, finds every reference matching the Synodal book abbreviations
(including common synonyms), verifies each chapter/verse against the vault at
`<VAULT>/Церковь/Библия/Библия/<testament>/<canon>/<canon> Глава <N>.md`, and
rewrites the file in place, replacing each match with an Obsidian wiki-link:

    (2Тим. 2:2)  ->  ([[2 Тим Глава 2#2:2|2 Тим 2:2]])

A JSON report of resolved/unresolved refs is written next to the input as
<input>.bible-refs.json.

Usage:
    python resolve_bible_refs.py <input.md> <vault_root>
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Abbreviation table — canonical folder name -> (testament, list of synonyms)
# Synonyms are matched case-insensitively, dots ignored, whitespace collapsed.
# Longer synonyms are checked first so "Иоан" doesn't shadow "1 Иоан".
# ---------------------------------------------------------------------------

NT = "Новый завет"
OT = "Ветхий завет"

BOOKS: list[tuple[str, str, list[str]]] = [
    # (canon, testament, synonyms)
    # New Testament
    ("Мф",     NT, ["Мф", "Матф", "Мат", "Матфея", "От Матфея", "Ев Матфея"]),
    ("Мк",     NT, ["Мк", "Марк", "Мар", "Марка", "От Марка", "Ев Марка"]),
    ("Лк",     NT, ["Лк", "Лук", "Луки", "От Луки", "Ев Луки"]),
    ("Ин",     NT, ["Ин", "Иоан", "Иоанна", "От Иоанна", "Ев Иоанна"]),
    ("Деян",   NT, ["Деян", "Деяния"]),
    ("Иак",    NT, ["Иак", "Иакова"]),
    ("1 Пет",  NT, ["1 Пет", "1Пет", "1-е Петра", "1 Петра", "Первое Петра"]),
    ("2 Пет",  NT, ["2 Пет", "2Пет", "2-е Петра", "2 Петра", "Второе Петра"]),
    ("1 Ин",   NT, ["1 Ин", "1Ин", "1 Иоан", "1Иоан", "1-е Иоанна", "1 Иоанна", "Первое Иоанна"]),
    ("2 Ин",   NT, ["2 Ин", "2Ин", "2 Иоан", "2Иоан", "2-е Иоанна", "2 Иоанна", "Второе Иоанна"]),
    ("3 Ин",   NT, ["3 Ин", "3Ин", "3 Иоан", "3Иоан", "3-е Иоанна", "3 Иоанна", "Третье Иоанна"]),
    ("Иуд",    NT, ["Иуд", "Иуды"]),
    ("Рим",    NT, ["Рим", "Римлянам", "К Римлянам"]),
    ("1 Кор",  NT, ["1 Кор", "1Кор", "1-е Кор", "1-е Коринфянам", "1 Коринфянам", "Первое Коринфянам"]),
    ("2 Кор",  NT, ["2 Кор", "2Кор", "2-е Кор", "2-е Коринфянам", "2 Коринфянам", "Второе Коринфянам"]),
    ("Гал",    NT, ["Гал", "Галатам", "К Галатам"]),
    ("Еф",     NT, ["Еф", "Ефесянам", "К Ефесянам"]),
    ("Флп",    NT, ["Флп", "Фил", "Филиппийцам", "К Филиппийцам"]),
    ("Кол",    NT, ["Кол", "Колоссянам", "К Колоссянам"]),
    ("1 Фес",  NT, ["1 Фес", "1Фес", "1 Сол", "1Сол", "1-е Фессалоникийцам", "1-е Солунянам", "1 Фессалоникийцам"]),
    ("2 Фес",  NT, ["2 Фес", "2Фес", "2 Сол", "2Сол", "2-е Фессалоникийцам", "2-е Солунянам", "2 Фессалоникийцам"]),
    ("1 Тим",  NT, ["1 Тим", "1Тим", "1-е Тимофею", "1 Тимофею", "Первое Тимофею"]),
    ("2 Тим",  NT, ["2 Тим", "2Тим", "2-е Тимофею", "2 Тимофею", "Второе Тимофею"]),
    ("Тит",    NT, ["Тит", "Титу", "К Титу"]),
    ("Флм",    NT, ["Флм", "Филим", "Филимону", "К Филимону"]),
    ("Евр",    NT, ["Евр", "Евреям", "К Евреям"]),
    ("Откр",   NT, ["Откр", "Отк", "Апок", "Апокалипсис", "Откровение", "Откровение Иоанна"]),
    # Old Testament
    ("Быт",    OT, ["Быт", "Бытие"]),
    ("Исх",    OT, ["Исх", "Исход"]),
    ("Лев",    OT, ["Лев", "Левит"]),
    ("Чис",    OT, ["Чис", "Числ", "Числа"]),
    ("Втор",   OT, ["Втор", "Второзаконие"]),
    ("Нав",    OT, ["Нав", "Иис Нав", "Иисуса Навина"]),
    ("Суд",    OT, ["Суд", "Судей", "Судьи"]),
    ("Руф",    OT, ["Руф", "Руфь", "Руфи"]),
    ("1 Цар",  OT, ["1 Цар", "1Цар", "1-я Царств", "Первая Царств"]),
    ("2 Цар",  OT, ["2 Цар", "2Цар", "2-я Царств", "Вторая Царств"]),
    ("3 Цар",  OT, ["3 Цар", "3Цар", "3-я Царств", "Третья Царств"]),
    ("4 Цар",  OT, ["4 Цар", "4Цар", "4-я Царств", "Четвёртая Царств"]),
    ("1 Пар",  OT, ["1 Пар", "1Пар", "1-я Паралипоменон", "Первая Паралипоменон"]),
    ("2 Пар",  OT, ["2 Пар", "2Пар", "2-я Паралипоменон", "Вторая Паралипоменон"]),
    ("Ездр",   OT, ["Ездр", "Езд", "Ездры"]),
    ("Неем",   OT, ["Неем", "Неемии"]),
    ("Есф",    OT, ["Есф", "Есфирь", "Есфири"]),
    ("Иов",    OT, ["Иов", "Иова"]),
    ("Пс",     OT, ["Пс", "Псал", "Псалом", "Псалтирь"]),
    ("Пр",     OT, ["Пр", "Притч", "Прит", "Притчи", "Притчей"]),
    ("Еккл",   OT, ["Еккл", "Екк", "Екклесиаст", "Экклезиаст"]),
    ("Песн",   OT, ["Песн", "Песнь Песней", "П Песн"]),
    ("Ис",     OT, ["Ис", "Исаия", "Исайя", "Исаии"]),
    ("Иер",    OT, ["Иер", "Иеремия", "Иеремии"]),
    ("Плач",   OT, ["Плач", "Плач Иер", "Плач Иеремии"]),
    ("Иез",    OT, ["Иез", "Иезекииль", "Иезекииля"]),
    ("Дан",    OT, ["Дан", "Даниил", "Даниила"]),
    ("Ос",     OT, ["Ос", "Осия", "Осии"]),
    ("Иоил",   OT, ["Иоил", "Иоиль", "Иоиля"]),
    ("Ам",     OT, ["Ам", "Амос", "Амоса"]),
    ("Авд",    OT, ["Авд", "Авдий", "Авдия"]),
    ("Ион",    OT, ["Ион", "Иона", "Ионы"]),
    ("Мих",    OT, ["Мих", "Михей", "Михея"]),
    ("Наум",   OT, ["Наум", "Наума"]),
    ("Авв",    OT, ["Авв", "Аввакум", "Аввакума"]),
    ("Соф",    OT, ["Соф", "Софония", "Софонии"]),
    ("Агг",    OT, ["Агг", "Аггей", "Аггея"]),
    ("Зах",    OT, ["Зах", "Захария", "Захарии"]),
    ("Мал",    OT, ["Мал", "Малахия", "Малахии"]),
    # Deuterocanonical
    ("Товит",  OT, ["Товит", "Тов", "Товита"]),
    ("Иудифь", OT, ["Иудифь", "Иудифи"]),
    ("Прем",   OT, ["Прем", "Прем Сол", "Премудрости Соломона"]),
    ("Сирах",  OT, ["Сирах", "Сир", "Сираха"]),
    ("Вар",    OT, ["Вар", "Варух", "Варуха"]),
    ("ПослИер",OT, ["ПослИер", "Посл Иер", "Послание Иеремии"]),
    ("1 Мак",  OT, ["1 Мак", "1Мак", "1-я Маккавейская"]),
    ("2 Мак",  OT, ["2 Мак", "2Мак", "2-я Маккавейская"]),
    ("3 Мак",  OT, ["3 Мак", "3Мак", "3-я Маккавейская"]),
    ("2 Ездр", OT, ["2 Ездр", "2Ездр", "2-я Ездры", "Вторая Ездры"]),
    ("3 Ездр", OT, ["3 Ездр", "3Ездр", "3-я Ездры", "Третья Ездры"]),
]


def norm_key(s: str) -> str:
    """Normalize a book synonym for matching: lowercase, no dots, spaces collapsed."""
    return re.sub(r"\s+", " ", s.replace(".", "").strip()).casefold()


# synonym -> (canon, testament); longer synonyms sorted first
SYNONYM_TO_CANON: dict[str, tuple[str, str]] = {}
for canon, testament, syns in BOOKS:
    for s in syns:
        SYNONYM_TO_CANON[norm_key(s)] = (canon, testament)

# All synonym patterns sorted by length descending — longest match wins
SORTED_SYNONYMS = sorted(SYNONYM_TO_CANON.keys(), key=len, reverse=True)

# Regex to detect a book prefix at some position. We escape and join synonyms.
# Between a numeric prefix and the letter part there may be whitespace or none.
# We'll re-parse the matched book text ourselves, so this pattern just captures it.
_book_alt = "|".join(re.escape(s) for s in SORTED_SYNONYMS)
BOOK_RE = re.compile(rf"(?<![\w\-])(?:{_book_alt})\.?", re.IGNORECASE)

# Chapter:verse spec after a book. Colon strictly required between chapter and verse
# (a bare period risks matching "2.0" version numbers). Whitespace inside the spec
# may include newlines (PDF line wraps). Comma-separated continuations accept both
# bare verses ("18") and full chapter:verse ("35:11").
_ws = r"[ \t\r\n]*"
SPEC_RE = re.compile(
    rf"{_ws}(\d{{1,3}}){_ws}:{_ws}"
    rf"(\d{{1,3}}(?:{_ws}[-–—]{_ws}(?:\d{{1,3}}{_ws}:{_ws})?\d{{1,3}})?"
    rf"(?:{_ws},{_ws}\d{{1,3}}(?:{_ws}:{_ws}\d{{1,3}}(?:{_ws}[-–—]{_ws}\d{{1,3}})?"
    rf"|{_ws}[-–—]{_ws}\d{{1,3}})?)*)",
    re.MULTILINE,
)


class VerseIndex:
    """Cache: (canon) -> {chapter_int: set of verse ints}."""

    def __init__(self, vault_root: Path):
        self.vault_root = vault_root
        self.bible_root = vault_root / "Церковь" / "Библия" / "Библия"
        self._cache: dict[str, dict[int, set[int]] | None] = {}
        self._testament_of: dict[str, str] = {c: t for c, t, _ in BOOKS}

    # Book -> chapter-file naming word. Default is "Глава"; Psalms use "Псалом".
    CHAPTER_WORD = {"Пс": "Псалом"}

    def chapter_word(self, canon: str) -> str:
        return self.CHAPTER_WORD.get(canon, "Глава")

    def _load_book(self, canon: str) -> dict[int, set[int]] | None:
        testament = self._testament_of.get(canon)
        if not testament:
            return None
        book_dir = self.bible_root / testament / canon
        if not book_dir.is_dir():
            return None
        word = self.chapter_word(canon)
        book: dict[int, set[int]] = {}
        # Case-insensitive filename match: glob everything, then filter by regex.
        pat = re.compile(rf"^{re.escape(canon)}\s+{re.escape(word)}\s+(\d+)\.md$", re.IGNORECASE)
        for md in book_dir.glob("*.md"):
            m = pat.match(md.name)
            if not m:
                continue
            ch = int(m.group(1))
            verses: set[int] = set()
            try:
                text = md.read_text(encoding="utf-8")
            except Exception:
                continue
            for vm in re.finditer(r"^######\s+(\d+):(\d+)\s*$", text, re.MULTILINE):
                verses.add(int(vm.group(2)))
            book[ch] = verses
        return book

    def get(self, canon: str) -> dict[int, set[int]] | None:
        if canon not in self._cache:
            self._cache[canon] = self._load_book(canon)
        return self._cache[canon]


def match_book(text: str, pos: int) -> tuple[str, str, int, int] | None:
    """At text[pos:], try to match a book synonym. Return (raw, canon, start, end).
    Longest match wins. Case-insensitive. Ignores trailing dot.

    Word-boundary requirements:
      - preceding char must be non-letter (start of file, whitespace, punctuation);
      - following char must be non-letter (avoid matching "-ам" endings, "Иное", etc).
    """
    # Preceding char must be non-letter or start of file.
    if pos > 0 and text[pos - 1].isalpha():
        return None
    # Slice for search — cap to reasonable length
    window = text[pos : pos + 40]
    win_norm_lower = window.casefold()
    for syn in SORTED_SYNONYMS:
        if win_norm_lower.startswith(syn):
            end = pos + len(syn)
            # allow trailing dot to be consumed
            if end < len(text) and text[end] == ".":
                end += 1
            # ensure it doesn't continue into more letters
            if end < len(text) and text[end].isalpha():
                continue
            raw = text[pos:end]
            canon, _ = SYNONYM_TO_CANON[syn]
            return raw, canon, pos, end
    return None


def parse_verse_spec(spec: str) -> list[tuple[int, int]] | None:
    """Parse a spec like '3:16', '3:16-18', '3:16, 18', '3:16-4:2' into
    a list of (chapter, verse) pairs (each verse expanded).
    Returns None if parsing fails.
    """
    spec = spec.strip()
    # Parse chapter and rest
    m = re.match(r"^(\d{1,3})\s*[:\.\s]\s*(.+)$", spec)
    if not m:
        return None
    chapter = int(m.group(1))
    rest = m.group(2).strip()
    pairs: list[tuple[int, int]] = []

    # Split by comma; each part is a verse or range, optionally with own chapter
    for part in re.split(r"\s*,\s*", rest):
        part = part.strip()
        if not part:
            continue
        # Range with explicit new chapter: "4:2"
        rm = re.match(r"^(\d{1,3})\s*[-–—]\s*(\d{1,3})\s*[:\.]\s*(\d{1,3})$", part)
        if rm:
            v_from = int(rm.group(1))
            ch2 = int(rm.group(2))
            v_to = int(rm.group(3))
            # cross-chapter: expand from (chapter, v_from) through end of chapter (unknown),
            # then (ch2, 1..v_to). We don't know chapter length; leave as endpoints.
            pairs.append((chapter, v_from))
            pairs.append((ch2, v_to))
            chapter = ch2
            continue
        # Simple range: "16-18"
        rm2 = re.match(r"^(\d{1,3})\s*[-–—]\s*(\d{1,3})$", part)
        if rm2:
            v_from = int(rm2.group(1))
            v_to = int(rm2.group(2))
            if v_from > v_to:
                return None
            for v in range(v_from, v_to + 1):
                pairs.append((chapter, v))
            continue
        # Single verse: "18"
        rm3 = re.match(r"^(\d{1,3})$", part)
        if rm3:
            pairs.append((chapter, int(rm3.group(1))))
            continue
        # Chapter:verse: "35:11" — same-book new chapter
        rm4 = re.match(r"^(\d{1,3})\s*[:\.]\s*(\d{1,3}(?:\s*[-–—]\s*\d{1,3})?)$", part)
        if rm4:
            new_ch = int(rm4.group(1))
            vspec = rm4.group(2)
            rm4r = re.match(r"^(\d{1,3})\s*[-–—]\s*(\d{1,3})$", vspec)
            if rm4r:
                for v in range(int(rm4r.group(1)), int(rm4r.group(2)) + 1):
                    pairs.append((new_ch, v))
            else:
                pairs.append((new_ch, int(vspec)))
            chapter = new_ch
            continue
        return None
    return pairs if pairs else None


def make_link(canon: str, chapter: int, orig_display: str, chapter_word: str = "Глава") -> str:
    """Build an Obsidian wiki-link that anchors on the first verse of `orig_display`.

    orig_display: the original human-readable ref like "1 Кор 13:4-7" (already canonized book).
    We anchor on the first verse for click-through; display keeps original range.
    """
    m = re.search(r"(\d+)\s*[:\.]\s*(\d+)", orig_display)
    if m:
        ch = m.group(1)
        v = m.group(2)
        return f"[[{canon} {chapter_word} {ch}#{ch}:{v}|{orig_display}]]"
    return f"[[{canon} {chapter_word} {chapter}|{orig_display}]]"


def find_and_resolve(text: str, index: VerseIndex) -> tuple[str, dict]:
    """Walk text left-to-right, find ref clusters, verify, and rewrite.

    A ref cluster starts at a book token and continues while we can consume:
      - a chapter:verse spec, then optional [",", ";", " "] followed by either
        another spec (same book, new chapter or verse) or a new book token.
    We stop when the next token is not a spec or a known book.
    """
    out = []
    i = 0
    stats = {
        "total_book_matches": 0,
        "resolved_refs": 0,
        "unresolved": [],  # {raw, reason}
        "unknown_book": 0,
        "chapter_missing": 0,
        "verse_missing": 0,
        "parse_failed": 0,
    }

    while i < len(text):
        # try match a book at position i
        bm = match_book(text, i)
        if not bm:
            out.append(text[i])
            i += 1
            continue
        raw_book, canon, b_start, b_end = bm
        stats["total_book_matches"] += 1

        # Consume spec after the book
        spec_m = SPEC_RE.match(text, b_end)
        # Post-processing: if the greedy match consumed the numeric prefix of a
        # following numbered book (e.g. "5:1-3, 1Тим." — we grabbed "5:1-3, 1"),
        # trim trailing ", <digits>" so the next book starts fresh. May need multiple passes.
        while spec_m is not None:
            after = text[spec_m.end():spec_m.end() + 4]
            if not (after and re.match(r"[А-Яа-яЁё]", after) and re.search(r",[ \t\r\n]*\d{1,3}$", spec_m.group(0))):
                break
            shorter = re.sub(r",[ \t\r\n]*\d{1,3}$", "", spec_m.group(0))
            # Re-match against text with an endpos cap so positions stay text-absolute.
            spec_m = SPEC_RE.match(text, b_end, endpos=b_end + len(shorter))
            if spec_m is None:
                break
        if not spec_m:
            # not a real ref (book name mentioned in prose)
            out.append(text[i:b_end])
            i = b_end
            continue

        spec_text = spec_m.group(0)
        chapter_str = spec_m.group(1)
        vspec_str = re.sub(r"\s+", "", spec_m.group(2))  # strip all internal whitespace (incl. newlines)
        try:
            chapter = int(chapter_str)
        except ValueError:
            out.append(text[i:spec_m.end()])
            i = spec_m.end()
            continue

        pairs = parse_verse_spec(f"{chapter}:{vspec_str}")
        if pairs is None:
            stats["parse_failed"] += 1
            stats["unresolved"].append({
                "raw": text[b_start:spec_m.end()],
                "reason": "parse_failed",
            })
            out.append(text[i:spec_m.end()])
            i = spec_m.end()
            continue

        book_verses = index.get(canon)
        if book_verses is None:
            stats["unknown_book"] += 1
            stats["unresolved"].append({
                "raw": text[b_start:spec_m.end()],
                "reason": f"book '{canon}' not found in local repo",
            })
            out.append(text[i:spec_m.end()])
            i = spec_m.end()
            continue

        # Verify every (ch, v) exists
        missing = []
        for ch, v in pairs:
            if ch not in book_verses:
                missing.append((ch, v, "chapter"))
            elif v not in book_verses[ch]:
                missing.append((ch, v, "verse"))

        if missing:
            if any(m[2] == "chapter" for m in missing):
                stats["chapter_missing"] += 1
            else:
                stats["verse_missing"] += 1
            stats["unresolved"].append({
                "raw": text[b_start:spec_m.end()],
                "canon": canon,
                "missing": [f"{ch}:{v} ({kind})" for ch, v, kind in missing],
            })
            out.append(text[i:spec_m.end()])
            i = spec_m.end()
            continue

        # Build display: canon + normalized spec text.
        # vspec_str already has whitespace stripped; add readability spacing back.
        vspec_display = re.sub(r",", ", ", vspec_str)
        display = f"{canon} {chapter}:{vspec_display}"
        link = make_link(canon, chapter, display, index.chapter_word(canon))

        out.append(text[i:b_start])  # any text before the book
        out.append(link)
        stats["resolved_refs"] += 1
        i = spec_m.end()

    return "".join(out), stats


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    input_path = Path(sys.argv[1])
    vault_root = Path(sys.argv[2])
    if not input_path.is_file():
        print(f"Not a file: {input_path}", file=sys.stderr)
        return 1

    text = input_path.read_text(encoding="utf-8")
    index = VerseIndex(vault_root)
    new_text, stats = find_and_resolve(text, index)

    # Write back (in place)
    input_path.write_text(new_text, encoding="utf-8")

    report_path = input_path.with_suffix(input_path.suffix + ".bible-refs.json")
    # Summarise unresolved by reason
    summary = {
        "input": str(input_path),
        "total_book_matches": stats["total_book_matches"],
        "resolved_refs": stats["resolved_refs"],
        "unknown_book_count": stats["unknown_book"],
        "chapter_missing_count": stats["chapter_missing"],
        "verse_missing_count": stats["verse_missing"],
        "parse_failed_count": stats["parse_failed"],
        "unresolved_sample": stats["unresolved"][:50],
        "unresolved_total": len(stats["unresolved"]),
    }
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"resolved: {stats['resolved_refs']}")
    print(f"unresolved: {len(stats['unresolved'])}")
    print(f"report: {report_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
