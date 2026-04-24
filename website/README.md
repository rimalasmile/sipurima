# סיפורימה — אתר v1

אתר דף-אחד (Single Page) של סיפורימה. Vanilla HTML + CSS + JS, ללא תלויות build.

## מבנה

```
website/
├── index.html          כל ה-HTML של הדף היחיד
├── style.css           עיצוב — Mobile-first, RTL
├── script.js           כפתור וואטסאפ צף + טופס + מעקב
├── assets/
│   ├── logo.png        הלוגו הזמני
│   ├── hero-placeholder.svg
│   └── gallery-1..8.svg  placeholders עד שיגיעו תמונות
└── README.md
```

## הפעלה מקומית

אין צורך בשום build. פתח את `index.html` ישירות בדפדפן, או הרץ שרת סטטי:

```bash
# פייתון 3
cd website
python -m http.server 8080
# לפתוח: http://localhost:8080
```

```bash
# Node (npx)
cd website
npx http-server -p 8080
```

## Deploy ל-Netlify

### דרך ממשק Drag & Drop (הכי מהיר):
1. להיכנס ל-https://app.netlify.com/drop
2. לגרור את התיקייה `website/` כולה לתוך הדף.
3. Netlify מעלה ונותן כתובת `*.netlify.app`.
4. לשנות שם תת-דומיין דרך Site settings → Domain.

### דרך CLI:
```bash
npm install -g netlify-cli
cd website
netlify deploy --prod
```

### חיבור דומיין מותאם (sipurima.co.il וכו'):
Domain settings → Add custom domain → עדכון רשומות DNS לפי הוראות Netlify.

## מה דורש החלפה (placeholders)

- `assets/logo.png` — לוגו זמני, מחכים לוגו סופי
- `assets/hero-placeholder.svg` — תמונת Hero — להחליף ב-JPG/WebP אמיתי (1200×800)
- `assets/gallery-1..8.svg` — 8 תמונות גלריה — להחליף ב-JPG/WebP (600×600 לפחות)
- טקסט "מי אני" — ממתין מרימה
- אזור שירות ב-FAQ וב-Footer — `[אזור שירות — ממתין לניסוח]`
- קוד GA4 — פלייסהולדר בתחתית `index.html`, לשלב לאחר קבלת Measurement ID

## שינויים נפוצים

- **לשנות טקסט** — לערוך את `index.html` ישירות. כל סקשן מסומן בהערת HTML.
- **לשנות צבעים** — `:root` בתחילת `style.css`.
- **להוסיף/להחליף תמונת גלריה** — להעלות קובץ לתוך `assets/` ולעדכן את ה-`src` ב-HTML.
- **לעדכן מחיר** — בטבלה בסקשן 5 ב-`index.html`.

## נגישות ו-SEO

- `<html lang="he" dir="rtl">`
- כל התמונות עם `alt`
- כותרות היררכיות (h1 → h2 → h3)
- Schema.org `LocalBusiness + PerformingGroup` משובץ
- Open Graph + Twitter Card
- טופס עם labels ו-`aria-live` להחזרת סטטוס
- מעדיף `prefers-reduced-motion`

## WhatsApp

3 כפתורי WhatsApp עם הודעות מוכנות שונות לפי מקור הקליק, פלוס כפתור צף שמופיע אחרי גלילה של 30%.

מספר היעד: `+972525564136`

אם רוצים לעדכן את המספר — חיפוש-והחלפה של המחרוזת `972525564136` בכל הקבצים.
