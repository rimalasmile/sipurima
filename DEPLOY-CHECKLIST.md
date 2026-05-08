# Deploy Checklist — Sipurima

Pre-deploy verification for every release. Run through before pushing to production.

## Visual & Functional

- [ ] Open site on mobile (375px) — hero, nav toggle, all sections render correctly
- [ ] Open site on desktop (1280px+) — layout, spacing, grid all correct
- [ ] Test contact form — submit with valid data, verify Netlify receives it
- [ ] Test contact form validation — submit empty, verify error states show
- [ ] Click all nav links — smooth scroll to correct sections
- [ ] Click WhatsApp links — opens wa.me with correct number and message
- [ ] Click email link — opens mailto with correct address
- [ ] Test 404 page — visit /nonexistent, verify custom 404 shows
- [ ] Open/close all FAQ items
- [ ] Test accessibility widget — font size, contrast, grayscale, link highlighting, animation stop
- [ ] Keyboard navigation — Tab through entire page, verify focus states visible
- [ ] Video plays on click, pause works

## Performance & SEO

- [ ] Run Lighthouse (accessibility, SEO, best-practices) — all must be 100
- [ ] Check OG preview — paste URL in https://www.opengraph.xyz/ after deploy
- [ ] Check Twitter preview — paste URL in https://cards-dev.twitter.com/validator
- [ ] Verify sitemap.xml loads at /sitemap.xml
- [ ] Verify robots.txt loads at /robots.txt

## Security

- [ ] Verify headers at https://securityheaders.com — should be A+
- [ ] Verify CSP at https://csp-evaluator.withgoogle.com/
- [ ] Check no console errors in browser DevTools
- [ ] Confirm form honeypot field is hidden (not visible to users)

## DNS & Domain (first deploy only)

- [ ] Add sipurima.com as custom domain in Netlify dashboard
- [ ] Configure DNS: A record → Netlify load balancer IP
- [ ] Configure DNS: CNAME www → sipurima.netlify.app
- [ ] Wait for SSL certificate provisioning (automatic via Let's Encrypt)
- [ ] Verify https://sipurima.com loads
- [ ] Verify https://www.sipurima.com redirects to apex

## Post-Deploy (first deploy only)

- [ ] Register site in Google Search Console (DNS TXT verification)
- [ ] Submit sitemap.xml in Google Search Console
- [ ] Test form submission on production URL
- [ ] Set up UptimeRobot or similar free monitor for https://sipurima.com
- [ ] Enable branch protection on main in GitHub (require PR reviews)
