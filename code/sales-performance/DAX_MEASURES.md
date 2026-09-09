# Power BI DAX Measures — Sales Performance & Call Conversion Analytics

These measures support the privacy-safe portfolio rebuild. The historical executive analysis is genuine; this public model is a new recreation for portfolio evidence.

Use table names:
- `Channel Performance`
- `Mobile Supply`
- `Time Audit`

```DAX
Channel Calls = SUM ( 'Channel Performance'[calls] )

Channel Qualified = SUM ( 'Channel Performance'[qualified] )

Qualified per 1,000 Calls =
DIVIDE ( [Channel Qualified], [Channel Calls] ) * 1000

Long-run Mobile Rate =
CALCULATE (
    [Qualified per 1,000 Calls],
    'Channel Performance'[period] = "May 2025-May 2026",
    'Channel Performance'[number_type] = "Mobile/Direct/Personal"
)

Long-run Landline Rate =
CALCULATE (
    [Qualified per 1,000 Calls],
    'Channel Performance'[period] = "May 2025-May 2026",
    'Channel Performance'[number_type] = "Switch/Landline"
)

Mobile vs Landline Rate Multiple =
DIVIDE ( [Long-run Mobile Rate], [Long-run Landline Rate] )
```

```DAX
Supply Mobile Calls = SUM ( 'Mobile Supply'[mobile_calls] )

Supply Qualified = SUM ( 'Mobile Supply'[qualified] )

Supply Qualified per 1,000 =
DIVIDE ( [Supply Qualified], [Supply Mobile Calls] ) * 1000

Apr-May Unique Contacts =
CALCULATE (
    SUM ( 'Mobile Supply'[unique_mobile_contacts] ),
    'Mobile Supply'[period] = "Apr-May 2026"
)

Jun-Jul Unique Contacts =
CALCULATE (
    SUM ( 'Mobile Supply'[unique_mobile_contacts] ),
    'Mobile Supply'[period] = "Jun-Jul 2026"
)

Unique Contact Change % =
DIVIDE ( [Jun-Jul Unique Contacts] - [Apr-May Unique Contacts], [Apr-May Unique Contacts] )

Apr-May Mobile Calls =
CALCULATE ( [Supply Mobile Calls], 'Mobile Supply'[period] = "Apr-May 2026" )

Jun-Jul Mobile Calls =
CALCULATE ( [Supply Mobile Calls], 'Mobile Supply'[period] = "Jun-Jul 2026" )

Mobile Call Change % =
DIVIDE ( [Jun-Jul Mobile Calls] - [Apr-May Mobile Calls], [Apr-May Mobile Calls] )

Apr-May Qualified =
CALCULATE ( [Supply Qualified], 'Mobile Supply'[period] = "Apr-May 2026" )

Jun-Jul Qualified =
CALCULATE ( [Supply Qualified], 'Mobile Supply'[period] = "Jun-Jul 2026" )

Qualified Change % =
DIVIDE ( [Jun-Jul Qualified] - [Apr-May Qualified], [Apr-May Qualified] )

Apr-May Supply Rate =
CALCULATE ( [Supply Qualified per 1,000], 'Mobile Supply'[period] = "Apr-May 2026" )

Jun-Jul Supply Rate =
CALCULATE ( [Supply Qualified per 1,000], 'Mobile Supply'[period] = "Jun-Jul 2026" )

Supply Rate Change % =
DIVIDE ( [Jun-Jul Supply Rate] - [Apr-May Supply Rate], [Apr-May Supply Rate] )
```

```DAX
Timing Calls = SUM ( 'Time Audit'[calls] )

Timing Qualified = SUM ( 'Time Audit'[qualified] )

Timing Qualified per 1,000 =
DIVIDE ( [Timing Qualified], [Timing Calls] ) * 1000

Qualified Within 5 Min =
SUM ( 'Time Audit'[qualified_within_5min] )

Within 5 Min Share =
DIVIDE ( [Qualified Within 5 Min], [Timing Qualified] )
```

Expected validation values:
- Long-run Mobile Rate ≈ **1.78**
- Long-run Landline Rate ≈ **0.29**
- Rate multiple ≈ **6.1x**
- Unique contacts change ≈ **-14.5%**
- Mobile calls change ≈ **+77.5%**
- Qualified change ≈ **+89.8%**
- Within-five-minute share = **33.3%**
