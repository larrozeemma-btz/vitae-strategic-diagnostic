"""
VITAE & CO. — Strategic Diagnostic
Full analytical workpaper: business diagnostic, customer/growth, product, ops, strategy.

Author: Emma Larroze
Generates all figures into outputs/figures/ and a metrics summary into outputs/.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import Rectangle
import json
import os

# ----------------------------------------------------------------------
# Brand palette (McKinsey-style minimalism)
# ----------------------------------------------------------------------
NAVY   = '#1B2845'
GOLD   = '#C9A961'
TEAL   = '#2A7F8E'
GREY   = '#8A8D91'
LGREY  = '#D9DBDD'
RED    = '#B23A48'
GREEN  = '#3A7D5D'

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.titleweight': 'bold',
    'axes.labelcolor': NAVY,
    'axes.edgecolor': LGREY,
    'axes.linewidth': 0.8,
    'axes.grid': True,
    'grid.color': '#EFEFEF',
    'grid.linewidth': 0.8,
    'xtick.color': GREY,
    'ytick.color': GREY,
    'text.color': NAVY,
    'figure.dpi': 110,
    'savefig.dpi': 150,
    'savefig.bbox': 'tight',
})

FIG = '/home/claude/vitae-portfolio/outputs/figures'
OUT = '/home/claude/vitae-portfolio/outputs'
DATA = '/home/claude/vitae-portfolio/data'
os.makedirs(FIG, exist_ok=True)

# ----------------------------------------------------------------------
# Load
# ----------------------------------------------------------------------
products   = pd.read_csv(f'{DATA}/products.csv', parse_dates=['launched'])
customers  = pd.read_csv(f'{DATA}/customers.csv', parse_dates=['signup_date'])
orders     = pd.read_csv(f'{DATA}/orders.csv', parse_dates=['order_date'])
items      = pd.read_csv(f'{DATA}/order_items.csv', parse_dates=['order_date'])
marketing  = pd.read_csv(f'{DATA}/marketing_spend.csv')
inventory  = pd.read_csv(f'{DATA}/inventory.csv')
tickets    = pd.read_csv(f'{DATA}/support_tickets.csv', parse_dates=['created_date'])

orders['ym'] = orders['order_date'].dt.to_period('M').astype(str)
orders['year'] = orders['order_date'].dt.year
metrics = {}

def fmt_usd(x, pos=None):
    if abs(x) >= 1e6: return f'${x/1e6:.1f}M'
    if abs(x) >= 1e3: return f'${x/1e3:.0f}K'
    return f'${x:.0f}'

def save(fig, name):
    fig.savefig(f'{FIG}/{name}.png', facecolor='white')
    plt.close(fig)
    print(f'  saved {name}.png')

# ======================================================================
# PART 1 — BUSINESS DIAGNOSTIC
# ======================================================================
print("PART 1 — Business Diagnostic")

delivered = orders[orders['order_status'] != 'Returned'].copy()
gmv = orders['gross_revenue'].sum()
net_rev = orders['net_revenue'].sum()
aov = orders['net_revenue'].mean()
gm_pct = orders['gross_margin'].sum() / net_rev
cm_pct = orders['contribution_margin'].sum() / net_rev
total_spend = marketing['spend'].sum()
total_new = marketing['new_customers'].sum()
blended_cac = total_spend / total_new if total_new else 0

metrics['headline'] = {
    'gmv': round(gmv), 'net_revenue': round(net_rev), 'aov': round(aov, 2),
    'gross_margin_pct': round(gm_pct, 4), 'contribution_margin_pct': round(cm_pct, 4),
    'total_marketing_spend': round(total_spend), 'blended_cac': round(blended_cac, 2),
    'n_customers': len(customers), 'n_orders': len(orders),
}

# --- 1a. Monthly net revenue + contribution margin trend (last 24 mo) ---
monthly = orders.groupby('ym').agg(
    net_revenue=('net_revenue', 'sum'),
    contribution_margin=('contribution_margin', 'sum'),
    orders=('order_id', 'count'),
).reset_index()
monthly['cm_pct'] = monthly['contribution_margin'] / monthly['net_revenue']
monthly_recent = monthly.tail(24).copy()

fig, ax1 = plt.subplots(figsize=(11, 5))
x = range(len(monthly_recent))
ax1.bar(x, monthly_recent['net_revenue'], color=NAVY, alpha=0.85, label='Net Revenue')
ax1.set_ylabel('Net Revenue', color=NAVY)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
ax2 = ax1.twinx()
ax2.plot(x, monthly_recent['cm_pct']*100, color=GOLD, marker='o', lw=2.2, label='Contribution Margin %')
ax2.set_ylabel('Contribution Margin %', color=GOLD)
ax2.grid(False)
ax1.set_xticks(list(x))
ax1.set_xticklabels(monthly_recent['ym'], rotation=45, ha='right', fontsize=8)
ax1.set_title('Revenue scaled steadily, but contribution margin compressed in early 2026', loc='left', color=NAVY)
fig.tight_layout()
save(fig, '01_revenue_margin_trend')

# --- 1b. YoY comparison ---
yoy = orders.groupby('year').agg(
    net_revenue=('net_revenue','sum'),
    orders=('order_id','count'),
    aov=('net_revenue','mean'),
    cm=('contribution_margin','sum'),
).reset_index()
yoy['cm_pct'] = yoy['cm'] / yoy['net_revenue']
metrics['yoy'] = yoy.round(2).to_dict('records')

fig, ax = plt.subplots(figsize=(9,5))
full_years = yoy[yoy['year'].isin([2023,2024,2025])]
bars = ax.bar(full_years['year'].astype(str), full_years['net_revenue'], color=[LGREY, TEAL, NAVY])
for b, v in zip(bars, full_years['net_revenue']):
    ax.text(b.get_x()+b.get_width()/2, v, fmt_usd(v), ha='center', va='bottom', fontweight='bold', color=NAVY)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
ax.set_title('Net revenue grew 3.0x from 2023 to 2024, then 1.98x into 2025', loc='left')
ax.set_ylabel('Net Revenue')
save(fig, '02_yoy_revenue')

# ======================================================================
# PART 2 — CUSTOMER & GROWTH
# ======================================================================
print("PART 2 — Customer & Growth")

# --- 2a. Segment economics (validated from data, not label) ---
cust_orders = orders.groupby('customer_id').agg(
    orders=('order_id','count'),
    net_revenue=('net_revenue','sum'),
    contribution=('contribution_margin','sum'),
    aov=('net_revenue','mean'),
).reset_index()
cust_orders = cust_orders.merge(customers[['customer_id','segment','acquisition_channel','is_subscriber']], on='customer_id')

seg = cust_orders.groupby('segment').agg(
    customers=('customer_id','count'),
    total_revenue=('net_revenue','sum'),
    total_contribution=('contribution','sum'),
    avg_orders=('orders','mean'),
    avg_ltv=('net_revenue','mean'),
).reset_index().sort_values('total_revenue', ascending=False)
seg['rev_share'] = seg['total_revenue']/seg['total_revenue'].sum()
seg['cust_share'] = seg['customers']/seg['customers'].sum()
metrics['segments'] = seg.round(2).to_dict('records')

fig, ax = plt.subplots(figsize=(11,5.5))
y = range(len(seg))
ax.barh(y, seg['rev_share']*100, color=NAVY, alpha=0.85, label='% of Revenue')
ax.barh(y, seg['cust_share']*100, color=GOLD, alpha=0.7, height=0.45, label='% of Customers')
ax.set_yticks(list(y)); ax.set_yticklabels(seg['segment'])
ax.invert_yaxis()
ax.set_xlabel('Share (%)')
ax.legend(loc='lower right', frameon=False)
ax.set_title('VIP & Aesthetic segments punch above their weight: high revenue share vs customer share', loc='left', fontsize=12)
save(fig, '03_segment_value')

# --- 2b. LTV by segment ---
fig, ax = plt.subplots(figsize=(10,5))
seg_ltv = seg.sort_values('avg_ltv', ascending=True)
bars = ax.barh(seg_ltv['segment'], seg_ltv['avg_ltv'], color=TEAL)
for b,v in zip(bars, seg_ltv['avg_ltv']):
    ax.text(v, b.get_y()+b.get_height()/2, f' ${v:,.0f}', va='center', fontweight='bold', fontsize=9, color=NAVY)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
ax.set_title('VIP Longevity Loyalists generate the highest lifetime value per customer', loc='left')
ax.set_xlabel('Average Lifetime Net Revenue per Customer')
save(fig, '04_ltv_by_segment')

# --- 2c. CAC & marketing efficiency by channel ---
mkt_ch = marketing.groupby('channel').agg(
    spend=('spend','sum'),
    new_customers=('new_customers','sum'),
).reset_index()
mkt_ch['cac'] = mkt_ch['spend']/mkt_ch['new_customers']
# revenue by acquisition channel
rev_ch = orders.groupby('channel').agg(net_revenue=('net_revenue','sum')).reset_index()
mkt_ch = mkt_ch.merge(rev_ch, on='channel', how='left')
mkt_ch['roas'] = mkt_ch['net_revenue']/mkt_ch['spend']
mkt_ch = mkt_ch.sort_values('cac')
metrics['channels'] = mkt_ch.round(2).to_dict('records')

fig, ax = plt.subplots(figsize=(11,5))
colors = [GREEN if c < blended_cac else RED for c in mkt_ch['cac']]
bars = ax.bar(mkt_ch['channel'], mkt_ch['cac'], color=colors)
ax.axhline(blended_cac, color=NAVY, ls='--', lw=1.3)
ax.text(len(mkt_ch)-0.5, blended_cac, f' Blended CAC ${blended_cac:,.0f}', va='bottom', ha='right', color=NAVY, fontsize=9, fontweight='bold')
for b,v in zip(bars, mkt_ch['cac']):
    ax.text(b.get_x()+b.get_width()/2, v, f'${v:,.0f}', ha='center', va='bottom', fontsize=8, color=NAVY)
ax.set_xticks(range(len(mkt_ch)))
ax.set_xticklabels(mkt_ch['channel'], rotation=30, ha='right', fontsize=8)
ax.set_ylabel('Customer Acquisition Cost')
ax.set_title('Email/Referral and TikTok acquire below blended CAC; Podcast is the costliest channel', loc='left', fontsize=11.5)
save(fig, '05_cac_by_channel')

# --- 2d. Cohort retention heatmap ---
first_order = orders.groupby('customer_id')['order_date'].min().reset_index()
first_order.columns = ['customer_id','cohort_date']
first_order['cohort'] = first_order['cohort_date'].dt.to_period('M')
oc = orders.merge(first_order, on='customer_id')
oc['order_period'] = oc['order_date'].dt.to_period('M')
oc['months_since'] = (oc['order_period'] - oc['cohort']).apply(lambda x: x.n)
# Use cohorts from 2024-01 onward, first 12 months
cohort_pivot = oc[oc['cohort'] >= '2024-01'].pivot_table(
    index='cohort', columns='months_since', values='customer_id', aggfunc='nunique')
cohort_size = cohort_pivot[0]
retention = cohort_pivot.divide(cohort_size, axis=0)
retention = retention.iloc[:18, :13]  # 18 cohorts, 12 months

fig, ax = plt.subplots(figsize=(12,7))
im = ax.imshow(retention.values, cmap='YlGnBu', aspect='auto', vmin=0, vmax=0.5)
ax.set_xticks(range(len(retention.columns)))
ax.set_xticklabels(retention.columns)
ax.set_yticks(range(len(retention.index)))
ax.set_yticklabels([str(c) for c in retention.index], fontsize=8)
ax.set_xlabel('Months Since First Purchase')
ax.set_title('Cohort retention: month-1 repeat rate is the key leverage point', loc='left')
for i in range(len(retention.index)):
    for j in range(len(retention.columns)):
        v = retention.values[i,j]
        if not np.isnan(v):
            ax.text(j, i, f'{v*100:.0f}', ha='center', va='center', fontsize=6.5,
                    color='white' if v>0.25 else NAVY)
cbar = fig.colorbar(im, ax=ax, fraction=0.025)
cbar.set_label('Retention %')
save(fig, '06_cohort_retention')

# --- 2e. Subscriber vs non-subscriber economics ---
sub_econ = cust_orders.groupby('is_subscriber').agg(
    customers=('customer_id','count'),
    avg_ltv=('net_revenue','mean'),
    avg_orders=('orders','mean'),
    avg_contribution=('contribution','mean'),
).reset_index()
sub_econ['label'] = sub_econ['is_subscriber'].map({True:'Subscriber', False:'Non-Subscriber'})
metrics['subscription'] = sub_econ.round(2).to_dict('records')

fig, axes = plt.subplots(1,2, figsize=(11,4.5))
axes[0].bar(sub_econ['label'], sub_econ['avg_ltv'], color=[GREY, GOLD])
axes[0].set_title('Avg Lifetime Revenue', loc='left', fontsize=11)
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
for i,v in enumerate(sub_econ['avg_ltv']):
    axes[0].text(i, v, f'${v:,.0f}', ha='center', va='bottom', fontweight='bold')
axes[1].bar(sub_econ['label'], sub_econ['avg_orders'], color=[GREY, TEAL])
axes[1].set_title('Avg Orders per Customer', loc='left', fontsize=11)
for i,v in enumerate(sub_econ['avg_orders']):
    axes[1].text(i, v, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')
fig.suptitle('Subscribers are worth multiples of one-time buyers — the core growth flywheel',
             x=0.02, ha='left', fontsize=12, fontweight='bold', color=NAVY)
fig.tight_layout()
save(fig, '07_subscription_economics')

# ======================================================================
# PART 3 — PRODUCT & MERCHANDISING
# ======================================================================
print("PART 3 — Product & Merchandising")

# --- 3a. Category profitability ---
cat = items.merge(orders[['order_id','order_status']], on='order_id')
cat_prof = items.groupby('category').agg(
    revenue=('line_revenue','sum'),
    cogs=('line_cogs','sum'),
    units=('quantity','sum'),
).reset_index()
cat_prof['gross_margin'] = cat_prof['revenue']-cat_prof['cogs']
cat_prof['gm_pct'] = cat_prof['gross_margin']/cat_prof['revenue']
cat_prof = cat_prof.sort_values('revenue', ascending=False)
metrics['categories'] = cat_prof.round(2).to_dict('records')

fig, ax1 = plt.subplots(figsize=(10,5))
xc = range(len(cat_prof))
ax1.bar(xc, cat_prof['revenue'], color=NAVY, alpha=0.85)
ax1.set_ylabel('Revenue')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_usd))
ax2 = ax1.twinx()
ax2.plot(xc, cat_prof['gm_pct']*100, color=GOLD, marker='o', lw=2.2)
ax2.set_ylabel('Gross Margin %', color=GOLD)
ax2.grid(False); ax2.set_ylim(0, 100)
ax1.set_xticks(list(xc)); ax1.set_xticklabels(cat_prof['category'], rotation=15, ha='right', fontsize=9)
ax1.set_title('Longevity Supplements: smaller revenue base but the highest-margin engine', loc='left', fontsize=11.5)
fig.tight_layout()
save(fig, '08_category_profitability')

# --- 3b. SKU BCG matrix (growth vs margin, bubble = revenue) ---
sku_rev = items.groupby('sku').agg(revenue=('line_revenue','sum'), cogs=('line_cogs','sum')).reset_index()
sku_rev['gm_pct'] = (sku_rev['revenue']-sku_rev['cogs'])/sku_rev['revenue']
# growth: H2 vs H1 of trailing 12 months
recent = items[items['order_date'] >= '2025-05-01'].copy()
recent['half'] = np.where(recent['order_date'] < '2025-11-01', 'H1', 'H2')
growth = recent.pivot_table(index='sku', columns='half', values='line_revenue', aggfunc='sum').fillna(0)
growth['growth'] = np.where(growth.get('H1',0)>0, (growth.get('H2',0)-growth.get('H1',0))/growth.get('H1',0), 0)
sku_rev = sku_rev.merge(growth[['growth']], on='sku', how='left').merge(products[['sku','name','category']], on='sku')
sku_rev['growth'] = sku_rev['growth'].clip(-0.6, 1.2).fillna(0)
metrics['sku_matrix'] = sku_rev.round(3).to_dict('records')

cat_colors = {'Longevity Supplements':NAVY,'Premium Nutrition':TEAL,'Aesthetic Grooming':GOLD,'Lifestyle & Home':GREY}
fig, ax = plt.subplots(figsize=(11,7))
gm_med = sku_rev['gm_pct'].median()
growth_med = sku_rev['growth'].median()
# Zoom axes so the medians sit visually near center
gm_pad = max(0.08, sku_rev['gm_pct'].std()*1.5)
gr_pad = max(0.15, sku_rev['growth'].std()*1.5)
ax.set_xlim((gm_med - gm_pad)*100, (gm_med + gm_pad)*100)
ax.set_ylim((growth_med - gr_pad)*100, (growth_med + gr_pad)*100)
ax.axvline(gm_med*100, color=LGREY, ls='--'); ax.axhline(growth_med*100, color=LGREY, ls='--')
for _, r in sku_rev.iterrows():
    ax.scatter(r['gm_pct']*100, r['growth']*100, s=max(50, r['revenue']/300),
               color=cat_colors.get(r['category'],GREY), alpha=0.75, edgecolor='white', lw=1.2)
ax.set_xlabel('Gross Margin %'); ax.set_ylabel('Revenue Growth % (H2 vs H1)')
ax.set_title('Product portfolio: where to invest (high-growth, high-margin) vs prune', loc='left')
ax.text(0.97, 0.97, 'STARS', transform=ax.transAxes, ha='right', va='top', fontsize=11, fontweight='bold', color=GREEN)
ax.text(0.03, 0.97, 'QUESTION MARKS', transform=ax.transAxes, ha='left', va='top', fontsize=11, fontweight='bold', color=GOLD)
ax.text(0.97, 0.03, 'CASH COWS', transform=ax.transAxes, ha='right', va='bottom', fontsize=11, fontweight='bold', color=NAVY)
ax.text(0.03, 0.03, 'DOGS', transform=ax.transAxes, ha='left', va='bottom', fontsize=11, fontweight='bold', color=RED)
handles = [plt.scatter([],[],color=c,label=k) for k,c in cat_colors.items()]
ax.legend(handles=handles, frameon=False, fontsize=9, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 0.93))
save(fig, '09_sku_bcg_matrix')

# ======================================================================
# PART 4 — OPERATIONS & EXPERIENCE
# ======================================================================
print("PART 4 — Operations & Experience")

# --- 4a. Inventory health ---
inv_status = inventory['stock_status'].value_counts()
metrics['inventory'] = {
    'status_counts': inv_status.to_dict(),
    'cash_in_overstock': round((inventory[inventory['stock_status']=='Overstocked']['units_on_hand']*inventory['unit_cost']).sum()),
    'low_stock_skus': inventory[inventory['stock_status']=='Low Stock']['product_name'].tolist(),
}
fig, ax = plt.subplots(figsize=(9,5))
status_colors = {'Healthy':GREEN,'Low Stock':RED,'Overstocked':GOLD,'Stockout':'#7A1F2B'}
bars = ax.bar(inv_status.index, inv_status.values, color=[status_colors.get(s,GREY) for s in inv_status.index])
for b,v in zip(bars, inv_status.values):
    ax.text(b.get_x()+b.get_width()/2, v, str(v), ha='center', va='bottom', fontweight='bold')
ax.set_ylabel('Number of SKUs')
ax.set_title('Inventory health snapshot: stock imbalances tie up cash and risk lost sales', loc='left', fontsize=11.5)
save(fig, '10_inventory_health')

# --- 4b. Support ticket mix & resolution ---
tt = tickets['ticket_type'].value_counts()
ticket_rate = len(tickets)/len(orders)
metrics['support'] = {
    'ticket_rate_per_order': round(ticket_rate,4),
    'avg_resolution_hours': round(tickets['resolution_hours'].mean(),1),
    'type_mix': tt.to_dict(),
}
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.barh(tt.index[::-1], tt.values[::-1], color=NAVY, alpha=0.85)
ax.set_xlabel('Tickets')
ax.set_title(f'Shipping delays dominate support volume — {ticket_rate*100:.0f}% of orders generate a ticket', loc='left', fontsize=11.5)
save(fig, '11_support_mix')

# --- 4c. Return rate by segment ---
ord_seg = orders.merge(customers[['customer_id','segment']], on='customer_id')
ret = ord_seg.groupby('segment').apply(
    lambda d: (d['order_status']=='Returned').mean(), include_groups=False).reset_index(name='return_rate')
ret = ret.sort_values('return_rate', ascending=True)
metrics['returns'] = ret.round(4).to_dict('records')
fig, ax = plt.subplots(figsize=(10,5))
bars = ax.barh(ret['segment'], ret['return_rate']*100, color=[RED if v>0.09 else TEAL for v in ret['return_rate']])
for b,v in zip(bars, ret['return_rate']):
    ax.text(v*100, b.get_y()+b.get_height()/2, f' {v*100:.1f}%', va='center', fontsize=9, fontweight='bold', color=NAVY)
ax.set_xlabel('Return Rate %')
ax.set_title('Lifestyle Buyers return at nearly double the base rate — a margin leak to fix', loc='left', fontsize=11.5)
save(fig, '12_return_rate')

# ======================================================================
# Save metrics summary
# ======================================================================
with open(f'{OUT}/metrics_summary.json', 'w') as f:
    json.dump(metrics, f, indent=2, default=str)

print("\n=== KEY METRICS ===")
print(f"GMV: ${gmv/1e6:.2f}M | Net Rev: ${net_rev/1e6:.2f}M | AOV: ${aov:.0f}")
print(f"Gross Margin: {gm_pct*100:.1f}% | Contribution Margin: {cm_pct*100:.1f}%")
print(f"Blended CAC: ${blended_cac:.0f} | Customers: {len(customers):,} | Orders: {len(orders):,}")
print(f"\nAll figures saved to {FIG}")
