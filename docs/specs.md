# ঞ  — Vocal for Local

**Tagline:** Search beyond language.

**Product promise:** Find useful information in your language, explore trustworthy sources, and understand answers grounded in evidence.

**Project status:** In development / planning  
**Initial market:** Assam, India  
**Long-term market:** India and its diverse language communities

---

## 1. Official Brand Identity

- **Brand name:** ঞ
- **Official product title:** ঞ — Vocal for Local
- **Pronunciation:** Nya, as defined by the brand
- **Primary tagline:** Search beyond language.
- **Secondary tagline:** Find useful information. See the sources.
- **Regional launch message:** Built for Assamese. Designed for a multilingual India.
- **Product category:** Regional-language-first web search engine with source-grounded AI answers.
- **Repository name:** `nya-search`
- **Suggested web title:** Nya — Vocal for Local
- **Short brand reference:** Nya

The character ঞ is a central visual identity element. The Latin spelling “Nya” makes the brand easier to pronounce, type, discover, and reference in technical environments.

## 2. Brand Story

The internet contains enormous amounts of information, but finding useful information can be difficult when people search in regional languages, use Latin-script transliteration, or mix languages in the same query.

Nya aims to make discovering information more natural for these users.

Starting with Assamese and the information needs of people in Assam, Nya combines language-aware web search with AI-generated answers grounded in retrieved sources. Rather than presenting an AI response as unquestionable truth, the product is designed to help people inspect the sources behind an answer.

The long-term goal is to make high-quality information easier to discover regardless of the language in which a person searches.

The letter ঞ is the brand's visual signature. Its association with the product's identity is a branding choice, not a claim that the character literally translates to “search,” “knowledge,” or “intelligence.”

## 3. Mission, Vision and Values

### Mission

Make useful, trustworthy online information easier to discover in Assamese and other regional languages.

### Vision

Build a multilingual search platform that helps people across India access information naturally, without language becoming a barrier.

### Core values

1. **Language inclusion:** Treat regional languages and transliterated queries as first-class search experiences.
2. **Evidence over invention:** Ground AI-generated answers in retrieved sources and show users where claims come from.
3. **Privacy by default:** Minimize data collection and avoid unnecessary storage of personal search activity.
4. **Fair discovery:** Support reputable local and smaller publishers instead of equating popularity with quality.
5. **Transparency:** Clearly distinguish AI answers from ranked web results and explain important limitations.
6. **Responsible engineering:** Respect source permissions, accessibility requirements, safety policies, and applicable law.

## 4. Product Description

### One-line description

Nya is an Assamese-first, multilingual search engine that combines ranked web results with AI answers grounded in sources.

### Short description

Search the web in Assamese, English, Romanized Assamese, or mixed-language queries. Nya is designed to help users find relevant information, explore its sources, and understand answers with greater transparency.

### Full description

ঞ (Nya) is a regional-language-focused search engine designed to improve how people discover information across language boundaries.

The initial product focuses on Assamese-language needs in Assam while supporting English, Assamese in its native script, Romanized Assamese, and mixed Assamese-English queries.

Nya combines traditional web retrieval and ranking with a grounded AI answer experience. Search results remain independently available, while AI-generated answers aim to summarize relevant evidence with claim-level citations.

The product roadmap prioritizes search relevance, responsible source ingestion, trustworthy citations, privacy, accessibility, and measurable quality before expanding to additional languages and advanced features.

### What Nya is not

Nya is not merely a chatbot, an AI wrapper, or a conventional search page with a different logo. Its intended value is the combination of language-aware retrieval, locally relevant discovery, transparent evidence, and responsible product engineering.

## 5. Target Users

- Assamese-speaking students and educators.
- People searching for local news, public information, government services, and educational resources.
- Users who naturally type Assamese queries in Latin characters.
- People who switch between Assamese and English while searching.
- Researchers, developers, journalists, and knowledge seekers.
- Publishers and institutions that want useful regional-language information to be discoverable.

## 6. Core Differentiators

### Regional-language-aware search

Normalize spelling and script variations and recognize common transliteration patterns, with quality measured separately for each query type.

### Assamese-first relevance

Evaluate search quality on Assamese topics, local entities, regional publishers, public services, education, and other locally important information needs.

### Grounded AI answers

Generate answers from retrieved evidence, attach citations to claims, and validate that citations point to real retrieved sources.

### Balanced discovery

Reduce unnecessary duplication and excessive dominance by a single domain when comparable alternatives exist, while preserving legitimate authoritative-source rankings.

### Privacy-first design

Make accounts optional, keep personalization opt-in, avoid raw search-query logging by default, and provide clear retention and deletion rules.

### Multilingual expansion

Establish a reusable technical and evaluation foundation that can support additional Indian languages without assuming that one language's search quality proves another's.

## 7. Initial Product Experience

The proposed homepage should feature:

- A clean, responsive search interface.
- The ঞ (Nya) brand mark and search bar.
- A clear language-aware placeholder.
- A visible way to submit a query.
- Optional Safe Search controls and language filters.
- Accessible loading, error, offline, and no-results states.

After searching, the results page should provide:

- An AI answer panel when a grounded answer can be produced.
- Ranked web results with titles, URLs, snippets, and available source dates.
- Inline citations and an expandable source panel.
- Language and source/date filters.
- Spelling and transliteration suggestions.
- Related-query suggestions and feedback controls.

If a grounded answer cannot be generated, Nya should still provide useful search results and clearly explain the limitation. It must not invent citations to make an answer look complete.

## 8. Technical Direction

The intended architecture is a modular, TypeScript-first frontend supported by a Python search and ingestion backend.

- **Web frontend:** Next.js and TypeScript, with responsive PWA capabilities.
- **Search/API service:** Python and FastAPI.
- **Primary database and retrieval:** PostgreSQL full-text search.
- **Optional semantic retrieval:** pgvector when evaluation demonstrates a meaningful improvement.
- **Authentication:** Optional Supabase Auth or an equivalent service.
- **Source processing:** Scheduled Python jobs for permitted discovery, crawling, extraction, deduplication, and indexing.
- **AI integration:** Provider-agnostic gateway for configurable inference providers.
- **Quality assurance:** Automated regression tests, multilingual evaluation datasets, citation validation, and human Assamese-language review.

These are architecture decisions and intentions, not a claim that every component is already implemented.

## 9. Search and AI Quality Principles

Search quality and AI-answer quality must be evaluated independently.

The project has the following initial targets:

- Search latency: p95 no greater than 2.5 seconds under a documented test load.
- AI-answer latency: p95 no greater than 15 seconds when inference is available.
- Citation correctness: at least 95% on the defined release evaluation set.
- Fabricated citations: zero in that evaluation set.
- Factual claim support: at least 90% of evaluated factual claims supported by their cited evidence.

Initial ranking targets are nDCG@10 of at least 0.70 for English, native-script Assamese, and mixed-language queries, and at least 0.60 for Romanized Assamese. These are release goals that must be demonstrated with labelled evaluation data, not current performance claims.

AI answers must include citations, respect safety restrictions, and disclose uncertainty when evidence is insufficient. High-impact topics require stricter source checks and safer fallback behavior.

## 10. Privacy, Sources and Trust

Nya's source ingestion system should respect robots.txt, terms of service, permissions, copyright, licences, applicable law, rate limits, and access restrictions.

The system must not bypass paywalls or access controls. It should retain only the content and metadata it is permitted to store and make available.

Privacy principles include:

- Guest-first use with optional accounts.
- No default persistent personal search history.
- Opt-in history with a maximum planned retention of 30 days.
- User deletion controls and account-deletion procedures.
- No behavioral advertising profiles based on personal search history.
- Access-controlled operational and security logs.
- Documented handling of removals, privacy complaints, and source corrections.

The launch remains gated on security checks, removal propagation, privacy verification, recovery testing, accessibility, and multilingual quality evaluation.

## 11. Development Roadmap

**Phase 0 — Foundations:** Repository setup, source registry, data contracts, policies, CI, and evaluation datasets.

**Phase 1 — Search first:** Permitted ingestion, deduplication, Assamese normalization and transliteration, PostgreSQL retrieval, initial ranking, result UI, and evaluation harness.

**Phase 2 — Grounded AI:** Evidence selection, claim-level citations, citation validation, source panel, safe fallback, prompt-injection defenses, and spending limits.

**Phase 3 — Product hardening:** Safe Search, feedback and removal workflows, optional authentication, privacy controls, monitoring, backup and restore tests, and accessibility checks.

**Phase 4 — Staged beta:** Internal testing, invited testers, public beta focused on Assam, and expansion only after quality and safety gates pass.

**Phase 5 — Expansion:** Additional languages and sources, measured semantic retrieval, advanced features, and validated institutional or developer services.

## 12. Business Model

Nya is planned to launch free and without advertising.

Possible future revenue sources include premium productivity tools, business or developer APIs, institutional services, and clearly labelled sponsorships.

Organic search results must remain distinguishable from any paid placement. Personal search history must not be used to create behavioral advertising profiles.

The initial operating budget target is ₹0–₹2,000 per month. Actual service availability, hosting limits, API costs, and free-tier restrictions must be verified before choosing production providers.

## 13. Brand Voice

Nya should sound:

- Clear rather than complicated.
- Helpful rather than authoritative for its own sake.
- Locally aware without excluding users outside Assam.
- Trustworthy without claiming perfect accuracy.
- Technically capable without unnecessary jargon.

Avoid exaggerated phrases such as “100% accurate AI,” “the world's best search engine,” or “every answer is guaranteed correct.”

## 14. Homepage Copy

**Eyebrow:** A search engine built with language in mind

# Search beyond language.

Find useful information across Assamese, English, and mixed-language searches.

Nya brings ranked web results and source-grounded AI answers together, helping you explore information and inspect the evidence behind it.

**Search placeholder:** Search in Assamese, English, or Romanized Assamese…

**Primary action:** Search

**Supporting line:** Real sources. Clear answers. Your language.

This is proposed launch copy. Publish capability claims only after the corresponding features and quality gates are validated.

## 15. Repository and README Identity

**Repository:** `nya-search`

**Suggested GitHub description:**

An Assamese-first, multilingual search engine combining language-aware web retrieval with AI-generated answers grounded in cited sources.

**README opening:**

# ঞ (Nya) — Vocal for Local

*Search beyond language.*

Nya is a regional-language-first search engine project focused initially on Assamese and the information needs of users in Assam, India.

The project aims to combine relevant web search results with AI-generated answers grounded in retrieved evidence. It prioritizes multilingual retrieval quality, source transparency, privacy, accessibility, and responsible content ingestion.

**Project status:** In development.

Core capabilities, deployment information, licensing, and contribution instructions should be updated as implementation progresses.

### Suggested repository structure

```text
nya-search/
├── apps/
│   └── web/
├── services/
│   └── search-api/
├── ingestion/
│   ├── discovery/
│   ├── crawler/
│   ├── extraction/
│   └── indexing/
├── packages/
│   └── contracts/
├── evaluation/
├── tests/
├── infra/
├── docs/
├── .github/
│   └── workflows/
├── README.md
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── .gitignore
```

This is a proposed monorepo layout, not an existing repository inventory.

## 16. Metadata and Technical Naming

Use the visible Assamese-script character for the brand and an ASCII-compatible spelling for repository names, service identifiers, and tooling that benefits from simple identifiers.

Suggested HTML metadata:

```html
<title>Nya — Vocal for Local</title>
<meta
  name="description"
  content="Search beyond language. Explore web results and source-grounded AI answers, starting with Assamese."
/>
<meta property="og:title" content="Nya — Vocal for Local" />
<meta
  property="og:description"
  content="Find useful information in your language. Discover the sources behind the answer."
/>
```

Suggested service names:

- `nya-search-web`
- `nya-search-api`
- `nya-search-ingestion`
- `nya-search-evaluation`

Before release, verify that the selected fonts render ঞ correctly, the glyph remains recognizable at small sizes, and its accessible name is announced as “Nya” by assistive technology.

## 17. Short Pitch

Nya is building a regional-language-first search engine that makes discovering reliable online information easier for Assamese-speaking users. It combines language-aware web retrieval with AI answers grounded in visible sources, while prioritizing privacy, transparent evidence, and measurable multilingual quality. Starting in Assam, the long-term goal is to make information more accessible across India's language communities.

## 18. Brand Launch Checklist

- [ ] Approve the official name and spelling.
- [ ] Design and test the primary logo, wordmark, favicon, and monochrome variants.
- [ ] Test Assamese-script rendering across supported browsers and devices.
- [ ] Verify trademark and company-name considerations.
- [ ] Check domain, social-handle, and repository-name availability.
- [ ] Publish the product overview and technical roadmap.
- [ ] Clearly label planned, experimental, and implemented features.
- [ ] Complete search relevance and AI-grounding evaluation.
- [ ] Verify privacy, content-removal, security, and accessibility requirements.
- [ ] Review all branding and capability claims before the public beta.

**Final public-facing name:** ঞ (Nya) — Vocal for Local  
**Final primary tagline:** Search beyond language.