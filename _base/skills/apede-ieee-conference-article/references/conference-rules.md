# IEEE conference paper rules (APEDE) - verified digest

Source: the official template supplied for APEDE,
`PhD/.../plasma_mdm_modulator_article_2026/APEDE/APEDE правила написания статьи.docx`,
which is the **stock IEEE two-column conference template** ("Paper Title,
use style: paper title" / "This electronic document is a live template ...").
The digest below is that template's prescriptions, reorganized as a
checklist. Recheck before an actual submission:
- IEEE templates: https://www.ieee.org/conferences/publishing/templates.html
- APEDE current-year call for papers (page limit, portal, PDF checker).

APEDE = International Conference "Actual Problems of Electron Devices
Engineering" (Saratov). Proceedings go to **IEEE Xplore**, in **English**.

## APEDE-specific verified requirements (checked 2026-06, APEDE-2026)

Beyond the stock IEEE template, APEDE itself requires (verified against the
conference materials in the user's draft notes):

- paper language: **English**;
- volume: **3-8 pages**;
- format: IEEE Word template (this digest);
- submission: through the **conference registration form** on the site;
- **after the reference list, the SAME Word file must contain
  Russian-language metadata**: article title, authors' full names,
  affiliations, and organization name in Russian;
- originality is checked through **IEEE CrossCheck**; non-IEEE formatting is
  grounds for rejection;
- an expert conclusion (экспертное заключение) on open publication may be
  required - confirm with the current call;
- deadlines shift between editions and are often extended - always compare
  against today's date and recheck the live site.

Official sources (recheck every edition):
- https://apede.sstuconf.ru/ (site, information letter, formatting
  recommendations PDFs);
- https://www.ieee.org/conferences/publishing/templates.html

## Golden rule

**Remove ALL template guidance text before submission.** The template ends
with: "Please ensure that all template text is removed from your conference
paper prior to submission ... Failure to remove template text from your
paper may result in your paper not being published." This is a hard, common
failure mode - grep the final DOCX/PDF for stock sentences.

## Paper size and template integrity

- This template is tailored for **A4**. (A US-Letter variant exists; use the
  size the conference requires.)
- Margins, column widths, line spacing, and type styles are **built-in - do
  not alter them.** Do not revise the current style designations.
- Confirm you have the correct template for your paper size before styling.

## Copyright notice (page-1 footer) and sponsors text box

- The template's first-page **footer contains the IEEE copyright-notice
  placeholder**: `XXX-X-XXXX-XXXX-X/XX/$XX.00 ©20XX IEEE`. The camera-ready
  paper must have this filled with the code and year the conference
  provides (or handled exactly as the conference instructs). Never leave
  the `XXX` placeholder in a submitted paper, and never delete the footer
  on your own - ask the conference/user if the code is unknown.
- The first page also has a **sponsors/funding text box** ("Identify
  applicable funding agency here. If none, delete this text box."):
  either fill it with the real funding agency/grant or DELETE the text
  box entirely.

## Workflow the template assumes

- Write and save the content as a plain text file FIRST; finish all content
  and organizational editing BEFORE formatting.
- Keep text and graphic files separate until the text is formatted and styled.
- Duplicate the template with Save As and **name the paper file using the
  naming convention prescribed by the conference**.
- Do **not** use hard tabs; limit hard returns to one at the end of a
  paragraph. Do **not** add pagination anywhere. Do **not** number text
  headings by hand - the template numbers them.

## Structure (named styles, in order)

1. **Paper Title** - style "paper title". No sub-titles (not captured in
   Xplore). CRITICAL: **no symbols, special characters, footnotes, or math
   in the title.** In the title, if "that uses" can replace "using",
   capitalize "Using"; else keep lowercase.
2. **Authors / Affiliations** - style "Author". Template designed for (not
   limited to) six authors; minimum one. List left-to-right then down to the
   next line - this is the citation/indexing order. Do not list in columns or
   group by affiliation. Keep affiliations succinct (do not split departments
   of the same organization). Each author block:
   `line1: Given Name Surname / line2: dept. of organization / line3: name of
   organization / line4: City, Country / line5: email or ORCID`.
   - >6 authors: add names horizontally, third row beyond 8.
   - <6 authors: adjust the column count of the author/affiliation block.
3. **Abstract** - style "Abstract" (run-in head, italic). Begins `Abstract—`.
   CRITICAL: **no symbols, special characters, footnotes, or math in the
   abstract.**
4. **Keywords** - style "Keywords" (italic run-in), begins `Keywords—`.
5. **Body** with numbered section headings (see Headings). Typical flow:
   Introduction, method, results, discussion, conclusion.
6. **Acknowledgment** - style "Heading 5" (component head, unnumbered).
   Spelling "acknowledgment" (no "e" after the "g"). Put sponsor
   acknowledgments in the unnumbered first-page footnote, not here, if
   preferred by the template.
7. **References** - style "Heading 5", then entries in style "references".
8. **Tables** and **Figures with captions** as needed, placed in-column.

Component heads (not topically subordinate) use **Heading 5**: e.g.
Acknowledgment, References. Text heads (hierarchical topics) use **Heading
1-4** (uppercase Roman numerals at level 1). Only introduce a sub-head level
if there are >=2 sub-topics.

## Abbreviations and acronyms

- Define abbreviations/acronyms at first use in the text, **even if already
  defined in the abstract**.
- Do NOT need defining: IEEE, SI, MKS, CGS, sc, dc, rms.
- Do not use abbreviations in the title or headings unless unavoidable.

## Units

- Primary units SI (MKS) (encouraged) or CGS; English units only as secondary
  (in parentheses), except as trade identifiers ("3.5-inch disk drive").
- Do not combine SI and CGS (dimensional imbalance). If mixing is
  unavoidable, state units for each quantity in an equation.
- Do not mix spelled-out and abbreviated units ("Wb/m2" or "webers per
  square meter", not "webers/m2"). Spell out units in running text
  ("...a few henries", not "...a few H").
- Use a zero before decimal points: **"0.25", not ".25"**. Use "cm3", not "cc".

## Equations

- Equations are an exception to the prescribed template specs. Type them in
  **Times New Roman or Symbol font only** (no other font). For multileveled
  equations, it may be necessary to treat the equation as a graphic and
  insert it after styling.
- Number equations **consecutively**; equation numbers in parentheses,
  **flush right** using a right tab stop, e.g. `(1)`. Center the equation
  with a center tab stop.
- Make equations compact: use the solidus `/`, the exp function, or
  exponents. **Italicize Roman symbols** for quantities/variables, but **not
  Greek symbols.**
- Use a **long dash rather than a hyphen for a minus sign.**
- Punctuate equations as part of the sentence (commas/periods).
- Define symbols before or immediately after the equation. Refer to "(1)",
  not "Eq. (1)"/"equation (1)", except at sentence start: "Equation (1) is...".

## Figures

- Place figures/tables at the **top or bottom of columns**, not the middle.
  Large ones may span both columns. Insert them **after** first citation.
- **Figure captions go BELOW** the figure (style "figure caption"). Use
  "Fig. 1", even at the start of a sentence. Multi-part figures under one
  number share one caption.
- Figure labels in **8 pt Times New Roman**. Use words, not just symbols, on
  axis labels: write "Magnetization", or "Magnetization, M", not just "M".
  Units in parentheses: "Magnetization (A/m)", "Temperature (K)" - not
  "Temperature/K", and do not label an axis with units only.
- Graphics: ideally **300 dpi TIFF or EPS with all fonts embedded**. Inserting
  via a text box is more stable in MS Word than a direct picture; set the
  text box to No Fill / No Line for invisible frame rules.

## Tables

- **Table heads go ABOVE** the table (style "table head"), numbered.
- Table styles provided: table head, table column head, table column subhead,
  table copy, table footnote. Use **letters for table footnotes** (a, b, ...).
- Do not put footnotes in the abstract or reference list.

## References (IEEE numbered style)

- The template numbers citations consecutively in brackets `[1]`.
- **Sentence punctuation follows the bracket** `[2].`
- Refer to the number only: "as in [3]" - not "Ref. [3]" or "reference [3]",
  except at sentence start: "Reference [3] was the first ...".
- Number footnotes separately in superscripts; footnote text at the bottom of
  the citing column. No footnotes in abstract/reference list.
- Give **all authors' names** unless there are **six or more**, then use
  "et al.". No period after "et" in "et al.".
- Unpublished (even if submitted): cite as "unpublished". Accepted: "in press".
- Capitalize only the first word of a paper title (plus proper nouns and
  element symbols).
- Translation journals: give the English citation first, then the original.
- "i.e." = "that is"; "e.g." = "for example".

Format examples (from the template):
- Journal: `G. Eason, B. Noble, and I. N. Sneddon, "On certain integrals of
  Lipschitz-Hankel type involving products of Bessel functions," Phil. Trans.
  Roy. Soc. London, vol. A247, pp. 529–551, April 1955.`
- Book: `J. Clerk Maxwell, A Treatise on Electricity and Magnetism, 3rd ed.,
  vol. 2. Oxford: Clarendon, 1892, pp.68–73.`
- Chapter in book: `I. S. Jacobs and C. P. Bean, "Fine particles, thin films
  and exchange anisotropy," in Magnetism, vol. III, G. T. Rado and H. Suhl,
  Eds. New York: Academic, 1963, pp. 271–350.`
- Unpublished: `K. Elissa, "Title of paper if known," unpublished.`
- In press: `R. Nicole, "Title of paper with only first word capitalized," J.
  Name Stand. Abbrev., in press.`
- Translation: `Y. Yorozu, ... IEEE Transl. J. Magn. Japan, vol. 2, pp.
  740–741, August 1987 [Digests 9th Annual Conf. Magnetics Japan, p. 301,
  1982].`
- arXiv: `D. P. Kingma and M. Welling, "Auto-encoding variational Bayes,"
  2013, arXiv:1312.6114. [Online]. Available: https://arxiv.org/abs/1312.6114`
- Code/dataset: include `[Online]. Available: <URL>` or `DOI:...`.

## Common English/style mistakes flagged by the template

- "data" is plural, not singular.
- Permeability of vacuum subscript is zero (subscript formatting), not letter
  "o".
- "inset" not "insert"; "alternatively" not "alternately" (unless it really
  alternates); do not use "essentially" to mean "approximately"/"effectively".
- Watch homophones: affect/effect, complement/compliment, discreet/discrete,
  principal/principle; do not confuse imply/infer.
- "non" is a prefix, join it to the word (usually no hyphen).
- American punctuation-inside-quotes rules; parenthetical statement at the end
  of a sentence is punctuated outside the closing parenthesis (like this).

## Pre-submission checklist

- [ ] Correct template/paper size (A4 for APEDE unless told otherwise); margins,
      columns, fonts, spacing UNCHANGED.
- [ ] Title: no symbols/special chars/footnotes/math; no sub-title; correct
      "Using"/"using" capitalization.
- [ ] Author block: left-to-right then down order; succinct affiliations; email
      or ORCID per author.
- [ ] Abstract: no symbols/special chars/footnotes/math; begins `Abstract—`.
- [ ] Keywords present, begins `Keywords—`.
- [ ] All abbreviations defined at first use in body (even if in abstract).
- [ ] SI units; zero before decimals ("0.25"); no mixed unit systems.
- [ ] Numbered equations consecutive, flush-right numbers, one equation object
      each; Roman symbols italic, Greek not; long dash for minus.
- [ ] Figures: cited before placement; caption BELOW; "Fig. 1"; axes with words
      + units in parentheses; >=300 dpi / vector; each figure a separate file.
- [ ] Tables: head ABOVE; letter footnotes; real Word tables.
- [ ] References: IEEE numbered [1] in citation order; punctuation after the
      bracket; all authors unless >=6 (then et al.); title first-word-only caps.
- [ ] **ALL template guidance text removed** (grep for stock sentences).
- [ ] Page-1 footer copyright notice filled with the conference-provided
      code/year (no `XXX-X-XXXX` placeholder left); sponsors text box filled
      or deleted.
- [ ] Paper file named per the conference naming convention.
- [ ] Within the conference PAGE LIMIT.
- [ ] IEEE-Xplore-compliant PDF (fonts embedded, correct size) - run PDF eXpress
      / conference checker if required.
- [ ] IEEE copyright / eCF handled per the conference (their step, not ours).
