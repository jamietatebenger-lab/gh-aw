#!/usr/bin/env python3

import argparse
import json
from urllib.parse import quote_plus


def quoted(value):
    return f'"{value.strip()}"'


def google_url(query):
    return "https://www.google.com/search?q=" + quote_plus(query)


def add_query(results, category, query):
    results.append({
        "category": category,
        "query": query,
        "url": google_url(query)
    })


def generate_queries(name, aliases=None, locations=None,
                     organisations=None, associates=None,
                     start_year=None, end_year=None):

    aliases = aliases or []
    locations = locations or []
    organisations = organisations or []
    associates = associates or []

    names = [name] + aliases
    results = []

    # -------------------------------------------------
    # IDENTITY RESOLUTION
    # -------------------------------------------------

    for n in names:
        qn = quoted(n)

        add_query(results, "identity", qn)
        add_query(results, "identity", f"{qn} Australia")
        add_query(results, "identity", f"{qn} biography")
        add_query(results, "identity", f"{qn} profile")
        add_query(results, "identity", f"{qn} occupation")
        add_query(results, "identity", f"{qn} director")
        add_query(results, "identity", f"{qn} proprietor")

        for location in locations:
            add_query(
                results,
                "identity-location",
                f'{qn} {quoted(location)}'
            )

    # -------------------------------------------------
    # AUSTRALIAN GOVERNMENT SOURCES
    # -------------------------------------------------

    government_domains = [
        "gov.au",
        "wa.gov.au",
        "nt.gov.au",
        "sa.gov.au",
        "qld.gov.au",
        "nsw.gov.au",
        "vic.gov.au",
        "tas.gov.au"
    ]

    for n in names:
        for domain in government_domains:
            add_query(
                results,
                "government",
                f'{quoted(n)} site:{domain}'
            )

            add_query(
                results,
                "government-pdf",
                f'{quoted(n)} site:{domain} filetype:pdf'
            )

    # -------------------------------------------------
    # COURTS / LEGAL MATERIAL
    # -------------------------------------------------

    legal_terms = [
        "court",
        "judgment",
        "tribunal",
        "proceeding",
        "decision",
        "appeal"
    ]

    for n in names:
        for term in legal_terms:
            add_query(
                results,
                "legal",
                f'{quoted(n)} {term}'
            )

        add_query(
            results,
            "austlii",
            f'{quoted(n)} site:austlii.edu.au'
        )

    # -------------------------------------------------
    # BUSINESS / CORPORATE
    # -------------------------------------------------

    business_terms = [
        "ABN",
        "ACN",
        "company",
        "business",
        "director",
        "shareholder",
        "proprietor"
    ]

    for n in names:
        for term in business_terms:
            add_query(
                results,
                "business",
                f'{quoted(n)} {term} Australia'
            )

        for organisation in organisations:
            add_query(
                results,
                "business-association",
                f'{quoted(n)} {quoted(organisation)}'
            )

    # -------------------------------------------------
    # NEWS / HISTORICAL ARCHIVES
    # -------------------------------------------------

    for n in names:

        add_query(
            results,
            "news",
            f'{quoted(n)} news Australia'
        )

        add_query(
            results,
            "trove",
            f'{quoted(n)} site:trove.nla.gov.au'
        )

        add_query(
            results,
            "nla",
            f'{quoted(n)} site:nla.gov.au'
        )

        add_query(
            results,
            "archives",
            f'{quoted(n)} archive Australia'
        )

        add_query(
            results,
            "historical",
            f'{quoted(n)} newspaper Australia'
        )

    # -------------------------------------------------
    # PUBLIC SOCIAL / USERNAME DISCOVERY
    # -------------------------------------------------

    public_platforms = [
        "github.com",
        "linkedin.com",
        "reddit.com"
    ]

    for n in names:
        for platform in public_platforms:
            add_query(
                results,
                "public-profile",
                f'{quoted(n)} site:{platform}'
            )

    # -------------------------------------------------
    # ASSOCIATION CORRELATION
    # -------------------------------------------------

    for n in names:
        for associate in associates:

            add_query(
                results,
                "associate",
                f'{quoted(n)} {quoted(associate)}'
            )

            for location in locations:
                add_query(
                    results,
                    "associate-location",
                    f'{quoted(n)} {quoted(associate)} '
                    f'{quoted(location)}'
                )

    # -------------------------------------------------
    # DOCUMENT DISCOVERY
    # -------------------------------------------------

    document_types = [
        "pdf",
        "doc",
        "docx",
        "xls",
        "xlsx"
    ]

    for n in names:
        for extension in document_types:
            add_query(
                results,
                "document",
                f'{quoted(n)} filetype:{extension}'
            )

    # -------------------------------------------------
    # GITHUB PUBLIC CODE SEARCH
    # -------------------------------------------------

    for n in names:
        add_query(
            results,
            "github",
            f'{quoted(n)} site:github.com'
        )

    # -------------------------------------------------
    # DOMAIN / INFRASTRUCTURE PUBLIC SOURCES
    # -------------------------------------------------

    for organisation in organisations:

        add_query(
            results,
            "infrastructure",
            f'{quoted(organisation)} domain'
        )

        add_query(
            results,
            "certificate-transparency",
            f'{quoted(organisation)} crt.sh'
        )

        add_query(
            results,
            "rdap",
            f'{quoted(organisation)} RDAP'
        )

    # -------------------------------------------------
    # DATE CORRELATION
    # -------------------------------------------------

    if start_year and end_year:

        for n in names:
            add_query(
                results,
                "date-range",
                f'{quoted(n)} after:{start_year}-01-01 '
                f'before:{end_year}-12-31'
            )

            for location in locations:
                add_query(
                    results,
                    "timeline",
                    f'{quoted(n)} {quoted(location)} '
                    f'after:{start_year}-01-01 '
                    f'before:{end_year}-12-31'
                )

    # Remove duplicates
    unique = {}
    for item in results:
        unique[item["query"]] = item

    return list(unique.values())


def main():

    parser = argparse.ArgumentParser(
        description=(
            "Generate structured public-source OSINT "
            "research queries."
        )
    )

    parser.add_argument("name")

    parser.add_argument(
        "--alias",
        action="append",
        default=[]
    )

    parser.add_argument(
        "--location",
        action="append",
        default=[]
    )

    parser.add_argument(
        "--organisation",
        action="append",
        default=[]
    )

    parser.add_argument(
        "--associate",
        action="append",
        default=[]
    )

    parser.add_argument("--start-year", type=int)
    parser.add_argument("--end-year", type=int)

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of text"
    )

    args = parser.parse_args()

    results = generate_queries(
        name=args.name,
        aliases=args.alias,
        locations=args.location,
        organisations=args.organisation,
        associates=args.associate,
        start_year=args.start_year,
        end_year=args.end_year
    )

    if args.json:
        print(json.dumps(results, indent=2))
        return

    categories = {}

    for result in results:
        categories.setdefault(
            result["category"], []
        ).append(result)

    print()
    print("FORENSIC OSINT QUERY PLAN")
    print("=" * 70)

    for category, items in categories.items():

        print()
        print(f"[{category.upper()}]")
        print("-" * 70)

        for item in items:
            print(item["query"])

    print()
    print(f"Generated {len(results)} unique queries.")


if __name__ == "__main__":
    main()
