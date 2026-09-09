"""Privacy-safe portfolio recreation of a customer-data reconciliation workflow.

This is NOT production code and uses no client data.

It demonstrates the logic behind a real workflow I designed and implemented:
- match client contact/account records against a maintained reference repository
- use LinkedIn URL as the primary contact identifier
- use secondary identifiers when LinkedIn is unavailable
- use company LinkedIn/domain/name/location for account matching
- expose simplified match categories for auditability
- keep every row in a human-review path
- produce a QA summary before a validated batch is loaded back to BigQuery

Important: the 60-day freshness value below is illustrative only. In the real
process, re-verification thresholds were set conservatively based on observed
change behaviour in continuously rebuilt data rather than one universal rule.
"""

from __future__ import annotations

from datetime import date
from urllib.parse import urlparse

import pandas as pd


DEMO_FRESHNESS_DAYS = 60  # portfolio illustration only, not a production SLA


def clean_text(value: object) -> str:
    """Lower-case and trim a value for simple deterministic comparison."""
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().lower().split())


def clean_url(value: object) -> str:
    """Normalise common URL differences without attempting fuzzy identity resolution."""
    text = clean_text(value)
    if not text:
        return ""
    if not text.startswith(("http://", "https://")):
        text = "https://" + text
    parsed = urlparse(text)
    host = parsed.netloc.removeprefix("www.")
    path = parsed.path.rstrip("/")
    return f"{host}{path}".lower()


def domain_from_website(value: object) -> str:
    text = clean_text(value)
    if not text:
        return ""
    if not text.startswith(("http://", "https://")):
        text = "https://" + text
    host = urlparse(text).netloc.lower().removeprefix("www.")
    return host


def reference_is_fresh(research_date: object, as_of: date) -> bool:
    """Illustrative freshness check for the public demo."""
    if pd.isna(research_date):
        return False
    researched = pd.to_datetime(research_date).date()
    return (as_of - researched).days <= DEMO_FRESHNESS_DAYS


def match_contact(client_row: pd.Series, reference: pd.DataFrame) -> dict:
    """Return the best deterministic contact candidate using simplified rules."""
    linkedin = clean_url(client_row.get("linkedin_url"))
    email = clean_text(client_row.get("work_email"))
    first_name = clean_text(client_row.get("first_name"))
    last_name = clean_text(client_row.get("last_name"))
    company = clean_text(client_row.get("company_name"))

    # Primary production concept: LinkedIn URL is the strongest contact key.
    if linkedin:
        mask = reference["linkedin_url"].map(clean_url).eq(linkedin)
        matches = reference[mask]
        if len(matches) == 1:
            return {"match_status": "LinkedIn match", "reference_index": matches.index[0]}

    # Secondary-field matching is deliberately conservative in this demo.
    if email:
        mask = reference["work_email"].map(clean_text).eq(email)
        matches = reference[mask]
        if len(matches) == 1:
            return {"match_status": "Secondary-field match", "reference_index": matches.index[0]}

    if first_name and last_name and company:
        mask = (
            reference["first_name"].map(clean_text).eq(first_name)
            & reference["last_name"].map(clean_text).eq(last_name)
            & reference["company_name"].map(clean_text).eq(company)
        )
        matches = reference[mask]
        if len(matches) == 1:
            return {"match_status": "Secondary-field match", "reference_index": matches.index[0]}
        if len(matches) > 1:
            return {"match_status": "Possible match / needs review", "reference_index": None}

    return {"match_status": "No match", "reference_index": None}


def match_account(client_row: pd.Series, reference: pd.DataFrame) -> dict:
    """Simplified account matching using company profile, domain, name and location."""
    company_linkedin = clean_url(client_row.get("company_linkedin"))
    domain = domain_from_website(client_row.get("website"))
    company = clean_text(client_row.get("company_name"))
    country = clean_text(client_row.get("country"))

    if company_linkedin:
        mask = reference["company_linkedin"].map(clean_url).eq(company_linkedin)
        matches = reference[mask]
        if len(matches) == 1:
            return {"match_status": "Company LinkedIn match", "reference_index": matches.index[0]}

    if domain:
        mask = reference["website"].map(domain_from_website).eq(domain)
        matches = reference[mask]
        if len(matches) == 1:
            return {"match_status": "Domain match", "reference_index": matches.index[0]}

    if company and country:
        mask = (
            reference["company_name"].map(clean_text).eq(company)
            & reference["country"].map(clean_text).eq(country)
        )
        matches = reference[mask]
        if len(matches) == 1:
            return {"match_status": "Name + location match", "reference_index": matches.index[0]}
        if len(matches) > 1:
            return {"match_status": "Possible match / needs review", "reference_index": None}

    return {"match_status": "No match", "reference_index": None}


def reconcile_contacts(client: pd.DataFrame, reference: pd.DataFrame, as_of: date) -> pd.DataFrame:
    """Create an auditable review queue. Every row still requires human review."""
    output = []

    for _, row in client.iterrows():
        result = match_contact(row, reference)
        ref_index = result["reference_index"]
        ref = reference.loc[ref_index] if ref_index is not None else None

        output.append(
            {
                "client_record_id": row["client_record_id"],
                "match_status": result["match_status"],
                "reference_research_date": None if ref is None else ref["research_date"],
                "reference_is_fresh": False if ref is None else reference_is_fresh(ref["research_date"], as_of),
                # Real workflow principle: matched values can replace stale client values,
                # but a researcher still reviews every row before delivery.
                "candidate_job_title": row.get("job_title") if ref is None else ref.get("job_title"),
                "human_review_required": True,
                "manual_research_required": ref is None
                or not reference_is_fresh(ref["research_date"], as_of),
            }
        )

    return pd.DataFrame(output)


def qa_summary(review_queue: pd.DataFrame) -> pd.DataFrame:
    """Example of a separate QA summary alongside row-level outcomes."""
    summary = (
        review_queue.groupby("match_status", dropna=False)
        .agg(records=("client_record_id", "count"), manual_research=("manual_research_required", "sum"))
        .reset_index()
    )
    summary["share_of_file"] = summary["records"] / len(review_queue)
    return summary.sort_values(["records", "match_status"], ascending=[False, True])


if __name__ == "__main__":
    # Synthetic records only. Names and companies are fictitious.
    repository = pd.DataFrame(
        [
            {
                "first_name": "Alex",
                "last_name": "Morgan",
                "company_name": "Harbour Grid",
                "linkedin_url": "https://linkedin.com/in/alex-morgan-demo",
                "work_email": "alex.morgan@harbourgrid.example",
                "job_title": "Head of Operations",
                "research_date": "2026-08-20",
            },
            {
                "first_name": "Sam",
                "last_name": "Lee",
                "company_name": "Northstar Systems",
                "linkedin_url": "",
                "work_email": "sam.lee@northstar.example",
                "job_title": "Data Manager",
                "research_date": "2026-05-01",
            },
        ]
    )

    client_file = pd.DataFrame(
        [
            {
                "client_record_id": "C001",
                "first_name": "Alex",
                "last_name": "Morgan",
                "company_name": "Harbour Grid",
                "linkedin_url": "linkedin.com/in/alex-morgan-demo/",
                "work_email": "old.email@client.example",
                "job_title": "Operations Manager",
            },
            {
                "client_record_id": "C002",
                "first_name": "Sam",
                "last_name": "Lee",
                "company_name": "Northstar Systems",
                "linkedin_url": "",
                "work_email": "sam.lee@northstar.example",
                "job_title": "Data Lead",
            },
            {
                "client_record_id": "C003",
                "first_name": "Taylor",
                "last_name": "Ng",
                "company_name": "Civic Cloud",
                "linkedin_url": "",
                "work_email": "",
                "job_title": "IT Manager",
            },
        ]
    )

    queue = reconcile_contacts(client_file, repository, as_of=date(2026, 9, 9))
    print("REVIEW QUEUE")
    print(queue.to_string(index=False))
    print("\nQA SUMMARY")
    print(qa_summary(queue).to_string(index=False))

    # In the real workflow, the final validated batch is loaded back into
    # BigQuery through Python after record-level human QA is complete.
