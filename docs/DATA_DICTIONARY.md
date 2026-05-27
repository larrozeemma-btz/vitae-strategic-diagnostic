# VITAE & CO. — Dataset Documentation

**Brand:** VITAE & CO. (fictional)
**Positioning:** Premium DTC pet ecommerce — aesthetic & longevity products for dogs and cats, national US market.
**Date range:** January 2023 – May 2026
**Purpose:** Portfolio dataset for Business Analyst, Business Operations, and Consulting Associate work samples.

---

## Headline metrics (built into the data)
- ~4,200 customers
- ~25,000 orders
- ~54,000 order line items
- $8.0M gross merchandise value (GMV)
- $7.95M net revenue
- 22 SKUs across 4 categories
- 6 acquisition channels with monthly spend, impressions, clicks, and CAC
- 7 customer segments (VIP, Aesthetic, Wellness Curious, Lifestyle, Bargain, New Parents, Churned)
- Multi-year seasonal patterns (Q4 spike, summer dip)
- Real promo events (Black Friday, Cyber Monday, V-Day, Mother's Day, Summer Sale)

---

## Tables

### 1. `products.csv` (22 rows)
Master product catalog.

| Field | Type | Description |
|---|---|---|
| sku | str | Unique product code (e.g. VC-LONG-001) |
| name | str | Product display name |
| category | str | One of: Longevity Supplements, Premium Nutrition, Aesthetic Grooming, Lifestyle & Home |
| subcategory | str | Granular grouping (Anti-Aging, Raw Food, Bath, Bedding, etc.) |
| price | float | Retail price USD |
| cogs | float | Cost of goods sold per unit USD |
| weight_oz | int | Shipping weight in ounces |
| launched | date | Product launch date — two SKUs launched in 2024 to enable new-product cohort analysis |

### 2. `customers.csv` (~4,200 rows)
Customer master with attribution and segmentation.

| Field | Type | Description |
|---|---|---|
| customer_id | str | C10000+ |
| signup_date | date | First account creation date |
| state | str | US state code |
| acquisition_channel | str | Paid Social - Meta / Paid Search - Google / Organic Search / Influencer / Affiliate / Email/Referral / Direct / Paid Social - TikTok / Podcast Sponsorship |
| segment | str | RFM-inspired: VIP Longevity Loyalists / Aesthetic Enthusiasts / Wellness Curious / Lifestyle Buyers / Bargain Hunters / New Pet Parents / Churned |
| pet_type | str | Dog / Cat / Both |
| pet_age_bracket | str | Puppy or Kitten (<1yr) / Adult (1-7yr) / Senior (7yr+) |
| is_subscriber | bool | Active subscription customer |
| email_opt_in | bool | Marketing email consent |

### 3. `orders.csv` (~25,000 rows)
Order-level transactions with full unit economics.

| Field | Type | Description |
|---|---|---|
| order_id | str | ORD-XXXXXX |
| customer_id | str | FK → customers |
| order_date | date | |
| channel | str | Inherited from customer's acquisition channel |
| state | str | Ship-to state |
| is_subscription_order | bool | True = recurring subscription delivery |
| shipping_method | str | Standard / Expedited |
| promo_code | str | BLACK_FRIDAY / CYBER_MONDAY / MOTHERS_DAY / VDAY_PETS / SUMMER_SALE / WELCOME10 / blank |
| discount_pct | float | 0.0 – 0.25 |
| gross_revenue | float | Pre-discount revenue |
| discount_amount | float | $ discount applied |
| net_revenue | float | Post-discount revenue (the "real" revenue) |
| shipping_revenue | float | Customer-paid shipping ($9.95 std / $18.95 expedited, free over $75 or for subscribers) |
| cogs | float | Total product cost |
| fulfillment_cost | float | Pick-pack-ship cost: $3.50 base + $0.045/oz |
| payment_processing_fee | float | ~2.9% + $0.30 |
| gross_margin | float | net_revenue – cogs |
| contribution_margin | float | net_revenue – cogs – fulfillment – payment_fee |
| order_status | str | Delivered / Returned / Refunded - Partial |
| csat_score | float | 1–5, populated for delivered orders only |
| items_count | int | Total units in the order |

### 4. `order_items.csv` (~54,000 rows)
Line-item detail for SKU-level analysis.

| Field | Type | Description |
|---|---|---|
| order_id | str | FK → orders |
| customer_id | str | FK → customers |
| order_date | date | |
| sku | str | FK → products |
| product_name | str | |
| category | str | |
| subcategory | str | |
| quantity | int | |
| unit_price | float | |
| unit_cogs | float | |
| line_revenue | float | quantity × unit_price |
| line_cogs | float | quantity × unit_cogs |

### 5. `marketing_spend.csv` (318 rows: 53 months × 6 paid channels)

| Field | Type | Description |
|---|---|---|
| month | str | YYYY-MM |
| channel | str | Paid Social - Meta / Paid Search - Google / Paid Social - TikTok / Influencer / Affiliate / Podcast Sponsorship / Email/Referral |
| spend | float | USD |
| impressions | int | |
| clicks | int | |
| ctr | float | clicks / impressions |
| new_customers | int | Net new customers acquired this month from this channel |
| cac | float | spend / new_customers (blended CAC by channel-month) |

### 6. `inventory.csv` (22 rows — current snapshot)

| Field | Type | Description |
|---|---|---|
| sku | str | |
| product_name | str | |
| category | str | |
| unit_cost | float | |
| unit_price | float | |
| units_on_hand | int | Current stock |
| units_sold_90d | int | Trailing 90-day sales |
| avg_daily_velocity | float | Units/day |
| days_of_supply | float | on_hand / velocity |
| reorder_point | int | velocity × 21-day lead time |
| lead_time_days | int | 21 |
| stock_status | str | Healthy / Low Stock / Overstocked / Stockout |
| warehouse | str | Reno-NV / Atlanta-GA / NJ-Edison |

### 7. `support_tickets.csv` (~4,400 rows — ~18% of orders generate tickets)

| Field | Type | Description |
|---|---|---|
| ticket_id | str | T50000+ |
| order_id | str | FK → orders |
| customer_id | str | FK → customers |
| created_date | date | |
| ticket_type | str | Shipping Delay / Product Question / Return Request / Subscription Mgmt / Damaged Item / Billing Issue / Wrong Item Shipped / Compliment - Feedback |
| priority | str | Low / Medium / High / Urgent |
| channel | str | Email / Chat / Phone / Social DM |
| resolution_hours | float | |
| status | str | Resolved / Open |
| csat_post_resolution | float | 1–5 |

---

## Built-in storylines for analysis

The data was generated with intentional patterns so a sharp analyst can surface real insights:

1. **Channel efficiency divergence** — TikTok has the lowest CAC but smaller volume; Podcast has the highest CAC; Email/Referral is the most efficient.
2. **Segment-driven LTV gap** — VIP Longevity Loyalists order ~14×/year at 1.4× AOV; Bargain Hunters churn faster and depress margin.
3. **Subscription economics** — Subscribers get free shipping (margin hit) but order more frequently in supplements/nutrition.
4. **Product portfolio quadrants** — Longevity Supplements = highest margin, Lifestyle & Home = highest AOV but lowest margin %.
5. **Q4 holiday spike** — November–December are 35–45% above baseline.
6. **Return rate variance** — Lifestyle Buyers return at ~11% vs 6% base, and first-time buyers return at ~9%.
7. **Inventory imbalance** — Some SKUs are overstocked, some at risk of stockout. Worth a reorder plan.
8. **Cohort retention** — Newer cohorts (2024+) behave differently from 2023 vintages; this enables cohort/LTV analysis.

Built for: Emma Larroze, May 2026.
