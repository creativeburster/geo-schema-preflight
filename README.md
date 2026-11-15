# geo-schema-preflight

Lightweight Python CLI for auditing **Technical SEO integrity**, **HTTP 200 deep-link status**, **/llms.txt markdown readiness**, and **JSON-LD @graph entity schemas** before production deployments.

## Why This Exists

Modern AI retrieval pipelines (ChatGPT Search, Perplexity, Claude) and Google Search Console indexing rely on predictable server-rendered HTML, clean canonical tags, and unambiguous structured data. Running a fast pre-flight check prevents broken commercial deep links and malformed JSON-LD blocks from reaching production.

## Usage

`ash
python geo_schema_preflight.py https://willsun.agency
`

## Checks Included

- **HTTP Status & Canonical Integrity**: Ensures core service and case-study pages resolve cleanly (HTTP 200, no accidental redirects or .html suffix drift).
- **JSON-LD @graph Validation**: Extracts <script type="application/ld+json"> blocks and flags syntax errors.
- **/llms.txt Inspection**: Checks availability, line count, and Markdown heading structure for LLM crawlers.

## Architecture References

- Engineering & GEO Advisory: [willsun.agency/services](https://willsun.agency/services)
- Technical Portfolio & Tooling: [willsun.agency/works](https://willsun.agency/works)
- Case Studies: [willsun.agency/cases](https://willsun.agency/cases)
