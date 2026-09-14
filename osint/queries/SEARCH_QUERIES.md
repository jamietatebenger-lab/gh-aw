# OSINT Public-Source Search Query Library

## Purpose

Reusable search patterns for lawful public-source investigations, identity
resolution, historical research, corporate research, public court material,
digital-footprint analysis and evidence preservation.

Replace placeholders such as:

- FULL_NAME
- ALIAS
- USERNAME
- COMPANY
- ABN
- ACN
- DOMAIN
- LOCATION
- YEAR

Do not treat a search result as proof. Corroborate important findings with
independent sources.

---

# 1. Identity Resolution

"FULL_NAME"
"FULL_NAME" Australia
"FULL_NAME" "Western Australia"
"FULL_NAME" Perth
"FULL_NAME" LOCATION

"FULL_NAME" occupation
"FULL_NAME" employer
"FULL_NAME" director
"FULL_NAME" proprietor
"FULL_NAME" company
"FULL_NAME" business

("FULL_NAME" OR "ALIAS") LOCATION
("FULL_NAME" OR "ALIAS") (Perth OR WA)
("FULL_NAME" OR "ALIAS") (director OR proprietor OR employee)

---

# 2. Alias and Name-Variant Resolution

"FULL_NAME"
"ALIAS"
"FIRST_NAME MIDDLE_NAME LAST_NAME"
"FIRST_NAME M LAST_NAME"
"FIRST_NAME LAST_NAME"

("FULL_NAME" OR "ALIAS")
("FULL_NAME" OR "ALIAS") Australia
("FULL_NAME" OR "ALIAS") LOCATION

Correlate using:

- approximate age/date
- occupation
- location
- employer
- business
- associates
- usernames
- timeline consistency

Never merge identities merely because names match.

---

# 3. Australian Business Research

"FULL_NAME" ABN
"FULL_NAME" ACN
"FULL_NAME" director
"FULL_NAME" company
"FULL_NAME" business
"FULL_NAME" proprietor

"COMPANY" ABN
"COMPANY" ACN
"COMPANY" director
"COMPANY" registration

site:abr.business.gov.au "FULL_NAME"
site:abr.business.gov.au "COMPANY"

site:asic.gov.au "FULL_NAME"
site:asic.gov.au "COMPANY"

site:gov.au "FULL_NAME" company
site:gov.au "FULL_NAME" business

"ABN" "COMPANY"
"ACN" "COMPANY"

---

# 4. Public Court and Tribunal Research

"FULL_NAME" court
"FULL_NAME" tribunal
"FULL_NAME" judgment
"FULL_NAME" decision
"FULL_NAME" proceeding

site:austlii.edu.au "FULL_NAME"
site:austlii.edu.au "FULL_NAME" LOCATION
site:austlii.edu.au "COMPANY"

site:fedcourt.gov.au "FULL_NAME"
site:hcourt.gov.au "FULL_NAME"
site:wa.gov.au "FULL_NAME" court

"FULL_NAME" filetype:pdf court
"FULL_NAME" filetype:pdf judgment

A name appearing in a judgment does not automatically mean the person was
an accused or defendant. Record their actual role.

---

# 5. Government and Regulatory Records

site:gov.au "FULL_NAME"
site:wa.gov.au "FULL_NAME"

site:gov.au "FULL_NAME" filetype:pdf
site:wa.gov.au "FULL_NAME" filetype:pdf

site:gov.au "COMPANY"
site:wa.gov.au "COMPANY"

site:gov.au "ABN"
site:gov.au "ACN"

"FULL_NAME" regulator
"COMPANY" regulator
"FULL_NAME" licence
"COMPANY" licence

---

# 6. News and Historical Archives

"FULL_NAME" news
"FULL_NAME" newspaper
"FULL_NAME" archive
"FULL_NAME" interview

"FULL_NAME" LOCATION
"FULL_NAME" LOCATION YEAR

"COMPANY" LOCATION
"COMPANY" YEAR

site:trove.nla.gov.au "FULL_NAME"
site:trove.nla.gov.au "COMPANY"

site:nla.gov.au "FULL_NAME"

Use date-bounded searches when reconstructing historical periods.

---

# 7. Public Social and Professional Profiles

"FULL_NAME" LinkedIn
"FULL_NAME" Facebook
"FULL_NAME" Instagram
"FULL_NAME" X
"FULL_NAME" Twitter
"FULL_NAME" GitHub

site:linkedin.com/in "FULL_NAME"
site:github.com "FULL_NAME"

"USERNAME"
"USERNAME" GitHub
"USERNAME" Reddit

site:github.com "USERNAME"
site:reddit.com "USERNAME"

Treat username matches as leads until independently corroborated.

---

# 8. GitHub Research

site:github.com "FULL_NAME"
site:github.com "USERNAME"
site:github.com "COMPANY"
site:github.com "DOMAIN"

Use GitHub's own search for:

"FULL_NAME"
"USERNAME"
"DOMAIN"
"COMPANY"

Look for legitimate public:

- repositories
- commits
- issues
- pull requests
- documentation
- organisation memberships

Do not treat an identical username alone as identity proof.

---

# 9. Domain Research

"DOMAIN"
"DOMAIN" company
"DOMAIN" contact
"DOMAIN" history

Use:

- RDAP
- WHOIS where publicly available
- DNS
- MX records
- certificate transparency
- web archives

Record:

- registrar
- registration dates
- nameservers
- MX infrastructure
- certificate history
- historical web content

---

# 10. Certificate Transparency

Search public certificate-transparency records for:

DOMAIN
%.DOMAIN

Record discovered public hostnames and certificate dates.

Do not assume ownership merely because infrastructure is technically related.

---

# 11. DNS and Infrastructure

For a domain under investigation record publicly available:

A
AAAA
MX
NS
TXT
CNAME

Correlate:

DOMAIN
→ DNS
→ hosting/provider
→ certificates
→ archived pages
→ public organisation records

Infrastructure association is not automatically personal attribution.

---

# 12. Historical Web Research

Search archival services for:

DOMAIN
COMPANY
FULL_NAME
USERNAME

Compare captures across dates.

Record:

- capture timestamp
- archived URL
- page title
- organisation/person named
- material changes
- evidence ID

---

# 13. Public Documents

"FULL_NAME" filetype:pdf
"FULL_NAME" filetype:doc
"FULL_NAME" filetype:docx
"FULL_NAME" filetype:xls
