# Methodology

This document records the definitions, assumptions, and limitations behind the VITAE & CO. diagnostic so the analysis is transparent and reproducible.

## Metric definitions

| Metric | Definition |
|---|---|
| **GMV** | Sum of gross revenue (pre-discount) across all orders |
| **Net Revenue** | Gross revenue less discounts |
| **AOV** | Average net revenue per order |
| **Gross Margin** | Net revenue − COGS |
| **Contribution Margin** | Net revenue − COGS − fulfillment cost − payment processing fee |
| **CAC** | Channel spend ÷ new customers acquired in that channel-month |
| **Blended CAC** | Total marketing spend ÷ total new customers |
| **LTV** | Cumulative net revenue per customer over their observed lifetime |
| **ROAS** | Net revenue attributed to a channel ÷ spend on that channel |
| **Retention (cohort)** | Share of a monthly acquisition cohort placing an order in month *n* after first purchase |
| **Return rate** | Share of orders with status = Returned |

## Modeling assumptions

- **LTV horizon:** observed lifetime within the data window (Jan 2023 to May 2026). Not extrapolated to a fixed 24-month forward LTV unless stated.
- **Attribution:** single-touch: each customer is attributed to the acquisition channel recorded at signup. A real engagement would pressure-test this against multi-touch or a media-mix model.
- **CAC:** computed per channel-month from spend and net new customers. Always-on brand spend is included in channel spend, which inflates CAC in low-acquisition months (a realistic feature, not a bug).
- **Contribution margin** excludes fixed overhead (salaries, software, warehouse lease); it is a unit-economics view, not a full P&L.
- **Subscription churn** is approximated from order recency rather than billing events, since the synthetic data does not model subscription cancellations explicitly.

## Data realism calibration

The synthetic generator was tuned so the aggregate metrics fall within plausible premium-DTC ranges:

- Marketing spend ≈ 33% of net revenue (growth-stage DTC norm)
- Blended revenue LTV:CAC ≈ 3.1x; contribution-margin LTV:CAC ≈ 2.1x
- Gross margin ~73% blended (high, but consistent with a supplement/grooming-weighted premium catalog)
- Seasonal Q4 lift of 35–45% over baseline
- Return rates 6% base, elevated for first orders and the Lifestyle category

## Limitations

1. **Synthetic data**: patterns are designed, so findings demonstrate *method*, not real market truth.
2. **No fixed-cost layer**: contribution margin is not net profit.
3. **Attribution is simplified**: single-touch acquisition channel only.
4. **No competitive or market context**: this is an internal-data diagnostic only.

These are stated explicitly because acknowledging the limits of an analysis is part of doing it credibly.
