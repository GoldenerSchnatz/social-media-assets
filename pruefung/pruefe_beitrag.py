#!/usr/bin/env python3
"""Mechanische Prüfung eines Beitragsentwurfs nach den Regeln von Stefan Schnatz.

Aufruf: python3 pruefe_beitrag.py entwurf.txt [--typ linkedin|caption|slide|kommentar|antwort]
Gibt Befunde (Regelverstoß) und Hinweise (bitte prüfen) aus. Keine Punktzahl.
Nur Standardbibliothek, kein Netzwerk, schreibt keine Dateien.
"""
import json, re, statistics, sys, unicodedata
from pathlib import Path

R = json.loads((Path(__file__).parent / "regeln.json").read_text(encoding="utf-8"))
ZAHLWORT = r"\b(zwei|drei|vier|fünf|sechs|sieben|acht|neun|zehn|elf|zwölf|zwanzig|dreißig|hundert|tausend)\b"

def saetze(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", t) if len(s.strip().split()) >= 2]

def pruefe(text, typ="linkedin"):
    befunde, hinweise = [], []
    zeilen = [z for z in text.split("\n")]
    absaetze = [a.strip() for a in re.split(r"\n\s*\n", text) if a.strip()]

    unsichtbar = [c for c in text if unicodedata.category(c) == "Cf" or c in "­  "]
    if unsichtbar:
        befunde.append(f"{len(unsichtbar)} unsichtbare oder Sonder-Leerzeichen im Text")
    if re.search(r"[—]|\s[–-]\s", text):
        befunde.append("Gedankenstrich im Text: " + ", ".join(repr(m.group(0)) for m in re.finditer(r"\S*\s?[—]\s?\S*|\S+\s[–-]\s\S+", text))[:160])
    if re.search(r"(?<!\w)#\w", text):
        befunde.append("Hashtag im Text")
    if any(0x1D400 <= ord(c) <= 0x1D7FF for c in text):
        befunde.append("Unicode-Fett- oder Kursivschrift")
    emojis = [c for c in text if unicodedata.category(c) == "So" or 0x1F300 <= ord(c) <= 0x1FAFF]
    if len(emojis) > 2:
        hinweise.append(f"{len(emojis)} Emojis, Standard sind keine oder wenige")

    for w in R["verbotene_woerter"]:
        if re.search(r"(?<!\w)" + re.escape(w), text, re.I):
            befunde.append(f"Verbotenes Wort: „{w}“")
    for s in saetze(text) + absaetze:
        for a in R["verbotene_satzanfaenge"]:
            if s.lower().startswith(a.lower()):
                befunde.append(f"Verbotener Satzanfang: „{a}“")
    befunde = list(dict.fromkeys(befunde))

    if re.search(r"\b[Nn]icht\b[^.!?\n]{0,90}[.,]\s*[Ss]ondern\b", text) or re.search(r"\bnicht nur\b[^.!?\n]{0,90}\bsondern\b", text, re.I):
        befunde.append("Muster „Nicht X. Sondern Y.“")

    for m in re.finditer(r":[ \t]+([a-zäöü]\w*)", text):
        vor = text[max(0, m.start() - 6):m.start()]
        if not re.search(r"https?$|\d$", vor):
            befunde.append(f"Nach Doppelpunkt klein: „: {m.group(1)}“")
    for m in re.finditer(r"\b(Du|Dir|Dich|Dein\w*|Euch|Euer\w*)\b", text):
        davor = text[:m.start()].rstrip(" \t")
        if davor and davor[-1] not in ".!?:\n»„\"":
            befunde.append(f"Anrede groß geschrieben: „{m.group(1)}“")

    dreier = re.findall(r"([^,.!?:\n]{2,45}), ([^,.!?:\n]{2,45}) und ([^,.!?:\n]{2,45})[.!?]", text)
    dreier += re.findall(r"(?:^|\n|[.!?] )([^,.!?\n]{2,30}), ([^,.!?\n]{2,30}), ([^,.!?\n]{2,30})\.", text)
    if dreier:
        hinweise.append(f"{len(dreier)} Dreierliste(n), Beispiel: „{', '.join(x.strip() for x in dreier[0])[:90]}“")

    ein_satz = [a for a in absaetze if len(saetze(a)) <= 1]
    if len(absaetze) >= 4 and len(ein_satz) / len(absaetze) > 0.5:
        hinweise.append(f"{len(ein_satz)} von {len(absaetze)} Absätzen haben nur einen Satz")
    laengen = [len(s.split()) for s in saetze(text)]
    if len(laengen) >= 6 and statistics.pstdev(laengen) / statistics.mean(laengen) < 0.35:
        hinweise.append("Satzlängen sehr gleichförmig")
    if typ in ("kommentar", "antwort"):
        start = text.strip()
        for e in R["kommentar_einstiege"]:
            if start.lower().startswith(e.lower()):
                befunde.append(f"Floskel als Einstieg: „{e}“")
        if start and (unicodedata.category(start[0]) == "So" or 0x1F300 <= ord(start[0]) <= 0x1FAFF):
            befunde.append("Emoji als erstes Zeichen")
        if re.match(r"^[A-ZÄÖÜ][\wäöüß-]+!", start):
            befunde.append("Vorname mit Ausrufezeichen als Einstieg")
        if typ == "kommentar":
            n = len(re.findall(r"[.!?]+(?:\s|$)", start)) or 1
            lo, hi = R["kommentar_saetze"]
            if not lo <= n <= hi:
                hinweise.append(f"{n} Sätze, Richtwert {lo} bis {hi}")
    elif not re.search(r"\d", text) and not re.search(ZAHLWORT, text, re.I):
        hinweise.append("Keine Zahl im Text: Ist der Beitrag konkret genug?")
    for f in R["reflex_fragen"]:
        if text.rstrip().endswith(f):
            hinweise.append(f"Reflex-Frage am Schluss: „{f}“")

    if typ == "linkedin":
        n = len(text.strip()); lo, hi = R["linkedin_zeichen"]
        if not lo <= n <= hi:
            hinweise.append(f"{n} Zeichen, Zielbereich {lo} bis {hi}")
        erste = next((z.strip() for z in zeilen if z.strip()), "")
        if erste.endswith("?"):
            befunde.append("Erste Zeile ist eine Frage")
        if len(erste) > R["erste_zeile_richtwert"]:
            hinweise.append(f"Erste Zeile hat {len(erste)} Zeichen, Richtwert {R['erste_zeile_richtwert']}")
    return befunde, hinweise

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    typ = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--typ" and i + 1 < len(sys.argv)), "linkedin")
    if not args:
        sys.exit(__doc__)
    text = Path(args[0]).read_text(encoding="utf-8")
    b, h = pruefe(text, typ)
    print(f"{args[0]} ({typ}, {len(text.strip())} Zeichen)")
    print("Befunde:" if b else "Befunde: keine")
    for x in b: print("  -", x)
    print("Hinweise:" if h else "Hinweise: keine")
    for x in h: print("  -", x)
    sys.exit(1 if b else 0)
