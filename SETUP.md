# לעבוד על סיפורימה ממחשב חדש — מדריך מלא (בלי לדלג על שום שלב)

האתר **sipurima.com** מתארח ב-Netlify ומתעדכן אוטומטית מ-GitHub.
הקוד כולו נמצא בריפו הפרטי **`rimalasmile/sipurima`**.
כדי לעבוד מכל מחשב — בצעי את השלבים לפי הסדר, פעם אחת בכל מחשב חדש.

---

## שלב 0 — מה צריך להתקין (פעם אחת לכל מחשב)

1. **Git** — https://git-scm.com/downloads (חובה)
2. **GitHub CLI (`gh`)** — https://cli.github.com (הכי קל להתחברות לריפו פרטי)
3. **עורך קוד** — VS Code: https://code.visualstudio.com (מומלץ)
4. **Python** — https://www.python.org/downloads (רק כדי לראות את האתר מקומית; אופציונלי)

> בדיקה שהכל מותקן — פתחי טרמינל והקלידי:
> ```bash
> git --version
> gh --version
> python --version
> ```

---

## שלב 1 — להתחבר ל-GitHub (פעם אחת לכל מחשב)

הריפו **פרטי**, אז חייבים להזדהות:

```bash
gh auth login
```
בחרי: **GitHub.com** → **HTTPS** → **Login with a web browser** → אשרי בדפדפן עם החשבון `rimalasmile`.

---

## שלב 2 — להוריד את הפרויקט (clone)

```bash
git clone https://github.com/rimalasmile/sipurima.git
cd sipurima
```

---

## שלב 3 — להגדיר זהות לקומיטים (פעם אחת בכל מחשב, בתוך התיקייה)

```bash
git config user.name "rimalasmile"
git config user.email "rimalasmile@gmail.com"
```

---

## שלב 4 — לראות את האתר מקומית לפני שמעלים

```bash
cd website
python -m http.server 8000
```
פתחי בדפדפן: **http://localhost:8000**
(לעצור את השרת: `Ctrl+C`. חלופה ב-VS Code: התוסף **Live Server**.)

---

## שלב 5 — לבצע שינוי ולהעלות לאוויר

לאחר ששינית קבצים:
```bash
git add -A
git commit -m "תיאור קצר של השינוי"
git push origin main
```
**זהו.** Netlify מזהה את הדחיפה ל-`main` ומפרסם אוטומטית ל-**https://sipurima.com** תוך 1–2 דקות.
אין שום שלב ידני ב-Netlify.

> לפני שמתחילים לעבוד במחשב שכבר עבדת בו — משכי קודם את העדכונים האחרונים:
> ```bash
> git pull origin main
> ```

---

## מפת הפרויקט (איפה כל דבר)

| תיקייה / קובץ | מה זה |
|---|---|
| `website/` | **האתר עצמו** — זה מה שמתפרסם ל-sipurima.com (הקבצים שגוגל וגולשים רואים) |
| `website/assets/` | תמונות, פונטים, אייקונים, וידאו של האתר החי |
| `brand/` | חומרי מותג ותמונות מקור (לא חלק מהאתר החי) |
| `netlify.toml` | הגדרות Netlify (publish dir, כותרות אבטחה) — לא לגעת בלי צורך |
| `CLAUDE.md`, `STRATEGY.md`, `agents/` | הקשר ותוכן פנימי של הצוות |
| `SETUP.md` | המסמך הזה |

---

## דברים חשובים לדעת

- **דחיפה ל-`main` = פרסום לאתר החי.** אין "טיוטה". מה שדוחפים ל-main עולה לאוויר.
- **הריפו פרטי** — רק החשבון `rimalasmile` יכול לגשת.
- **תעודת SSL / דומיין** — כבר מוגדרים אוטומטית. אין מה לעשות.
- **וידאו מקור כבד** (`brand/from-rima/approved-videos/`) **לא נמצא בגיט** — קבצי וידאו גדולים מדי ל-GitHub. שמרי גיבוי שלהם בענן (Google Drive). תמונות ה-PNG כן נמצאות בגיט.
- **שינוי תוכן יומי/אוטומטי** — לא רלוונטי כאן; האתר סטטי ומתעדכן רק כשדוחפים.

---

## תקלות נפוצות

| בעיה | פתרון |
|---|---|
| `git push` מבקש סיסמה ונכשל | הריצי `gh auth login` שוב (שלב 1) |
| שינוי לא מופיע באתר | חכי 1–2 דק', ואז רענון קשיח בדפדפן: `Ctrl+Shift+R` |
| שינוי לא מופיע אחרי `pull` | ודאי שאת על `main`: `git checkout main` |
| לא רואה את האתר מקומית | ודאי שאת בתוך `website/` כשמריצים את השרת |
