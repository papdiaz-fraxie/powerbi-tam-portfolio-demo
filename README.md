# Phillip Paez — Data, Automation & Operations Portfolio

Recruiter-facing portfolio built around genuine professional data, analytics and automation work.

## Live portfolio

https://papdiaz-fraxie.github.io/powerbi-tam-portfolio-demo/

## Selected projects

1. **BigQuery Data Platform & Automation** — created a central repository for B2B research that previously lived in separate campaign Google Sheets. The broader environment grew to roughly **1M+ records**, with around **56 researchers** contributing data and an average of about **208 client campaigns per year** across 2022–2025. The case study covers layered human/programmatic QA, Python/SQL standardisation, historical record retention, latest-build selection and Paperform/webhook/Apps Script data exports.
2. **Customer Data Reconciliation & Quality Pipeline** — designed a Python + BigQuery reconciliation workflow for incoming client enrichment files of roughly **1,000–5,000 contact or account records**. Before the workflow, researchers built records manually one by one at roughly **50 records per researcher per day**. Current repository matches could be verified in **seconds** rather than rebuilt from scratch, while every row still received human review. The project covers controlled intake schemas, contact/account matching, recency logic, human-in-the-loop verification, row-level QA outcomes, separate client QA reporting and Python batch loading back into BigQuery for future reuse.
3. **Sales Performance & Call Conversion Analytics** — produced monthly Power BI analysis mainly for the **CEO and directors**, matching call activity to Qualified outcomes and comparing **Mobile / Direct / Personal** with **Switch / Landline** performance. For May 2025–May 2026 the measured rates were **1.78 vs 0.29 qualified per 1,000 calls**. The project also investigates reduced fresh mobile supply, heavier repeat calling and a time-of-day result that was challenged because CRM update timing could create bias. Public aggregate data, DAX and a Power BI build guide support a new privacy-safe portfolio recreation; the new Desktop report is not called validated until it is actually opened and checked in Power BI Desktop.
4. **Market Intelligence & TAM Analysis** — converted a client targeting brief into a **37,993-company Australian TAM** and analysed where the opportunity was concentrated. NSW + Victoria represented **63.7%** of the market; NSW + Victoria + Queensland represented **80.9%**. The original client-facing report was built in Looker Studio and the analytical concept was recreated in Power BI Desktop for the public portfolio.

The earlier **Research Workflow & Data Production** case study remains in the repository but is not a headline homepage project. The featured mix now prioritises data platform, customer data, operational performance analytics and market intelligence.

## Technical evidence

The repository includes safe public examples of:

- BigQuery-style SQL quality checks
- Python/pandas data standardisation and validation
- Latest-researched-build selection with SQL window functions
- Duplicate-detection patterns
- Synthetic customer-data reconciliation using primary/fallback identifiers
- Human-review and QA-summary logic for matched/unmatched customer data
- Power BI DAX measures for call-channel, supply and attribution-quality analysis
- Privacy-safe aggregate source tables for the operations analytics rebuild
- Browser recreations of the sales-performance and market-intelligence analyses
- Source-derived Australian TAM state analysis in Python
- Synthetic campaign funnel / qualification analysis in Python

## Development approach

For the customer-data reconciliation workflow, Phillip has practical working Python knowledge and used ChatGPT as a coding assistant. He defined the matching rules and business logic, tested outputs, debugged failures and iterated the working process. The portfolio therefore uses **designed and implemented** language without presenting him as an advanced Python software engineer or implying every line was written unaided.

The sales-performance project uses a deliberate historical-versus-portfolio distinction. The underlying analysis, attribution rules, findings, monthly Power BI delivery and executive audience are genuine professional work. The new Power BI portfolio rebuild is an upskilling artifact; it should only be described as personally built and Desktop-validated after Phillip actually completes and checks it in Power BI Desktop.

## Privacy and accuracy

The portfolio is based on real professional work, but public code and detailed datasets are synthetic, simplified, aggregated or anonymised where required. No client contact/company records, credentials or proprietary production code are published.

For the BigQuery case study, operating scale is deliberately shown as approximate where appropriate. Campaign volume figures cover internal SalesPond client campaigns; DaaS work was additional.

For the customer-data case study, typical job size (**~1,000–5,000 records**), manual build rate (**~50 records/day**), current-match verification in **seconds**, matching hierarchy, human review and closed-loop BigQuery reuse are based on the real process. No typical match-rate percentage or overall time-saving percentage is claimed because there is no reliable aggregate figure.

For the sales-performance case study, the public source tables contain aggregate results only. A one-call difference is intentionally preserved between the June–July channel slice (**29,772** Mobile / Direct / Personal calls) and the separate supply comparison (**29,771**) because the exact reason for the discrepancy has not been established. The 4–5 pm result is presented with its CRM-timing caveat rather than as a definitive best calling hour.

For the TAM case study, the overall **37,993** Australian company count and exact state totals are source-derived from the original client report. Percentages such as **63.7%** and **80.9%** are calculated directly from those aggregates. Detailed industry, employee-size, revenue, technology-readiness and priority distributions in the public interactive demo are synthetic/anonymised.
