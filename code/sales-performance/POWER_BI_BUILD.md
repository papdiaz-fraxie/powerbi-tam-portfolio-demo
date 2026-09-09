# Power BI Portfolio Build — Sales Performance & Call Conversion Analytics

This is a new privacy-safe recreation of genuine professional analysis. The historical analysis was delivered monthly in Power BI to the CEO and directors; this portfolio build is a separate upskilling artifact.

## Source tables

- `data/sales-performance/channel_performance.csv`
- `data/sales-performance/mobile_supply_comparison.csv`
- `data/sales-performance/time_of_day_audit.csv`

Load them into Power BI Desktop as:
- **Channel Performance**
- **Mobile Supply**
- **Time Audit**

No relationships are required because each table represents a distinct aggregate analytical slice.

## Page 1 — Call Channel Performance

Show:
- Mobile/Direct/Personal qualified per 1,000 calls: ~1.78
- Switch/Landline qualified per 1,000 calls: ~0.29
- descriptive rate multiple: ~6.1x
- bar chart of qualified per 1,000 calls by number type
- evidence table with calls, qualified and rate

Methodology note:
- match calls to leads using campaign ID, sub-campaign ID, party ID and exact phone number
- use the call immediately before Qualified
- require Qualified update within 30 minutes
- remove duplicates and ambiguous matches

## Page 2 — Fresh Data Supply vs Calling Intensity

Show:
- unique contacts: 10,411 → 8,904 (-14.5%)
- calls: 16,770 → 29,771 (+77.5%)
- qualified: 49 → 93 (+89.8%)
- qualified per 1,000 calls: 2.92 → 3.12

Interpretation:
> The fresh mobile pool became smaller while calling volume rose sharply, indicating more repeat attempts. The measured conversion rate did not deteriorate over the compared periods.

Keep this observational, not causal.

Important source note: the separate June–July channel analysis reports 29,772 Mobile/Direct/Personal calls while the supply slice reports 29,771. The portfolio preserves the source values rather than forcing a reconciliation without evidence.

## Page 3 — Timing & Attribution Quality

Show:
- strongest recorded hour: 4:00–4:59 pm
- 3,364 calls
- 21 qualified
- 6.24 qualified per 1,000
- only 7 of 21 qualifications within five minutes of the call (33.3%)

Interpretation:
> 4–5 pm looks strong in the recorded data, but delayed CRM administration may inflate the apparent result. The evidence is not strong enough to call it the definitive best hour.

## DAX

See `DAX_MEASURES.md`.

## Claim boundary

Do not claim the historical Power BI model/dashboard was personally built by Phillip unless separately verified. After Phillip builds and validates this new report in Power BI Desktop, it is accurate to say he built the **portfolio Power BI recreation** including its model, DAX measures and visuals.
