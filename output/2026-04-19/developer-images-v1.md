# דוח Developer — עיבוד תמונות לגלריה

**תאריך:** 2026-04-19
**סוכן:** developer
**סטטוס:** **חסום חלקית** — תשתית + סקריפטים + HTML מוכנים לעבודה. הרצת Python/ffmpeg/ImageMagick נחסמה בסנדבוקס.

---

## TL;DR

- נכתבו **3 סקריפטי Python** עצמאיים (face blur, frame extract, responsive build) וקובץ batch מאחד.
- **index.html עודכן** עם `<picture>` tags מלאים, srcset רספונסיבי, WebP+JPG fallback, `loading="lazy"` לגלריה, `loading="eager"` + `fetchpriority="high"` ל-Hero, ו-`onerror` fallback לתמונות SVG הקיימות (האתר לא נשבר עד הרצת ה-pipeline).
- **5 התמונות שמחייבות טשטוש הועתקו** ל-`website/assets/source-to-blur/`, מוכנות להרצה.
- **לא הופקו קבצי תמונה סופיים** (WebP/JPG) כי הסנדבוקס חסם כל הרצה של Python, powershell, cmd, ffmpeg ו-magick. המשתמש ציין שהסביבה זמינה, אבל בפועל כל `Bash` קריאה לבינארי חיצוני הוחזרה עם "Permission to use Bash has been denied". גם גישת קריאה ל-`C:\Users\Avner\AppData\` נחסמה.
- **צעד הבא:** רימה/אבנר מריצים את `website/scripts/run_pipeline.bat` פעם אחת — ואחרי סינון ידני של ~100 פריימים (שלב 3) — הרצה שנייה. זה ייצר את כל התמונות הסופיות, וה-HTML כבר מוכן לקלוט אותן.

---

## מה נעשה בפועל

### 1. סקריפטי עיבוד — כולם ב-`website/scripts/`

| קובץ | תפקיד | תלות |
|---|---|---|
| `blur_faces.py` | MediaPipe Face Detection (model 0+1, confidence 0.25) → Pixelate 20px על כל פנים עם 25% margin | opencv-python, mediapipe, numpy |
| `extract_frames.py` | ffprobe לזמן → ffmpeg להוצאת פריים ב-25%/50%/75% מכל סרטון | ffmpeg/ffprobe |
| `make_responsive.py` | ImageMagick → 3 רוחבים (480/768/1200) × 2 פורמטים (WebP q85, JPG q82) עם auto-orient + strip | magick |
| `run_pipeline.bat` | קובץ batch שמריץ את כולם בסדר הנכון, עם הפסקה ידנית באמצע לסינון פריימים | — |

הסקריפטים פרמטריזיים, מדפיסים לוג ברור, מדלגים על קבצים שנכשלים בלי להפיל את הרצה.

### 2. תמונות מקור הוכנו לטשטוש

הועתקו ל-`website/assets/source-to-blur/`:
- `IMG-20240801-WA0008.jpg` — 4+ פנים על במה + קהל בצד
- `IMG-20240801-WA0014.jpg` — 3 פנים על במה (קהל כבר מגב)
- `IMG-20240801-WA0034.jpg` — 5 פנים קטנים + קהל רובו מגב
- `IMG-20240801-WA0037.jpg` — 2 פנים בלבד
- `IMG-20240801-WA0038.jpg` — 2 פנים בלבד

**הפורטרט של רימה** (`Screenshot_20240718_131943_WhatsApp.jpg`) **לא הועתק לטשטוש** — יעבור ישירות לשלב ה-responsive תחת שם `hero-rima.jpg`.

### 3. index.html — עודכן מלא

- **Hero:** `<picture>` עם WebP + JPG fallback, 3 רוחבים, `loading="eager"`, `fetchpriority="high"`, alt עברי, `onerror` ל-`hero-placeholder.svg`.
- **Gallery:** 6 `<figure>` (במקום 8) עם `<picture>` מלא, `loading="lazy"`, alt עברי תיאורי מפורט לכל תמונה (מבוסס על תיאורי הוויזואל), `onerror` fallback לקבצי SVG הקיימים.
- **sizes** attribute מותאם: Hero `(max-width: 600px) 100vw, (max-width: 1100px) 60vw, 720px` / Gallery `(max-width: 600px) 100vw, (max-width: 1100px) 50vw, 33vw`.

שמות הקבצים הצפויים (להרצת ה-pipeline):
```
assets/images/hero-rima-{480,768,1200}.{webp,jpg}
assets/images/gallery-{1..6}-{480,768,1200}.{webp,jpg}
```

### 4. OG / Social meta
**לא שונה** — נשאר `assets/hero-placeholder.svg` כי OG scrapers לא מריצים onerror. אחרי שה-pipeline ירוץ, יש להחליף ל-`assets/images/hero-rima-1200.jpg` (TODO ברור — שורה 16, 23 ב-HTML).

---

## חסימה — מה לא עבד

הסנדבוקס של הסשן הנוכחי חוסם:
1. **כל קריאה לבינארי חיצוני** — `python.exe`, `powershell.exe`, `cmd.exe`, `magick`, `ffmpeg` — כולם מחזירים `Permission to use Bash has been denied`.
2. **כל גישה ל-`/c/Users/Avner/AppData/`** — אפילו `ls` פשוט. נראה שהסנדבוקס תוחם ל-`sipurima/` בלבד.

Glob tool כן מגלה את `python.exe` בנתיב הנכון, ו-`Bash echo/ls` בתוך `sipurima/` עובד. זה מעיד שהמסנן הוא על exec של בינארים מחוץ ל-workspace, לא על Python ספציפית.

---

## מה שצריך להריץ ידנית

מ-PowerShell או CMD של אבנר/רימה:

```cmd
cd C:\Users\Avner\Documents\sipurima
website\scripts\run_pipeline.bat
```

הסקריפט:
1. מטשטש פנים ב-5 התמונות → `assets/blurred/`.
2. מחלץ ~108 פריימים (36 סרטונים × 3 timestamps) → `assets/frames-raw/`.
3. **עצירה ידנית** — לסנן את הפריימים, לבחור 3–4 טובים (רימה לבד / ילדים מגב / תקריב אביזר), לשים ב-`assets/selected/` בשמות:
   ```
   hero-rima.jpg                    # העתק של Screenshot_20240718_131943_WhatsApp.jpg
   gallery-1.jpg .. gallery-5.jpg   # 5 תמונות הגלריה המטושטשות מ-assets/blurred/ בסדר הנכון
   gallery-6.jpg                    # פריים מסרטון שנבחר
   ```
4. הרצה שנייה של ה-batch (או רק `make_responsive.py`) → `assets/images/` עם כל הגדלים.

**הסדר המומלץ לגלריה (לפי v2):**
1. `IMG-20240801-WA0014-blurred` (רימה + ילד יושב)
2. `IMG-20240801-WA0008-blurred` (הצגה בקהל מלא)
3. `IMG-20240801-WA0037-blurred` (תקריב תחפושות)
4. `IMG-20240801-WA0038-blurred` (וריאציה צבעונית)
5. `IMG-20240801-WA0034-blurred` (תמונה מעמדית)
6. פריים נבחר מסרטון

---

## אומדן משקלי קבצים (יעד)

| קובץ | צפוי (KB) | יעד |
|---|---|---|
| hero-rima-1200.webp | 120–180 | < 250 ✓ |
| hero-rima-768.webp | 55–85 | < 250 ✓ |
| hero-rima-480.webp | 25–40 | < 250 ✓ |
| gallery-N-1200.webp | 80–130 | < 150 ✓ |
| gallery-N-768.webp | 40–70 | < 150 ✓ |
| gallery-N-480.webp | 18–30 | < 150 ✓ |

JPG fallbacks ~20-30% כבדים יותר אבל עדיין בטווח.

---

## Bearing על index.html

- **לפני:** 8 `<img src="*.svg">` + 1 `<img src="hero-placeholder.svg">`.
- **אחרי:** 6 `<picture>` בגלריה + 1 `<picture>` ב-hero. כל אחד עם WebP+JPG srcset רספונסיבי + `onerror` ל-SVG.
- **תאימות:** `<picture>` תומך ב-100% דפדפנים מודרניים; `onerror` מכסה מצב שהקבצים עוד לא הופקו.
- **ביצועים:** Hero eager + fetchpriority=high → LCP מיטבי. Gallery lazy → לא טוענת עד scroll. srcset מטען תמיד את הגודל הקרוב למסך.
- **נגישות:** כל alt עברי תיאורי (לא "תמונה 1").

---

## דברים ש-QA צריך לבדוק

1. **אחרי הרצת הסקריפט** — האם MediaPipe תפס את כל הפנים? (במיוחד ב-`IMG-20240801-WA0008.jpg` שיש קהל בצד — אם פספס, להגביר margin ל-0.35 או להוריד min-conf ל-0.2).
2. איכות ויזואלית של הפיקסליישן (20px) — האם נראה מכוון עיצובית? אם גרגירי-מדי: להקטין ל-15px. אם לא מספיק מטשטש: להגדיל ל-25px.
3. כל קבצי ה-WebP קטנים מ-150KB (גלריה) / 250KB (hero)?
4. האם כל 6 התמונות בגלריה מסונכרנות עם ה-alt שב-HTML?

---

## קבצים שהושפעו

נוצרו:
- `C:\Users\Avner\Documents\sipurima\website\scripts\blur_faces.py`
- `C:\Users\Avner\Documents\sipurima\website\scripts\extract_frames.py`
- `C:\Users\Avner\Documents\sipurima\website\scripts\make_responsive.py`
- `C:\Users\Avner\Documents\sipurima\website\scripts\run_pipeline.bat`
- `C:\Users\Avner\Documents\sipurima\website\assets\source-to-blur\` (5 תמונות)
- `C:\Users\Avner\Documents\sipurima\website\assets\blurred\` (ריק, ימולא ע"י הסקריפט)
- `C:\Users\Avner\Documents\sipurima\website\assets\frames-raw\` (ריק)
- `C:\Users\Avner\Documents\sipurima\website\assets\images\` (ריק, יעד סופי)

שונה:
- `C:\Users\Avner\Documents\sipurima\website\index.html` — Hero + Gallery sections.

---

*הוכן על ידי developer · לאישור QA → CEO · 2026-04-19*
