# Karussell-Vorlage

Vorlage für Instagram-Karussells (1080 x 1350) im Brand Design System 2.0. Stand: 24.11.2026.

- `vorlage.html`: alle Slide-Typen (dunkel, Foto-Hintergrund, hell, Zahl, Zitat). Überschriften beginnen auf Text-Slides auf derselben Höhe (Klasse `top`).
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
