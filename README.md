# We, the People — Landingpage

Statische One-Page-Landingpage für „We, the People", ein Projekt der Kontor 4 Projektentwicklung GmbH. Reines HTML/CSS/JS, keine Build-Pipeline, kein Backend, keine Datenbank.

## Struktur

```
/
├── index.html            Hauptseite (One-Pager)
├── impressum.html         Rechtliche Pflichtangaben (Platzhalter, s. u.)
├── datenschutz.html       Datenschutzerklärung (Platzhalter, s. u.)
├── robots.txt
├── sitemap.xml
├── site.webmanifest
├── assets/
│   ├── css/style.css      Gesamtes Styling (ein File, keine Frameworks)
│   ├── js/main.js         Navigation, Scroll-Reveal, Web3Forms-Anbindung
│   ├── fonts/             (aktuell ungenutzt, s. „Google Fonts" unten)
│   └── img/
│       ├── favicon.svg / favicon-32.png / apple-touch-icon.png
│       ├── icon-192.png / icon-512.png
│       └── og-image.png   Social-Sharing-Bild (1200×630)
└── scripts/gen_assets.py  Python-Skript, mit dem Icon/Favicons/OG-Bild aus der
                            Logo-Geometrie generiert wurden (nur für spätere Anpassungen nötig)
```

## Vor dem Live-Schalten: drei offene Punkte

### 1. Web3Forms Access Key eintragen

Das Kontaktformular (`#kontakt` in `index.html`) postet an `https://api.web3forms.com/submit`, aktuell mit einem Platzhalter:

```html
<input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
```

1. Auf [web3forms.com](https://web3forms.com) mit `kontakt@kontor.eu.com` (oder der finalen Zieladresse) einen kostenlosen Access Key erzeugen.
2. Platzhalter in `index.html` durch den echten Key ersetzen.
3. Das Formular sendet per `fetch` als JSON an Web3Forms (in `assets/js/main.js`); solange der Platzhalter drinsteht, verhindert das Script bewusst den Versand und zeigt eine Fehlermeldung, damit keine Testdaten ins Leere laufen.
4. Enthält bereits ein verstecktes Honeypot-Feld (`botcheck`) gegen Bot-Spam.

### 2. Rechtstexte vervollständigen

`impressum.html` und `datenschutz.html` enthalten türkis hervorgehobene Platzhalter (Anschrift, Registergericht, HRB-Nummer, USt-IdNr., Auftragsverarbeiter-Angaben zu Web3Forms/bunny.net etc.). Diese sind rechtlich verbindliche Angaben — bitte von der Geschäftsführung / Rechtsberatung final befüllen und prüfen lassen, insbesondere:

- Vollständige Anschrift und Registerdaten der Kontor 4 Projektentwicklung GmbH
- AVV-Status und Serverstandort von Web3Forms und bunny.net
- Aufbewahrungsfrist für Kontaktanfragen

### 3. Google Fonts — Empfehlung

Aus dieser Umgebung heraus war kein Zugriff auf `fonts.googleapis.com` bzw. die npm-Registry möglich, um „Fraunces" und „Inter" lokal einzubetten. Die Seite lädt die Schriften daher aktuell per `<link>`-Tag von Google-Servern (Standardverfahren, in `datenschutz.html` entsprechend dokumentiert). Für maximale Kontrolle über Ladezeit und Datenschutz empfiehlt sich, die woff2-Dateien (z. B. via `npm i @fontsource/inter @fontsource/fraunces` oder direkt von [fonts.google.com](https://fonts.google.com)) in `assets/fonts/` abzulegen und per `@font-face` in `assets/css/style.css` einzubinden statt der Google-CDN-Links im `<head>`. Sag Bescheid, dann übernehme ich das beim nächsten Durchgang.

## Deployment — GitHub + bunny.net

1. **Repository anlegen:** Diesen Ordner in ein neues GitHub-Repo pushen (z. B. `we-the-people-web`).
2. **bunny.net Storage Zone:** Im bunny.net-Dashboard eine Storage Zone anlegen, darauf eine Pull Zone bzw. direkt „bunny.net Edge Storage + CDN" für statisches Hosting verbinden.
3. **Auto-Deploy aus GitHub:** bunny.net bietet eine Git-Integration (bzw. GitHub Actions lassen sich alternativ nutzen, um bei jedem Push den Ordnerinhalt per FTP/API in die Storage Zone zu synchronisieren).
4. **Domain verbinden:** `www.projectppl.com` als Custom Hostname auf die bunny.net Pull Zone legen, SSL-Zertifikat (Let's Encrypt, automatisch über bunny.net) aktivieren, DNS-CNAME beim Domain-Registrar setzen.
5. **Root-Redirect:** `projectppl.com` (ohne www) auf `www.projectppl.com` weiterleiten (301), je nach Registrar/DNS-Anbieter.

→ Ich unterstütze dich gerne direkt beim Einrichten von Repo, bunny.net-Konfiguration und DNS, sobald du so weit bist.

## Technische Hinweise

- **Keine Abhängigkeiten** außer optional Google Fonts (siehe oben). Kein Build-Schritt nötig.
- **Barrierefreiheit:** Skip-Link, semantisches HTML, sichtbare Fokus-Zustände, `aria-label`/`aria-live` an den relevanten Stellen, `prefers-reduced-motion` wird respektiert (alle Animationen werden dann deaktiviert bzw. Endzustand sofort gezeigt).
- **Performance:** ein CSS-File, ein JS-File, keine Bild-Hero, System-naher Font-Stack als Fallback.
- **SEO:** Title/Description, OpenGraph- und Twitter-Card-Metadaten, `sitemap.xml`, `robots.txt`, JSON-LD (`Organization`) in `index.html`.
