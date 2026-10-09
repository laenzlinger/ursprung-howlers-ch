# B&W Chocolate Howlers – Website-Archiv

Statisches Archiv der Original-Website [ursprung.howlers.ch](https://ursprung.howlers.ch).

👉 **[Archiv ansehen](https://laenzlinger.github.io/ursprung-howlers-ch/)**

Aktuelle Website: [www.howlers.ch](https://www.howlers.ch)

## Struktur

- **9 Seiten** (`.shtml`) mit **Server-Side Includes (SSI)** für Header/Footer
- `partials/header.html` — gemeinsamer Header + Navigation
- `partials/footer.html` — gemeinsamer Footer + Active-Nav-Script

## Lokal anschauen

**Python `http.server` unterstützt KEIN SSI** — die Includes werden nicht verarbeitet.

Optionen für lokales Testen mit SSI:

### 1. nginx (empfohlen, entspricht GitHub Pages)
```sh
# nginx.conf minimal
server {
    listen 8080;
    root /path/to/ursprung-howlers-ch;
    ssi on;
    index index.shtml;
}
```
Dann `nginx -c nginx.conf -p .` und http://localhost:8080

### 2. Apache httpd
```sh
# .htaccess
Options +Includes
AddType text/html .shtml
AddOutputFilter INCLUDES .shtml
```
Dann `httpd -f /path/to/httpd.conf` oder MAMP/XAMPP nutzen.

### 3. Node: `ssi-server` (einfach)
```sh
npx ssi-server -p 8000 -r .
```

### 4. Ohne SSI (nur Inhalt prüfen)
```sh
python3 -m http.server 8000
```
→ Öffnet `index.shtml` aber **Header/Footer fehlen** (Includes werden als Kommentare angezeigt).

## Deployment

GitHub Pages (Nginx) hat **SSI standardmässig aktiviert** für `.shtml` Dateien. Einfach pushen — funktioniert out of the box.
