# Mechanische Prüfung für Beitragsentwürfe

Stand: 27.11.2026 (KI-typische Floskeln und Muster nach dem Wikipedia-Leitfaden „Signs of AI writing“ ergänzt; Grenzwerte LinkedIn: 700 bis 1.300 Zeichen, Obergrenze 1.500, 6 bis 9 Absätze, erste Zeile bis 60 Zeichen und kein Zitat). Eigene Prüfung nach den Regeln von Stefan Schnatz (Voice Standards, Rollen-Anweisung LinkedIn-Redakteur). Angeregt durch den Humanizer des Open-Source-Projekts linkedin-agent-skill, aber neu geschrieben: auf Deutsch, ohne Punktzahl, ohne Umwandlung von Anführungszeichen.

```
python3 pruefe_beitrag.py entwurf.txt --typ linkedin
python3 pruefe_beitrag.py caption.txt --typ caption
```

- Befunde sind Regelverstöße und werden vor der Ausgabe behoben.
- Hinweise werden geprüft und dürfen begründet stehen bleiben (zum Beispiel eine Dreierliste in Stefans eigenem Wortlaut).
- Wörter und Satzanfänge stehen in `regeln.json` und werden dort gepflegt.
- Das Skript nutzt nur die Standardbibliothek, hat keinen Netzwerkzugriff und schreibt keine Dateien.
