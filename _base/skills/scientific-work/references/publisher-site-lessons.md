# Publisher Site Lessons

Use this file for compact reusable lessons from publisher, DOI, repository, and literature-hosting sites. Keep entries practical: site, symptom, route, what worked, and what to avoid. Do not store credentials, cookies, session tokens, personal data, or one-off private state.

## General Rules

- Before downloading from a publisher page, search the vault for an existing PDF by DOI, DOI-safe fragment, DOI suffix, year, and stable title words. Existing filenames may contain truncated, corrected, translated, or slightly wrong titles.
- If an existing valid PDF is found, update the project manifest/checkpoint with the local path instead of creating a duplicate. Treat DOI and DOI-suffix matches as strong; treat title-only matches as candidates that need manual confirmation, especially for families of papers with similar PCM/plasmonics titles.
- When deduplicating by year, match the year against the PDF filename or the immediate paper-folder name, not the whole absolute path. Project folders can contain unrelated years such as `article_2026` and create false confidence for older papers.
- If a publisher page blocks script-based PDF access with 403 or a bot/security check, do not immediately mark the paper unavailable. Try the in-app browser and, when needed, let the user complete institutional login or browser verification in the visible UI.
- When a CAPTCHA/security-check page appears, first try one or two ordinary page reloads or the same legitimate route again, without clicking or solving the CAPTCHA itself. If the blocker persists after those attempts, tell the user to complete the human verification manually in the visible browser.
- When a new site-specific route is learned, append a short note here after the session.

## AIP Publishing

- `pubs.aip.org` may show a Cloudflare/security verification page before the real article page or institutional-login flow. Treat this as a browser-verification blocker, not as evidence that the university has no access.
- Direct AIP PDF URLs discovered through metadata can return HTTP 403 to shell downloaders even when the article page is reachable in a browser. Before spending time on browser login, run the duplicate-PDF check because older AIP papers may already exist in the vault under year-title filenames.

## Optica Publishing Group

- Optica pages often resolve to `opg.optica.org/.../abstract.cfm?uri=...`. Check the article page for PDF/View Media and institutional-login controls before marking a DOI unavailable.
- For Optica EIM/waveguide papers, keep the DOI and `uri` value in the checkpoint; page titles and metadata can be less stable than the DOI.
- `PDF Article` links usually point to `viewmedia.cfm?uri=...&seq=0`. A first shell request may return a small HTML redirect to `/viewmedia.cfm?r=1&rwjcode=...`; following that redirect from shell can trigger a Radware Captcha page. Treat this as a browser/security-gate state. Continue in the visible in-app browser and let the user complete verification or institutional login; do not mark the PDF as unavailable only from this shell result.
- The Optica `Institutional Login` link can route to OpenAthens Wayfinder. In Russian locale the page may show `Найти ваше учреждение` ("Find your institution"). Leave this step to the user in the visible browser; after they complete SSO, return to the article/PDF URL and retry the download in the authenticated session.
- If OpenAthens Wayfinder reports `No matching institution found` after abbreviation, full English/Russian name, and email-domain searches, stop trying variants and check the institution library's full-text databases, discovery search, proxy/VPN instructions, or librarian contact path. Record the institution-access route separately from the publisher-access status.

## PubMed Central And EuropePMC

- If an article has a PMCID, NCBI/PMC direct PDF URLs may still return a Google reCAPTCHA page to shell clients. Before marking the PDF unavailable, try the EuropePMC renderer route `https://europepmc.org/articles/PMCxxxxxxx?pdf=render`; it can return a valid official OA `%PDF` when NCBI and publisher PDF endpoints block automated requests.

## ResearchGate

- ResearchGate pages may expose author-provided full text in search snippets or metadata, but browser access can stop at a `Security check required` page and shell download can return HTTP 403. Treat this as an author-provided PDF candidate, not as downloaded full text. Continue only through visible browser verification or ask the user to download manually; do not mark it as read until a valid local `%PDF` file exists.
- ResearchGate can show ordinary cookie/privacy and signup overlays before the PDF controls. These may be dismissed through normal UI controls; they are not CAPTCHA. If the Codex in-app browser cannot save the `Download` response, ask the user to download the visible author PDF manually, then move it from `Downloads/` to the project literature folder, rename it with the DOI-safe pattern, validate `%PDF`, and update manifest/checkpoint.
