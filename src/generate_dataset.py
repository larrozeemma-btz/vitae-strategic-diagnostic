"""
Premium Pet Ecommerce Dataset Generator
Brand: VITAE & CO. — Aesthetic & Longevity Pet Products (US National)

Designed for portfolio analysis: BizOps, Strategy, Consulting Associate
Showcases: segmentation, cohort/LTV, marketing attribution, P&L, ops, churn
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# ============================================================
# 1. PRODUCT CATALOG
# ============================================================
products = [
    # Longevity Supplements (highest margin)
    {"sku": "VC-LONG-001", "name": "Cellular Renewal Drops (NMN+)", "category": "Longevity Supplements", "subcategory": "Anti-Aging", "price": 89.00, "cogs": 18.50, "weight_oz": 2, "launched": "2022-03-15"},
    {"sku": "VC-LONG-002", "name": "Joint Vitality Complex", "category": "Longevity Supplements", "subcategory": "Mobility", "price": 64.00, "cogs": 14.20, "weight_oz": 4, "launched": "2022-01-10"},
    {"sku": "VC-LONG-003", "name": "Cognitive Clarity Chews", "category": "Longevity Supplements", "subcategory": "Cognitive", "price": 54.00, "cogs": 11.80, "weight_oz": 6, "launched": "2022-06-20"},
    {"sku": "VC-LONG-004", "name": "Senior Vitality Bundle", "category": "Longevity Supplements", "subcategory": "Bundle", "price": 179.00, "cogs": 42.00, "weight_oz": 12, "launched": "2022-09-01"},
    {"sku": "VC-LONG-005", "name": "Omega Marine Elixir", "category": "Longevity Supplements", "subcategory": "Skin & Coat", "price": 49.00, "cogs": 10.50, "weight_oz": 8, "launched": "2022-04-05"},

    # Premium Nutrition
    {"sku": "VC-NUTR-001", "name": "Heritage Beef Raw Blend (4lb)", "category": "Premium Nutrition", "subcategory": "Raw Food", "price": 78.00, "cogs": 31.00, "weight_oz": 64, "launched": "2022-01-15"},
    {"sku": "VC-NUTR-002", "name": "Wild Salmon Bowl (4lb)", "category": "Premium Nutrition", "subcategory": "Raw Food", "price": 82.00, "cogs": 33.50, "weight_oz": 64, "launched": "2022-02-01"},
    {"sku": "VC-NUTR-003", "name": "Bone Broth Reserve", "category": "Premium Nutrition", "subcategory": "Hydration", "price": 28.00, "cogs": 7.50, "weight_oz": 32, "launched": "2022-03-20"},
    {"sku": "VC-NUTR-004", "name": "Functional Treats (Adaptogens)", "category": "Premium Nutrition", "subcategory": "Treats", "price": 22.00, "cogs": 5.20, "weight_oz": 6, "launched": "2022-05-10"},
    {"sku": "VC-NUTR-005", "name": "Bio-Active Kibble Topper", "category": "Premium Nutrition", "subcategory": "Toppers", "price": 38.00, "cogs": 9.80, "weight_oz": 16, "launched": "2022-07-15"},

    # Aesthetic Grooming
    {"sku": "VC-AEST-001", "name": "Botanical Coat Serum", "category": "Aesthetic Grooming", "subcategory": "Serums", "price": 58.00, "cogs": 9.20, "weight_oz": 4, "launched": "2022-02-20"},
    {"sku": "VC-AEST-002", "name": "Hydrating Paw Balm", "category": "Aesthetic Grooming", "subcategory": "Skincare", "price": 32.00, "cogs": 5.10, "weight_oz": 2, "launched": "2022-01-25"},
    {"sku": "VC-AEST-003", "name": "Spa Shampoo & Conditioner Duo", "category": "Aesthetic Grooming", "subcategory": "Bath", "price": 48.00, "cogs": 8.50, "weight_oz": 24, "launched": "2022-04-10"},
    {"sku": "VC-AEST-004", "name": "Dental Polish Kit", "category": "Aesthetic Grooming", "subcategory": "Dental", "price": 44.00, "cogs": 7.80, "weight_oz": 4, "launched": "2022-06-01"},
    {"sku": "VC-AEST-005", "name": "Tear Stain Refining Solution", "category": "Aesthetic Grooming", "subcategory": "Skincare", "price": 36.00, "cogs": 5.50, "weight_oz": 4, "launched": "2022-08-15"},

    # Lifestyle & Home (lower margin, high AOV driver)
    {"sku": "VC-LIFE-001", "name": "Orthopedic Memory Bed (M)", "category": "Lifestyle & Home", "subcategory": "Bedding", "price": 189.00, "cogs": 72.00, "weight_oz": 120, "launched": "2022-03-01"},
    {"sku": "VC-LIFE-002", "name": "Orthopedic Memory Bed (L)", "category": "Lifestyle & Home", "subcategory": "Bedding", "price": 249.00, "cogs": 98.00, "weight_oz": 180, "launched": "2022-03-01"},
    {"sku": "VC-LIFE-003", "name": "Ceramic Slow Feeder", "category": "Lifestyle & Home", "subcategory": "Feeding", "price": 68.00, "cogs": 18.00, "weight_oz": 48, "launched": "2022-05-20"},
    {"sku": "VC-LIFE-004", "name": "Italian Leather Collar", "category": "Lifestyle & Home", "subcategory": "Accessories", "price": 124.00, "cogs": 38.00, "weight_oz": 8, "launched": "2022-07-01"},
    {"sku": "VC-LIFE-005", "name": "Hand-Loomed Throw Blanket", "category": "Lifestyle & Home", "subcategory": "Bedding", "price": 98.00, "cogs": 32.00, "weight_oz": 32, "launched": "2022-09-10"},

    # New 2024 launches (test cohort)
    {"sku": "VC-LONG-006", "name": "Microbiome Restore (Probiotics)", "category": "Longevity Supplements", "subcategory": "Gut Health", "price": 72.00, "cogs": 15.50, "weight_oz": 4, "launched": "2024-03-15"},
    {"sku": "VC-AEST-006", "name": "Anti-Shed Coat Treatment", "category": "Aesthetic Grooming", "subcategory": "Serums", "price": 52.00, "cogs": 8.80, "weight_oz": 6, "launched": "2024-05-01"},
]

products_df = pd.DataFrame(products)

# ============================================================
# 2. CUSTOMERS — segmented realistically
# ============================================================
N_CUSTOMERS = 4200

# US states with realistic premium-pet skew (CA, NY, TX, FL, MA dominate)
state_weights = {
    'CA': 0.18, 'NY': 0.11, 'TX': 0.09, 'FL': 0.08, 'MA': 0.06,
    'WA': 0.05, 'IL': 0.05, 'CO': 0.04, 'NJ': 0.04, 'VA': 0.03,
    'GA': 0.03, 'PA': 0.03, 'OR': 0.03, 'AZ': 0.03, 'NC': 0.03,
    'CT': 0.02, 'MD': 0.02, 'MN': 0.02, 'MI': 0.02, 'TN': 0.01,
    'OH': 0.01, 'NV': 0.01, 'UT': 0.01, 'Other': 0.01
}
states = list(state_weights.keys())
state_probs = np.array(list(state_weights.values()))
state_probs = state_probs / state_probs.sum()

# Acquisition channels
channels = {
    'Paid Social - Meta': 0.28,
    'Paid Search - Google': 0.18,
    'Organic Search': 0.12,
    'Influencer / Affiliate': 0.14,
    'Email/Referral': 0.10,
    'Direct': 0.09,
    'Paid Social - TikTok': 0.06,
    'Podcast Sponsorship': 0.03,
}
channel_list = list(channels.keys())
channel_probs = np.array(list(channels.values()))
channel_probs = channel_probs / channel_probs.sum()

# Customer segments (RFM-inspired)
segments = {
    'VIP Longevity Loyalists': 0.08,    # high LTV, supplements subscribers
    'Aesthetic Enthusiasts': 0.15,       # grooming-focused, premium
    'Wellness Curious': 0.32,            # one-time supplement triers
    'Lifestyle Buyers': 0.18,            # beds/accessories, lower frequency
    'Bargain Hunters': 0.12,             # discount-driven
    'New Pet Parents': 0.10,             # recent acquisition, exploring
    'Churned': 0.05,
}

pet_types = ['Dog', 'Dog', 'Dog', 'Dog', 'Cat', 'Cat', 'Cat', 'Both']  # ~62% dog only
pet_age_brackets = ['Puppy/Kitten (<1yr)', 'Adult (1-7yr)', 'Senior (7yr+)']
pet_age_weights = [0.18, 0.52, 0.30]

customers = []
for i in range(N_CUSTOMERS):
    cust_id = f"C{10000+i}"
    state = np.random.choice(states, p=state_probs)
    channel = np.random.choice(channel_list, p=channel_probs)
    segment_probs = np.array(list(segments.values()))
    segment_probs = segment_probs / segment_probs.sum()
    segment = np.random.choice(list(segments.keys()), p=segment_probs)

    # First order date — weighted toward 2023-2024 with growth
    months_ago_probs = np.array([0.04]*6 + [0.035]*6 + [0.025]*12 + [0.018]*16)
    months_ago_probs = months_ago_probs / months_ago_probs.sum()
    months_ago = np.random.choice(range(0, 40), p=months_ago_probs)
    signup_date = datetime(2026, 5, 1) - timedelta(days=int(months_ago*30) + random.randint(0,29))

    pet_type = random.choice(pet_types)
    pet_age = np.random.choice(pet_age_brackets, p=pet_age_weights)

    # Subscription status — VIPs & Wellness more likely
    sub_rate = {'VIP Longevity Loyalists': 0.85, 'Aesthetic Enthusiasts': 0.35,
                'Wellness Curious': 0.20, 'Lifestyle Buyers': 0.08,
                'Bargain Hunters': 0.05, 'New Pet Parents': 0.25, 'Churned': 0.0}
    is_subscriber = random.random() < sub_rate[segment]

    customers.append({
        'customer_id': cust_id,
        'signup_date': signup_date.strftime('%Y-%m-%d'),
        'state': state if state != 'Other' else random.choice(['NM','ID','MT','WY','VT']),
        'acquisition_channel': channel,
        'segment': segment,
        'pet_type': pet_type,
        'pet_age_bracket': pet_age,
        'is_subscriber': is_subscriber,
        'email_opt_in': random.random() < 0.78,
    })

customers_df = pd.DataFrame(customers)

# ============================================================
# 3. ORDERS — Realistic seasonality, AOV by segment, churn
# ============================================================
print("Generating orders...")

orders = []
order_items = []
order_id_counter = 100000

# Segment behavior parameters
segment_behavior = {
    'VIP Longevity Loyalists': {'orders_per_yr': 14, 'aov_mult': 1.4, 'cat_pref': 'Longevity Supplements'},
    'Aesthetic Enthusiasts':   {'orders_per_yr': 8,  'aov_mult': 1.2, 'cat_pref': 'Aesthetic Grooming'},
    'Wellness Curious':        {'orders_per_yr': 3,  'aov_mult': 1.0, 'cat_pref': 'Longevity Supplements'},
    'Lifestyle Buyers':        {'orders_per_yr': 2,  'aov_mult': 1.6, 'cat_pref': 'Lifestyle & Home'},
    'Bargain Hunters':         {'orders_per_yr': 4,  'aov_mult': 0.7, 'cat_pref': None},
    'New Pet Parents':         {'orders_per_yr': 5,  'aov_mult': 1.1, 'cat_pref': None},
    'Churned':                 {'orders_per_yr': 1,  'aov_mult': 0.8, 'cat_pref': None},
}

# Seasonal multipliers (Nov-Dec spike, summer dip, slight bump in Spring grooming)
month_seasonality = {1:0.92, 2:0.88, 3:1.02, 4:1.05, 5:1.08, 6:0.95,
                     7:0.90, 8:0.93, 9:1.00, 10:1.05, 11:1.35, 12:1.45}

# Promotion windows (real promo events)
promo_events = {
    '2023-11-24': ('BLACK_FRIDAY', 0.20),
    '2023-11-27': ('CYBER_MONDAY', 0.25),
    '2024-05-12': ('MOTHERS_DAY', 0.15),
    '2024-11-29': ('BLACK_FRIDAY', 0.20),
    '2024-12-02': ('CYBER_MONDAY', 0.25),
    '2025-02-14': ('VDAY_PETS', 0.10),
    '2025-07-04': ('SUMMER_SALE', 0.15),
    '2025-11-28': ('BLACK_FRIDAY', 0.22),
    '2025-12-01': ('CYBER_MONDAY', 0.25),
    '2026-02-14': ('VDAY_PETS', 0.10),
}

for _, cust in customers_df.iterrows():
    signup = datetime.strptime(cust['signup_date'], '%Y-%m-%d')
    behavior = segment_behavior[cust['segment']]
    days_active = (datetime(2026, 5, 1) - signup).days
    if days_active < 1:
        continue

    # Expected orders for this customer
    base_orders = behavior['orders_per_yr'] * (days_active / 365.0)
    n_orders = max(1, int(np.random.poisson(base_orders)))

    # Churn logic — if Churned segment, only first ~30% of timeline
    if cust['segment'] == 'Churned':
        n_orders = random.randint(1, 3)
        churn_cutoff_days = int(days_active * 0.4)
    else:
        churn_cutoff_days = days_active

    for o in range(n_orders):
        day_offset = random.randint(0, max(1, churn_cutoff_days))
        order_date = signup + timedelta(days=day_offset)
        if order_date > datetime(2026, 5, 1):
            continue

        # Seasonal boost
        season_mult = month_seasonality[order_date.month]
        if random.random() > season_mult / 1.45:  # higher mult = more likely kept
            if random.random() > 0.6:
                continue

        # Promo check
        promo_code = None
        discount_pct = 0.0
        date_key = order_date.strftime('%Y-%m-%d')
        for promo_start, (code, pct) in promo_events.items():
            promo_dt = datetime.strptime(promo_start, '%Y-%m-%d')
            if 0 <= (order_date - promo_dt).days <= 4:
                promo_code = code
                discount_pct = pct
                break
        if not promo_code and cust['segment'] == 'Bargain Hunters' and random.random() < 0.45:
            promo_code = 'WELCOME10'
            discount_pct = 0.10

        # Pick items — bias toward segment preference
        n_items = np.random.choice([1, 2, 3, 4, 5], p=[0.35, 0.32, 0.18, 0.10, 0.05])
        order_id_counter += 1
        order_id = f"ORD-{order_id_counter}"

        # Subscription orders skew to supplements/nutrition
        is_sub_order = cust['is_subscriber'] and random.random() < 0.55

        chosen_skus = []
        for _ in range(n_items):
            if is_sub_order:
                eligible = products_df[products_df['category'].isin(['Longevity Supplements', 'Premium Nutrition'])]
            elif behavior['cat_pref'] and random.random() < 0.55:
                eligible = products_df[products_df['category'] == behavior['cat_pref']]
            else:
                eligible = products_df

            # Filter by launch date
            eligible = eligible[pd.to_datetime(eligible['launched']) <= order_date]
            if len(eligible) == 0:
                continue
            sku_row = eligible.sample(1).iloc[0]
            qty = np.random.choice([1, 1, 1, 2, 2, 3], p=[0.55, 0.0, 0.0, 0.30, 0.0, 0.15])
            chosen_skus.append((sku_row, qty))

        if not chosen_skus:
            continue

        gross_revenue = sum(s['price'] * q for s, q in chosen_skus)
        gross_revenue *= behavior['aov_mult']
        discount_amt = round(gross_revenue * discount_pct, 2)
        net_revenue = round(gross_revenue - discount_amt, 2)

        # Shipping — free over $75 (their threshold), else $9.95; expedited 8% of orders
        shipping_method = 'Standard'
        if net_revenue >= 75:
            shipping_cost = 0.0
        else:
            shipping_cost = 9.95
        if random.random() < 0.08:
            shipping_method = 'Expedited'
            shipping_cost = 18.95
        # Subscription = always free
        if is_sub_order:
            shipping_cost = 0.0

        total_cogs = sum(s['cogs'] * q for s, q in chosen_skus) * behavior['aov_mult']
        # Fulfillment cost — variable by weight
        total_weight = sum(s['weight_oz'] * q for s, q in chosen_skus)
        fulfillment_cost = round(3.50 + total_weight * 0.045, 2)
        # Payment processing ~ 2.9% + $0.30
        payment_fee = round(net_revenue * 0.029 + 0.30, 2)

        # Returns — 6% base, higher for first-time buyers and Lifestyle
        return_rate = 0.06
        if cust['segment'] == 'Lifestyle Buyers':
            return_rate = 0.11
        if o == 0:
            return_rate += 0.03
        is_returned = random.random() < return_rate
        return_status = 'Returned' if is_returned else ('Refunded - Partial' if random.random() < 0.02 else 'Delivered')

        # CSAT score for delivered orders
        csat = None
        if return_status == 'Delivered':
            base_csat = 4.6 if cust['segment'] in ['VIP Longevity Loyalists', 'Aesthetic Enthusiasts'] else 4.3
            csat = round(np.clip(np.random.normal(base_csat, 0.5), 1, 5), 1)

        orders.append({
            'order_id': order_id,
            'customer_id': cust['customer_id'],
            'order_date': order_date.strftime('%Y-%m-%d'),
            'channel': cust['acquisition_channel'],
            'state': cust['state'],
            'is_subscription_order': is_sub_order,
            'shipping_method': shipping_method,
            'promo_code': promo_code if promo_code else '',
            'discount_pct': round(discount_pct, 3),
            'gross_revenue': round(gross_revenue, 2),
            'discount_amount': discount_amt,
            'net_revenue': net_revenue,
            'shipping_revenue': shipping_cost if not is_sub_order and net_revenue < 75 else 0.0,
            'cogs': round(total_cogs, 2),
            'fulfillment_cost': fulfillment_cost,
            'payment_processing_fee': payment_fee,
            'gross_margin': round(net_revenue - total_cogs, 2),
            'contribution_margin': round(net_revenue - total_cogs - fulfillment_cost - payment_fee, 2),
            'order_status': return_status,
            'csat_score': csat,
            'items_count': sum(q for _, q in chosen_skus),
        })

        for sku_row, qty in chosen_skus:
            order_items.append({
                'order_id': order_id,
                'customer_id': cust['customer_id'],
                'order_date': order_date.strftime('%Y-%m-%d'),
                'sku': sku_row['sku'],
                'product_name': sku_row['name'],
                'category': sku_row['category'],
                'subcategory': sku_row['subcategory'],
                'quantity': qty,
                'unit_price': sku_row['price'],
                'unit_cogs': sku_row['cogs'],
                'line_revenue': round(sku_row['price'] * qty, 2),
                'line_cogs': round(sku_row['cogs'] * qty, 2),
            })

orders_df = pd.DataFrame(orders)
order_items_df = pd.DataFrame(order_items)

print(f"Generated {len(customers_df)} customers, {len(orders_df)} orders, {len(order_items_df)} line items")

# ============================================================
# 4. MARKETING SPEND — monthly by channel
# ============================================================
print("Generating marketing spend...")

months = pd.date_range('2022-01-01', '2026-05-01', freq='MS')
mkt_rows = []

channel_baseline = {
    'Paid Social - Meta':      {'cac_base': 58, 'share': 0.28},
    'Paid Search - Google':    {'cac_base': 72, 'share': 0.18},
    'Paid Social - TikTok':    {'cac_base': 51, 'share': 0.06},
    'Influencer / Affiliate':  {'cac_base': 62, 'share': 0.14},
    'Podcast Sponsorship':     {'cac_base': 98, 'share': 0.03},
    'Email/Referral':          {'cac_base': 18, 'share': 0.10},
}

for m_idx, month in enumerate(months):
    seasonal = month_seasonality[month.month]
    month_str = month.strftime('%Y-%m')
    for ch, params in channel_baseline.items():
        # New customers acquired this channel-month (the real driver)
        new_custs = customers_df[
            (customers_df['acquisition_channel'] == ch) &
            (customers_df['signup_date'].str.startswith(month_str))
        ].shape[0]
        # CAC drifts up ~0.4%/month (rising acquisition costs storyline) with noise
        cac = params['cac_base'] * (1 + 0.004) ** m_idx * np.random.uniform(0.9, 1.12)
        # Spend = customers won * CAC, plus substantial always-on brand/retargeting spend
        # Scaled so total marketing lands ~25-30% of revenue (realistic DTC growth mode)
        always_on = params['cac_base'] * params['share'] * 950  # baseline brand spend
        spend = new_custs * cac + always_on * seasonal * np.random.uniform(0.85, 1.15)
        impressions = int(spend * np.random.uniform(180, 320))
        clicks = int(impressions * np.random.uniform(0.012, 0.028))
        cac_reported = round(spend / new_custs, 2) if new_custs > 0 else 0
        mkt_rows.append({
            'month': month_str,
            'channel': ch,
            'spend': round(spend, 2),
            'impressions': impressions,
            'clicks': clicks,
            'ctr': round(clicks/impressions, 4) if impressions else 0,
            'new_customers': new_custs,
            'cac': cac_reported,
        })

marketing_df = pd.DataFrame(mkt_rows)

# ============================================================
# 5. INVENTORY & OPERATIONS
# ============================================================
print("Generating inventory snapshot...")

inventory_rows = []
for _, p in products_df.iterrows():
    # Compute sales velocity from order_items
    sku_items = order_items_df[order_items_df['sku'] == p['sku']]
    last_90 = order_items_df[
        (order_items_df['sku'] == p['sku']) &
        (pd.to_datetime(order_items_df['order_date']) >= datetime(2026, 2, 1))
    ]
    units_90d = int(last_90['quantity'].sum())
    avg_daily = round(units_90d / 90, 2)
    on_hand = int(np.random.uniform(50, 800)) if avg_daily > 0 else int(np.random.uniform(10, 200))
    days_of_supply = round(on_hand / avg_daily, 1) if avg_daily > 0 else 999
    reorder_point = int(avg_daily * 21)  # 21-day lead time
    status = 'Healthy'
    if days_of_supply < 14:
        status = 'Low Stock'
    elif days_of_supply > 120:
        status = 'Overstocked'
    if on_hand == 0:
        status = 'Stockout'

    inventory_rows.append({
        'sku': p['sku'],
        'product_name': p['name'],
        'category': p['category'],
        'unit_cost': p['cogs'],
        'unit_price': p['price'],
        'units_on_hand': on_hand,
        'units_sold_90d': units_90d,
        'avg_daily_velocity': avg_daily,
        'days_of_supply': days_of_supply,
        'reorder_point': reorder_point,
        'lead_time_days': 21,
        'stock_status': status,
        'warehouse': random.choice(['Reno-NV', 'Atlanta-GA', 'NJ-Edison']),
    })

inventory_df = pd.DataFrame(inventory_rows)

# ============================================================
# 6. CUSTOMER SUPPORT TICKETS
# ============================================================
print("Generating support tickets...")

ticket_types = {
    'Shipping Delay': 0.32,
    'Product Question': 0.18,
    'Return Request': 0.15,
    'Subscription Mgmt': 0.12,
    'Damaged Item': 0.08,
    'Billing Issue': 0.07,
    'Wrong Item Shipped': 0.04,
    'Compliment / Feedback': 0.04,
}
ticket_priorities = ['Low', 'Medium', 'High', 'Urgent']
ticket_channels = ['Email', 'Chat', 'Phone', 'Social DM']

tickets = []
# About 18% of orders generate a ticket
sample_orders = orders_df.sample(frac=0.18, random_state=42)
for i, (_, o) in enumerate(sample_orders.iterrows()):
    tt_probs = np.array(list(ticket_types.values()))
    tt_probs = tt_probs / tt_probs.sum()
    t_type = np.random.choice(list(ticket_types.keys()), p=tt_probs)
    priority = np.random.choice(ticket_priorities, p=[0.45, 0.35, 0.15, 0.05])
    ch = np.random.choice(ticket_channels, p=[0.55, 0.28, 0.10, 0.07])
    created = datetime.strptime(o['order_date'], '%Y-%m-%d') + timedelta(days=random.randint(1, 14))
    if created > datetime(2026, 5, 1):
        continue
    resolution_hrs = np.random.exponential(scale=18)
    if priority == 'Urgent':
        resolution_hrs = np.random.exponential(scale=4)
    elif priority == 'High':
        resolution_hrs = np.random.exponential(scale=10)
    resolution_hrs = round(min(resolution_hrs, 240), 1)
    status = 'Resolved' if random.random() < 0.92 else 'Open'

    tickets.append({
        'ticket_id': f"T{50000+i}",
        'order_id': o['order_id'],
        'customer_id': o['customer_id'],
        'created_date': created.strftime('%Y-%m-%d'),
        'ticket_type': t_type,
        'priority': priority,
        'channel': ch,
        'resolution_hours': resolution_hrs,
        'status': status,
        'csat_post_resolution': round(np.clip(np.random.normal(4.2, 0.7), 1, 5), 1) if status == 'Resolved' else None,
    })

tickets_df = pd.DataFrame(tickets)

# ============================================================
# 7. WRITE ALL TO CSV (for Python work) + ONE XLSX (multi-sheet)
# ============================================================
import os
os.makedirs('/home/claude/vitae-portfolio/data', exist_ok=True)
OUTDIR = '/home/claude/vitae-portfolio/data'

products_df.to_csv('/home/claude/vitae-portfolio/data/products.csv', index=False)
customers_df.to_csv('/home/claude/vitae-portfolio/data/customers.csv', index=False)
orders_df.to_csv('/home/claude/vitae-portfolio/data/orders.csv', index=False)
order_items_df.to_csv('/home/claude/vitae-portfolio/data/order_items.csv', index=False)
marketing_df.to_csv('/home/claude/vitae-portfolio/data/marketing_spend.csv', index=False)
inventory_df.to_csv('/home/claude/vitae-portfolio/data/inventory.csv', index=False)
tickets_df.to_csv('/home/claude/vitae-portfolio/data/support_tickets.csv', index=False)

# Also write a single XLSX with all sheets
with pd.ExcelWriter('/home/claude/vitae-portfolio/data/VITAE_CO_dataset.xlsx', engine='openpyxl') as writer:
    products_df.to_excel(writer, sheet_name='products', index=False)
    customers_df.to_excel(writer, sheet_name='customers', index=False)
    orders_df.to_excel(writer, sheet_name='orders', index=False)
    order_items_df.to_excel(writer, sheet_name='order_items', index=False)
    marketing_df.to_excel(writer, sheet_name='marketing_spend', index=False)
    inventory_df.to_excel(writer, sheet_name='inventory', index=False)
    tickets_df.to_excel(writer, sheet_name='support_tickets', index=False)

print("\n=== DATASET SUMMARY ===")
print(f"Products:        {len(products_df):,} SKUs")
print(f"Customers:       {len(customers_df):,}")
print(f"Orders:          {len(orders_df):,}")
print(f"Order line items:{len(order_items_df):,}")
print(f"Marketing rows:  {len(marketing_df):,} (months × channels)")
print(f"Inventory rows:  {len(inventory_df):,}")
print(f"Support tickets: {len(tickets_df):,}")
print(f"\nGMV total:       ${orders_df['gross_revenue'].sum():,.0f}")
print(f"Net Revenue:     ${orders_df['net_revenue'].sum():,.0f}")
print(f"Avg AOV:         ${orders_df['net_revenue'].mean():,.2f}")
print(f"Total Mkt Spend: ${marketing_df['spend'].sum():,.0f}")
print(f"Date range:      {orders_df['order_date'].min()} → {orders_df['order_date'].max()}")
