<div dir="rtl">

# Developer — דוח בניית שלד אתר v1

**תאריך:** 2026-04-19
**מאת:** Developer
**מקבל:** QA → CEO
**סטטוס:** שלד מוכן לביקורת ומילוי תוכן

---

## מה נבנה

אתר דף-אחד (Single Page), Hebrew RTL, Mobile-first, Vanilla HTML+CSS+JS ללא build. כל הקבצים תחת `website/`:

```
website/
├── index.html          דף יחיד עם 11 סקשנים
├── style.css           עיצוב בפלטת קורל/צהוב/ירוק/לבנדר/סגול על קרם
├── script.js           וואטסאפ צף אחרי 30% גלילה + טופס + מעקב
├── README.md           הוראות מלאות
└── assets/
    ├── logo.png                         (מ-brand/logo-temp.png)
    ├── hero-placeholder.svg             (1200×800, צריך להחליף)
    └── gallery-1.svg … gallery-8.svg    (600×600, צריך להחליף)
```

**11 סקשנים כפי שאושרו:** Hero → מי אני → איך הקסם קורה → 5 הערכים → הצגות בשיתוף הקהל + תמחור → הצגה פרטית → גלריה → ציטוטי המלצות → FAQ → טופס + CTA → Footer.

**טכנולוגיה:**
- Vanilla בלבד. אין React, אין jQuery, אין Bootstrap, אין npm.
- פונטים Google Fonts עם `font-display: swap` (Assistant לגוף, Rubik לכותרות).
- כל התמונות עם `loading="lazy"` חוץ מה-Hero.
- Schema.org `LocalBusiness + PerformingGroup`, Open Graph, Twitter Card.
- `<!-- GA4 placeholder -->` מוטמע בתחתית `index.html`.

**נגישות:**
- `<html lang="he" dir="rtl">`
- ARIA `aria-labelledby` על כל סקשן
- `aria-live="polite"` על סטטוס הטופס
- focus-visible styling + `prefers-reduced-motion` respect
- כל התמונות עם `alt` תיאורי

**3 כפתורי WhatsApp נפרדים + צף:**
1. **Hero / ראשי + טופס + צף** — "היי רימה, הגעתי מהאתר. אשמח לשמוע פרטים על ההצגות שלך 💛"
2. **סדרות (סקשן 5)** — "היי רימה, אני [תפקיד] ב-[שם הגוף]. מתעניינת בסדרת הצגות לגילאי 4-7. אפשר לדבר?"
3. **הצגה פרטית (סקשן 6)** — "היי רימה, מחפשת הצגה ליום הולדת/אירוע משפחתי לילד/ה בגילאי 4-7. אשמח לשמוע פרטים ולבדוק תאריך."

כולם מפנים ל-`https://wa.me/972525564136?text=...` (text URL-encoded).

**טופס יצירת קשר:** שם, טלפון, סוג אירוע, תאריך. ב-v1 השליחה פותחת `mailto:` אוטומטית (פתרון zero-backend). כשיהיה Netlify Forms / Formspree — להחליף את ההנדלר ב-`script.js`.

---

## מה דורש החלפה (placeholders)

| פריט | איפה | מה להחליף ל- |
|---|---|---|
| לוגו זמני | `assets/logo.png` | לוגו סופי מ-Visual Director |
| תמונת Hero | `assets/hero-placeholder.svg` | JPG/WebP 1200×800 אמיתי |
| 8 תמונות גלריה | `assets/gallery-1.svg`..`8.svg` | JPG/WebP 600×600+ |
| "מי אני" | סקשן 2 ב-`index.html` | טקסט ביו מרימה |
| אזור שירות | סקשן FAQ + Footer | טקסט סופי (כרגע: `[אזור שירות — ממתין לניסוח]`) |
| GA4 | תחתית `index.html` | snippet אחרי קבלת Measurement ID |
| דומיין/email בפוטר | `hello@sipurima.co.il` | כתובת מייל אמיתית כשהדומיין יירכש |

---

## הוראות הפעלה מקומית

אין צורך ב-build. אפשרות 1 — פתיחה ישירה של `website/index.html` בדפדפן.

אפשרות 2 — שרת סטטי מקומי (מומלץ לבדיקת פונטים ו-CORS):

```bash
cd website
python -m http.server 8080
# או: npx http-server -p 8080
```

פתיחה: `http://localhost:8080`

---

## הוראות Deploy ל-Netlify (קצרות)

**הכי מהיר — Drag & Drop:**
1. להיכנס ל-https://app.netlify.com/drop
2. לגרור את תיקיית `website/` לתוך הדפדפן.
3. תוך שניות מקבלים URL זמני מסוג `sipurima-abc123.netlify.app`.
4. ב-Site settings → Domain management → שינוי subdomain + חיבור דומיין מותאם (sipurima.co.il) עם הוראות DNS של Netlify.

**דרך CLI:**
```bash
npm install -g netlify-cli
cd website
netlify deploy --prod
```

**טיפ:** כשנרצה טופס עובד ללא backend — להוסיף `netlify` ו-`data-netlify="true"` לתג ה-`<form>`, ו-Netlify Forms ייקח את זה אוטומטית (ללא שינוי ב-JS חוץ מהסרת `preventDefault`).

---

## בעיות פתוחות / נקודות לתשומת לב

1. **תוכן "מי אני" חסר** — רימה צריכה לכתוב. עד אז מופיע placeholder מסומן.
2. **אזור שירות** — הוחלט להיכנס כ-`[אזור שירות — ממתין לניסוח]` עד שיוחלט. מופיע ב-2 מקומות.
3. **תמונות אמיתיות** — SVG placeholders משרתים בינתיים; QA וו Visual Director יידעו להחליף לפי שם קובץ. מומלץ לשמור 600×600 לגלריה ו-1200×800 ל-Hero כדי לא לשבור את ה-aspect ratios.
4. **טופס ב-v1 פותח `mailto:`** — זה עובד אבל לא אידאלי (דורש לקוח מייל מוגדר). המלצה: בעלייה לאוויר להוסיף Netlify Forms (5 דק' עבודה).
5. **מספר WhatsApp** — מקודד במספר מקומות (4 קישורים + footer). אם משתנה — חיפוש-והחלפה של `972525564136`.
6. **GA4** — placeholder בלבד. ה-JS כבר קורא `window.gtag` על קליקי WhatsApp — ברגע שמטמיעים את ה-snippet, אירועי `click_whatsapp` עם label יתחילו לזרום.
7. **Favicon** — כרגע משתמש ב-`logo.png`; כשיהיה לוגו רשמי מומלץ ליצור favicon מרובה-גדלים.
8. **ביצועים** — לא מדדתי LCP במכשיר אמיתי. להנחה: עם התמונות האמיתיות (במיוחד Hero) להמיר ל-WebP ולהוסיף `<picture>` עם srcset.

---

## צ'ק-ליסט ל-QA

- [ ] כל הטקסטים מתאימים בדיוק לקובץ הסופי מ-`2026-04-19/website-v1-FINAL-for-rima.md`.
- [ ] 3 כפתורי WhatsApp + צף — כולם עם ההודעה הנכונה, פותחים בלשונית חדשה.
- [ ] כפתור צף מופיע רק אחרי 30% גלילה.
- [ ] טופס — validation בסיסי, `mailto:` נפתח.
- [ ] 768px ו-1024px breakpoints נראים נכון.
- [ ] בדיקת iPhone SE (375px) — שום דבר לא גולש.
- [ ] RTL — אייקונים ומיקומים בצד הנכון.
- [ ] Schema.org תקין (Rich Results Test).

---

*Developer, סיפורימה — 2026-04-19*

</div>
