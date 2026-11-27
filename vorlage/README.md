# Karussell-Vorlage

Vorlage für Instagram-Karussells (1080 x 1350) im Brand Design System 2.0. Stand: 24.11.2026.

- `vorlage.html`: alle Slide-Typen (dunkel, Foto-Hintergrund, hell, Zahl, Zitat). Überschriften beginnen auf Text-Slides auf derselben Höhe (Klasse `top`).
- Dunkle Slides tragen einen Farbverlauf oben rechts (Midnight Navy zu Navy Surface).
- Foto-Karussell: jede Slide als `photo bottom`, `photo mid` (stärker abgedunkelt) oder `photo full`, mit einem eigenen Foto je Slide.
- Instrument Serif (aufgenommen von Stefan am 27.11.2026): Zitat (`quote`) und Versprechen-Zeile (`promise`) stehen in Instrument Serif Italic. Klasse `em` setzt ein betontes Wort oder eine Wortgruppe in Serife, nie zusammen mit dem Pinselstrich auf derselben Slide.
- Slide 9: betontes Wort in Serife. Slide 10: fremdes Material (`fremd`) mit Quelle unten links (`src`).
- `story.html`: Story-Vorlage 1080 x 1920 mit sechs Typen (Aussage, Zitat, Zahl, Kommentar zu fremdem Material mit Quelle, Foto mit Overlay, helle Story). Oben 250 px und unten 340 px bleiben frei. Rendern wie unten mit `--window-size=1080,1920`.
- `fremd.jpg`: Platzhalter für fremdes Material, wird je Beitrag ersetzt.
- `pinsel.svg`: Pinselstrich in Industrial Magenta für markierte Wörter.
- `logo-weiss.png`, `logo-navy.png`: Logo für die Fußzeile.
- Die Foto-Slides erwarten ein Bild `foto_s.jpg` im selben Ordner. Es liegt nicht im Repository.

## Rendern

```
npm install
google-chrome --headless=new --no-sandbox --hide-scrollbars --allow-file-access-from-files \
  --force-device-scale-factor=1 --window-size=1080,1350 --virtual-time-budget=3000 \
  --screenshot=slide1.png "file://$PWD/vorlage.html#1"
```

Die Zahl hinter `#` wählt die Slide.
