---
name: worksheet-metadata
description: >
  Generate complete, publication-ready metadata for educational worksheets and
  handouts. Produces SEO-optimized titles, meta descriptions, URL slugs, tags,
  categories, and 400–600 word description bodies using 4 audience-matched
  templates (Skill Spotlight, Standards Navigator, Classroom-Ready, Learner-
  Centered). Aligned to CCSS, NGSS, and TEKS standards. Built for US teachers,
  TpT sellers, and curriculum publishers. Use when user says "write a description
  for this worksheet", "generate metadata for worksheet", "create listing copy",
  "SEO description for worksheet", "worksheet metadata", or "worksheet listing".
license: MIT
metadata:
  author: dangluu
  version: "1.0.0"
user-invokable: true
argument-hint: "[worksheet-title-or-topic] [grade-level] [subject]"
---

# Worksheet Metadata Writer

Generate complete, publication-ready metadata for educational worksheets. Output
is dual-optimized for US teachers (trust, grade/standard fit, practical utility)
and search engines/AI systems (Google rankings, AI Overview citation, ChatGPT/
Perplexity extractability).

---

## Activation

This skill activates when the user provides a worksheet topic/title and grade level,
or says any of:
- "write a description for this worksheet"
- "generate metadata for [worksheet name]"
- "create listing copy for [topic] worksheet"
- "SEO description for worksheet"
- "worksheet metadata"

---

## Step 1 — Information Collection

Collect the following fields. Ask for any missing REQUIRED fields before proceeding.

### Required
- `worksheet_title`  — Working title or topic of the worksheet
- `grade_level`      — Single grade (e.g., "Grade 5") or range (e.g., "Grades 3–5")
- `subject`          — e.g., ELA, Math, Science, Social Studies, ESL, Special Education

### Recommended
- `primary_standard`    — Standard code + description (e.g., CCSS.ELA-LITERACY.RI.5.1)
- `supporting_standard` — Secondary standard code if applicable
- `skill_focus`         — Specific skill targeted (e.g., "identifying text evidence")
- `task_count`          — Number of problems or tasks
- `page_count`          — Number of student-facing pages
- `time_estimate`       — Expected completion time in minutes
- `includes_answer_key` — Yes / No
- `differentiation`     — On-level / Below-level / Above-level / All three levels

### Optional
- `file_format`      — PDF, Google Slides, Word, etc.
- `special_features` — e.g., word bank, sentence frames, rubric, worked examples
- `use_cases`        — e.g., warm-up, exit ticket, homework, sub plan, assessment
- `state_context`    — If targeting a specific state standard (TEKS, Virginia SOL, etc.)

If the user provides a URL to a worksheet page, fetch the page content with
WebFetch and extract as many fields as possible before asking for more information.

---

## Step 2 — Template Selection

Select one template based on the worksheet's primary value proposition.
Apply this logic in order:

```
IF worksheet has 3 differentiated levels or versions
  → USE template_4_learner_centered.md

ELSE IF worksheet is explicitly built around a named standard as its core value
  → USE template_2_standards_navigator.md

ELSE IF worksheet is positioned as zero-prep / sub plan / print-and-go
  → USE template_3_classroom_ready.md

ELSE
  → USE template_1_skill_spotlight.md  [default]
```

If the user specifies a template by name or number (1–4), use that template
regardless of the logic above.

Template files: `~/.claude/skills/worksheet-metadata/templates/`
- `template_1_skill_spotlight.md`
- `template_2_standards_navigator.md`
- `template_3_classroom_ready.md`
- `template_4_learner_centered.md`

Read the selected template file before writing.

---

## Step 3 — Standards Resolution

If a standard code is provided, use it directly.

If the user provides a topic and grade but NO standard code, resolve the most
likely applicable standard using the table below, then confirm with the user
before writing.

### Common Standards by Subject

**ELA — CCSS (adopted by 41 states + DC)**
- Reading Informational Text : `CCSS.ELA-LITERACY.RI.[grade].[1-10]`
- Reading Literature         : `CCSS.ELA-LITERACY.RL.[grade].[1-10]`
- Writing                    : `CCSS.ELA-LITERACY.W.[grade].[1-10]`
- Language                   : `CCSS.ELA-LITERACY.L.[grade].[1-6]`
- Speaking & Listening       : `CCSS.ELA-LITERACY.SL.[grade].[1-6]`

**Math — CCSS (adopted by 41 states + DC)**
- Operations & Algebraic Thinking : `CCSS.MATH.CONTENT.[grade].OA.[code]`
- Number & Operations Base Ten    : `CCSS.MATH.CONTENT.[grade].NBT.[code]`
- Fractions                       : `CCSS.MATH.CONTENT.[grade].NF.[code]`
- Geometry                        : `CCSS.MATH.CONTENT.[grade].G.[code]`
- Measurement & Data              : `CCSS.MATH.CONTENT.[grade].MD.[code]`

**Science — NGSS (adopted by 20 states)**
- Format  : `[grade]-[discipline core idea]-[number]`
- Example : `3-LS1-1`  (Grade 3, Life Science, standard 1)

**Texas — TEKS (Texas only)**
- Format  : `[Subject] §[chapter].[subchapter]([grade])`
- Note    : Always label as "TEKS" — never use "CCSS" for Texas listings.

**Multi-state note:** If the target state uses a framework layered on CCSS, cite both.
Example: "Aligned to CCSS.ELA-LITERACY.RI.5.1, as adopted by the California ELA/ELD Framework."

---

## Step 4 — Output Specification

Produce ALL of the following fields for every worksheet:

| Field             | Format             | Length           | Notes                                       |
|-------------------|--------------------|------------------|---------------------------------------------|
| title             | Plain text         | 40–60 characters | Primary keyword in first half; power word   |
| meta_title        | Plain text         | 40–60 characters | Matches or variants title; brand optional   |
| meta_description  | Plain text         | 150–160 chars    | Value prop + standard code + implicit CTA   |
| url_slug          | Lowercase, hyphens | Max 75 chars     | Keyword-first; no stop words; no dates      |
| description_body  | Markdown           | 400–600 words    | Uses selected template; At a Glance block   |
| tags              | Comma-separated    | 5–10 tags        | Grade, subject, standard, skill, use case   |
| category          | Single value       | —                | Subject area (e.g., "Grade 5 ELA")          |

---

## Step 5 — SEO Validation

Before delivering output, run ALL checks below. Flag any failure with a fix.

**Title Checks**
- [ ] 40–60 characters — no SERP truncation risk
- [ ] Primary keyword appears in first half of title
- [ ] At least one power word: `Printable | Aligned | Complete | Essential | Ready | Proven | Free | Guide`
- [ ] Specific — includes grade + skill + format signal

**Meta Description Checks**
- [ ] 150–160 characters exactly
- [ ] Contains at least one specific value (standard code, page count, or named feature)
- [ ] Ends with an implied action word (download, print, use, assign, access)
- [ ] Primary keyword present; not repeated more than once

**URL Slug Checks**
- [ ] All lowercase, hyphens only — no underscores or special characters
- [ ] Contains primary keyword or close variant
- [ ] No date segments (/2024/, /2025/, /2026/)
- [ ] Under 75 characters
- [ ] Minimal stop words

**Description Body Checks**
- [ ] Total word count between 400–600 words
- [ ] Opens with 40–60 word answer-first paragraph before At a Glance
- [ ] At a Glance block present immediately after opening paragraph
- [ ] Standard code cited with plain-English description of what it requires
- [ ] Citation Capsule paragraph present — 130–160 words, self-contained and quotable
- [ ] At least one specific number (task count, page count, time, or research statistic)
- [ ] No banned AI phrases: `"dive into" | "game-changer" | "digital landscape" | "harness the power" | "unlock" | "revolutionize" | "in today's world" | "it's important to note" | "ever-evolving" | "seamlessly"`

---

## Step 6 — Output Delivery Format

Deliver all output in this structure:

```
---
## [worksheet_title] — Metadata Output

### SEO Fields
Title            : [title]
Meta Title       : [meta_title]
Meta Description : [meta_description]
URL Slug         : /[url_slug]
Tags             : [tag1], [tag2], [tag3], ...
Category         : [category]

### Description
[Full description body — markdown formatted, ready to paste]

### SEO Validation
[Pass/fail for each check — flag failures with one-line fix suggestion]
---
```

---

## Quality Gates

Do NOT deliver output if any of the following are true:
- Standard code is missing AND user has not confirmed proceeding without one
- Description body is under 380 words or over 640 words
- Meta description is outside 140–165 characters
- More than 2 SEO validation checks fail without user acknowledgment

In any of these cases, flag the issue and ask the user how to proceed.

---

## At a Glance Block Specification

The At a Glance block is a scannable summary inserted after the opening paragraph.

**Format:** markdown blockquote with bold field labels
**Placement:** immediately after the opening paragraph, before the first content section
**Word count:** 50–80 words (counted as part of the total 400–600 word body)

Base structure (adapt per template):

```
> **At a Glance**
> - **Grade:** [N] · **Subject:** [Subject]
> - **Standard:** `[CODE]` — [Plain-English: what students must do, max 15 words]
> - **Skill Focus:** [Specific skill this worksheet targets]
> - **Format:** [N] pages · [N] problems · Answer key included · PDF
> - **Best For:** [Primary use case in 5–7 words]
> - **Time:** [N]–[N] minutes
```

The standard code must appear in backticks. The plain-English description must
explain what the standard requires students to DO — not just its name.

---

## References

- Templates      : `~/.claude/skills/worksheet-metadata/templates/`
- CCSS standards : https://www.thecorestandards.org
- NGSS standards : https://www.nextgenscience.org
- TEKS standards : https://tea.texas.gov/academics/curriculum-standards
- SEO rules      : Adapted from blog-seo-check and seo-content skills
- Research       : RAND AIRS 2024, EdReports State of Market 2024,
                   ScienceDirect TpT Analysis (500k listings)
