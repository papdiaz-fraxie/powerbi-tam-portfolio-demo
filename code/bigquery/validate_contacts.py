"""Synthetic portfolio example of pre-BigQuery data preparation.

This is not production code and contains no client data. It illustrates the
kind of standardisation and validation applied after researcher/human QA and
before loading data into a central repository.
"""

import re
import pandas as pd

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
NON_DIGIT_RE = re.compile(r"\D+")

COUNTRY_MAP = {
    "au": "Australia",
    "aus": "Australia",
    "australia": "Australia",
    "nz": "New Zealand",
    "new zealand": "New Zealand",
}

SENIORITY_MAP = {
    "mgr": "Manager",
    "manager": "Manager",
    "snr manager": "Senior Manager",
    "senior manager": "Senior Manager",
    "dir": "Director",
    "director": "Director",
}


def clean_text(value: object) -> str:
    return " ".join(str(value or "").strip().split())


def normalise_country(value: object) -> str:
    raw = clean_text(value)
    return COUNTRY_MAP.get(raw.lower(), raw)


def normalise_phone(value: object) -> str:
    """Create a consistent digits-only representation for this public demo."""
    return NON_DIGIT_RE.sub("", clean_text(value))


def normalise_seniority(value: object) -> str:
    raw = clean_text(value)
    return SENIORITY_MAP.get(raw.lower(), raw)


records = [
    [1, "Alex", "Smith", "Northstar Tech", "alex.smith@example.com", "AU", "0412 345 678", "Mgr", "https://linkedin.com/in/alex-smith"],
    [2, "Jordan", "Lee", "Harbour Systems", "jordan.lee@example.com", "AUS", "+61 412 222 333", "Director", "https://linkedin.com/in/jordan-lee"],
    [3, "Taylor", "Brown", "Vector Labs", "bad-email", "Australia", "02 9000 1234", "Snr Manager", "https://linkedin.com/in/taylor-brown"],
    [4, "", "Wilson", "Summit Digital", "morgan.wilson@example.com", "Australia", "(03) 9010 1111", "Manager", "https://linkedin.com/in/morgan-wilson"],
    [5, "Sam", "Martin", "Northstar Tech", "", "NZ", "09 300 1000", "Dir", "https://linkedin.com/in/sam-martin"],
    [6, "Jordan", "Lee", "Harbour Systems", "jordan.lee@example.com", "Australia", "0412222333", "Director", "https://linkedin.com/in/jordan-lee"],
]

columns = [
    "contact_id",
    "first_name",
    "last_name",
    "company",
    "email",
    "country",
    "phone",
    "seniority",
    "linkedin_url",
]

df = pd.DataFrame(records, columns=columns)

# Standardisation layer
for col in ["first_name", "last_name", "company", "email", "linkedin_url"]:
    df[col] = df[col].map(clean_text)

df["email_clean"] = df["email"].str.lower()
df["country_clean"] = df["country"].map(normalise_country)
df["phone_clean"] = df["phone"].map(normalise_phone)
df["seniority_clean"] = df["seniority"].map(normalise_seniority)
df["linkedin_clean"] = df["linkedin_url"].str.lower().str.rstrip("/")

# Validation layer
required_fields = ["first_name", "last_name", "company", "country_clean", "linkedin_clean"]
df["missing_required_field"] = df[required_fields].eq("").any(axis=1)
df["valid_email"] = df["email_clean"].apply(
    lambda value: bool(EMAIL_RE.match(value)) if value else False
)
df["duplicate_email"] = df["email_clean"].replace("", pd.NA).duplicated(keep=False)
df["duplicate_linkedin"] = df["linkedin_clean"].replace("", pd.NA).duplicated(keep=False)

df["needs_review"] = (
    df["missing_required_field"]
    | (~df["valid_email"] & df["email_clean"].ne(""))
    | df["duplicate_email"]
    | df["duplicate_linkedin"]
)

summary = {
    "total_records": len(df),
    "records_needing_review": int(df["needs_review"].sum()),
    "missing_required_fields": int(df["missing_required_field"].sum()),
    "invalid_nonblank_email": int((~df["valid_email"] & df["email_clean"].ne("")).sum()),
    "duplicate_email_rows": int(df["duplicate_email"].sum()),
    "duplicate_linkedin_rows": int(df["duplicate_linkedin"].sum()),
}

print("DATA QUALITY SUMMARY")
for key, value in summary.items():
    print(f"{key:28} {value}")

print("\nSTANDARDISED SAMPLE")
print(
    df[
        [
            "contact_id",
            "country_clean",
            "phone_clean",
            "seniority_clean",
            "needs_review",
        ]
    ].to_string(index=False)
)
