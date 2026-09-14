# OSINT Source & Cross-Reference Matrix

## Purpose

Track every significant source, claim, identity attribute,
corroboration and contradiction discovered during an investigation.

## Master Source Matrix

| ID | Subject | Source Type | Source | Claim | Date | Grade | Confidence | Corroborated |
|---|---|---|---|---|---|---|---|---|
| SRC-001 | | | | | | | | |

## Identity Resolution Matrix

| Attribute | Observed Value | Source 1 | Source 2 | Match | Confidence |
|---|---|---|---|---|---|
| Full Name | | | | | |
| Alias | | | | | |
| DOB / Age | | | | | |
| Location | | | | | |
| Employment | | | | | |
| Business | | | | | |
| ABN / ACN | | | | | |
| Associate | | | | | |
| Username | | | | | |
| Domain | | | | | |

## Claim Corroboration Matrix

| Claim ID | Claim | Primary Source | Independent Source | Contradiction | Status |
|---|---|---|---|---|---|
| CLM-001 | | | | | |

Status:

CONFIRMED  
PROBABLE  
UNVERIFIED  
CONTRADICTED  
REJECTED

## Associate Matrix

| Entity A | Relationship | Entity B | Evidence | Source | Date Range | Confidence |
|---|---|---|---|---|---|---|

## Timeline Correlation

| Date | Event | Person / Organisation | Location | Source | Confidence |
|---|---|---|---|---|---|

## Source Categories

- Government
- Court
- Tribunal
- Regulatory
- Corporate registry
- News
- Newspaper archive
- Historical archive
- Public social profile
- Professional profile
- GitHub/code
- Domain/DNS
- RDAP/WHOIS
- Certificate Transparency
- Public document
- Metadata
- Aggregator
- Other

## Source Grades

A — Primary / official evidence

B — Strong independent secondary source

C — Public profile or professional source

D — Aggregator or indirect source

E — Unverified lead

## Cross-Reference Rule

Never treat repeated copies of the same original information
as independent corroboration.

Two websites repeating one newspaper article represent one
underlying source, not two independent sources.

## Identity Collision Rule

Before merging records, compare:

- Name
- Name variants
- Age / DOB
- Geography
- Employment
- Business associations
- Associates
- Timeline
- Username
- Domain
- Other distinguishing attributes

A matching name alone does not establish identity.

## Contradiction Rule

Record contradictory evidence rather than removing it.

Contradictions may reveal:

- Different people with the same name
- Incorrect dates
- Incorrect locations
- Outdated information
- Copied reporting errors
- False attribution
- Username collisions

## Evidence Rule

Important findings should reference an evidence record containing:

- Evidence ID
- Original source
- Publication date
- Collection date/time
- Claim supported
- Identity attributes
- Corroborating evidence
- Contradictions
- Source grade
- Confidence
- SHA-256 where evidence is preserved
