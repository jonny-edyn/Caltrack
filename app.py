import os
import html
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title='Caltrack', page_icon='🥩', layout='wide')

BASE_ID = os.getenv('AIRTABLE_BASE_ID') or st.secrets.get('AIRTABLE_BASE_ID', 'appD9LwNGFQLeRwOI')
TOKEN = os.getenv('AIRTABLE_TOKEN') or st.secrets.get('AIRTABLE_TOKEN', '')

st.markdown('''
<style>
.stApp{background:radial-gradient(circle at top,#1a2030 0%,#0d0f13 38%,#090b10 100%);color:#f4f6fb}
.stApp::before{content:"";position:fixed;inset:0;background:linear-gradient(180deg,rgba(118,217,134,.08),transparent 24%),radial-gradient(circle at 15% 15%,rgba(92,132,232,.12),transparent 22%);pointer-events:none;z-index:0}
.block-container,.stAppViewContainer{position:relative;z-index:1}
[data-testid="stHeader"]{display:none}
.block-container{max-width:1180px;padding-top:1.8rem;padding-bottom:2.5rem}
h1{font-size:3.1rem!important;line-height:1.02!important;letter-spacing:-.04em!important;margin-bottom:.35rem!important}
h3{font-size:1.25rem!important;letter-spacing:-.02em!important;margin-top:.25rem!important;margin-bottom:.9rem!important}
[data-testid="stCaptionContainer"] p{color:#8f97aa}
[data-testid="stMetric"]{background:linear-gradient(180deg,rgba(29,33,44,.96),rgba(20,23,31,.96));border:1px solid #31384a;padding:16px 16px 14px;border-radius:22px;box-shadow:0 18px 38px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.03)}
[data-testid="stMetricLabel"],[data-testid="stMetricLabel"] p{color:#9098ab!important;text-transform:uppercase;letter-spacing:.06em;font-size:.78rem!important}
[data-testid="stMetricValue"],[data-testid="stMetricValue"] p{color:#f4f6fb!important;font-weight:650}
[data-testid="stMetricDelta"]{background:rgba(118,217,134,.08);border:1px solid rgba(118,217,134,.16);padding:4px 8px;border-radius:999px;display:inline-flex;width:auto}
.hero{background:linear-gradient(145deg,rgba(24,28,38,.98),rgba(20,24,34,.96));border:1px solid #31384a;border-radius:28px;padding:28px 28px 24px;margin-bottom:20px;box-shadow:0 24px 60px rgba(0,0,0,.28)}
.hero-grid{display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap}
.hero-main{flex:1;min-width:300px}
.hero-value{font-size:48px;font-weight:800;letter-spacing:-.05em}
.hero-subvalue{font-size:20px;color:#8f97aa;font-weight:600;letter-spacing:-.02em;margin-left:10px;display:inline-block}
.hero-side{min-width:240px;padding:18px 18px 14px;border-radius:22px;background:linear-gradient(180deg,rgba(255,255,255,.04),rgba(255,255,255,.02));border:1px solid rgba(255,255,255,.06)}
.hero-side .hero-value{font-size:36px}
.meal-card-title{margin-bottom:.2rem}
.meal-photo-frame{background:#171a21;border:1px solid #31384a;border-radius:22px;overflow:hidden;aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 34px rgba(0,0,0,.2)}
.meal-photo-frame img{width:100%;height:100%;object-fit:contain;object-position:center;display:block}
.macro-panel{background:linear-gradient(180deg,rgba(24,28,38,.98),rgba(18,21,29,.96));border:1px solid #31384a;border-radius:28px;padding:22px 18px;margin-top:18px;box-shadow:0 24px 50px rgba(0,0,0,.24)}
.macro-panel-head{display:flex;justify-content:space-between;gap:16px;align-items:flex-end;margin-bottom:8px}
.macro-panel-title{margin:0}
.macro-panel-note{color:#969dad;font-size:12px;text-align:right}
.macro-grid{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:14px;align-items:end}
.macro-day{text-align:center;position:relative}
.macro-value{color:#a8afc2;font-size:11px;margin-bottom:6px}
.macro-track{height:160px;background:linear-gradient(180deg,#262b3d,#222738);border-radius:14px;position:relative;padding:6px;display:flex;align-items:flex-end;box-shadow:inset 0 1px 0 rgba(255,255,255,.03)}
.macro-maintenance{position:absolute;left:6px;right:6px;bottom:6px;border-radius:7px;background:rgba(95,103,134,.18)}
.macro-fill{width:100%;border-radius:7px;min-height:8px}
.macro-line{position:absolute;left:-6px;right:-6px;height:3px;background:#a8afc2;border-radius:999px;opacity:.9}
.macro-label{color:#969dad;font-size:12px;margin-top:8px}
.macro-tooltip{position:absolute;left:50%;bottom:calc(100% + 10px);transform:translateX(-50%);width:190px;padding:10px 12px;border-radius:12px;background:#0f1219;border:1px solid #343a49;color:#f4f6fb;font-size:12px;line-height:1.45;text-align:left;box-shadow:0 10px 24px rgba(0,0,0,.35);opacity:0;pointer-events:none;transition:opacity .15s ease;z-index:20}
.macro-tooltip::after{content:"";position:absolute;left:50%;bottom:-6px;transform:translateX(-50%) rotate(45deg);width:12px;height:12px;background:#0f1219;border-right:1px solid #343a49;border-bottom:1px solid #343a49}
.macro-day:hover .macro-tooltip{opacity:1}
.macro-section-gap{margin-top:22px}
.muted{color:#969dad}
.progress{height:12px;background:#252a36;border-radius:999px;overflow:hidden;margin-top:10px;box-shadow:inset 0 1px 3px rgba(0,0,0,.35)}
.fill{height:100%;background:linear-gradient(90deg,#76d986,#4fcf81);border-radius:999px}
[data-testid="stDataFrame"]{border:1px solid #31384a;border-radius:22px;overflow:hidden;box-shadow:0 18px 34px rgba(0,0,0,.2)}
[data-testid="stDataFrame"] [role="grid"]{background:#151922}
[data-testid="stDataFrame"] [role="columnheader"]{background:#1b2030!important;color:#aeb5c7!important;text-transform:uppercase;letter-spacing:.05em;font-size:.76rem!important}
[data-testid="stDataFrame"] [role="gridcell"]{background:#151922!important;color:#edf1f7!important}
[data-testid="stElementContainer"] .stMarkdown p code{background:rgba(255,255,255,.05);padding:.14rem .36rem;border-radius:6px}
[data-testid="stDivider"]{opacity:.45}
@media (max-width: 900px){
  h1{font-size:2.45rem!important}
  .hero{padding:22px 20px}
  .hero-value{font-size:40px}
  .macro-grid{gap:10px}
  .macro-track{height:132px}
}
</style>
''', unsafe_allow_html=True)


def fetch_table(table):
    if not TOKEN:
        raise RuntimeError('AIRTABLE_TOKEN is not configured')
    url = f'https://api.airtable.com/v0/{BASE_ID}/{requests.utils.quote(table, safe="")}'
    headers = {'Authorization': f'Bearer {TOKEN}'}
    rows, offset = [], None
    while True:
        params = {'pageSize': 100}
        if offset:
            params['offset'] = offset
        r = requests.get(url, headers=headers, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        rows.extend(data.get('records', []))
        offset = data.get('offset')
        if not offset:
            break
    return rows


@st.cache_data(ttl=60)
def load_data():
    return fetch_table('Meals'), fetch_table('Weigh-ins'), fetch_table('Profile')


def to_df(records):
    out = []
    for rec in records:
        row = {'record_id': rec['id']}
        row.update(rec.get('fields', {}))
        out.append(row)
    return pd.DataFrame(out)


def extract_image_url(value):
    if isinstance(value, list):
        for item in value:
            url = extract_image_url(item)
            if url:
                return url
        return None
    if isinstance(value, dict):
        url = value.get('url')
        kind = str(value.get('type') or value.get('mimeType') or '')
        if isinstance(url, str) and (kind.startswith('image/') or url.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif'))):
            return url
        thumbnails = value.get('thumbnails') or {}
        for size in ['full', 'large', 'small']:
            thumb = thumbnails.get(size) or {}
            if isinstance(thumb.get('url'), str):
                return thumb['url']
        return None
    if isinstance(value, str) and value.lower().startswith(('http://', 'https://')) and value.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
        return value
    return None


def meal_image_url(row):
    for key, value in row.items():
        if key in {'record_id', 'Logged At', 'Logged Local', 'Date'}:
            continue
        url = extract_image_url(value)
        if url:
            return url
    return None


def format_meal_value(value, suffix=''):
    if pd.isna(value):
        return None
    if isinstance(value, float):
        if value.is_integer():
            value = int(value)
        else:
            value = round(value, 1)
    return f'{value}{suffix}'


def build_day_meal_tooltip(day_rows, metric='calories'):
    if day_rows.empty:
        return ['No meals logged']
    items = []
    for _, meal in day_rows.sort_values('Logged Local' if 'Logged Local' in day_rows.columns else 'record_id').iterrows():
        meal_name = meal.get('Meal') or meal.get('Meal Type') or 'Meal'
        if metric == 'protein':
            protein_source = None
            for field_name in ['Protein Source', 'Main Protein', 'Protein Breakdown']:
                value = meal.get(field_name)
                if value is not None and not pd.isna(value) and str(value).strip():
                    protein_source = str(value).strip()
                    break
            if protein_source:
                items.append(protein_source)
            else:
                items.append('Protein source not set')
        else:
            calories = meal.get('Calories Estimate')
            if calories is not None and not pd.isna(calories):
                cal_text = f'{int(round(float(calories))):,} kcal'
                items.append(f'{meal_name}: {cal_text}')
            else:
                items.append(str(meal_name))
    return items


def resolve_maintenance_calories(profile_data, target_calories):
    explicit = profile_data.get('Maintenance Calories')
    if explicit is not None and not pd.isna(explicit):
        return int(float(explicit))
    fallback_gap = max(250, min(600, int(target_calories * 0.2)))
    return int(target_calories + fallback_gap)


def build_macro_section(title, day_data, target, note, maintenance=None):
    scale_points = [target] + [float(day['value']) for day in day_data] + [1]
    if maintenance is not None:
        scale_points.append(float(maintenance))
    max_value = max(scale_points)
    scale_max = max_value * 1.15
    line_pct = min(92.0, max(8.0, target / scale_max * 100))
    maintenance_pct = None if maintenance is None else min(92.0, max(8.0, maintenance / scale_max * 100))
    bars = []
    for day in day_data:
        value = float(day['value'])
        fill_pct = min(100.0, max(0.0, value / scale_max * 100))
        maintenance_html = f'<div class="macro-maintenance" style="height:{maintenance_pct:.1f}%"></div>' if maintenance_pct is not None else ''
        tooltip_lines = day.get('tooltip') or ['No meals logged']
        tooltip_html = '<br>'.join(html.escape(line) for line in tooltip_lines)
        bars.append(
            f'<div class="macro-day">'
            f'<div class="macro-tooltip">{tooltip_html}</div>'
            f'<div class="macro-value">{int(round(value)):,}</div>'
            f'<div class="macro-track">'
            f'{maintenance_html}'
            f'<div class="macro-line" style="bottom:{line_pct:.1f}%"></div>'
            f'<div class="macro-fill" style="height:{fill_pct:.1f}%;background:{day["color"]}"></div>'
            f'</div>'
            f'<div class="macro-label">{day["label"]}</div>'
            f'</div>'
        )
    section_class = 'macro-section-gap' if title == 'PROTEIN' else ''
    return (
        f'<div class="{section_class}">'
        f'<div class="macro-panel-head">'
        f'<div class="muted macro-panel-title">{title}</div>'
        f'<div class="macro-panel-note">{note}</div>'
        f'</div>'
        f'<div class="macro-grid">{"".join(bars)}</div>'
        f'</div>'
    )


st.title('🥩 Caltrack')
st.caption('Journey to 80kg eating 2050 kcal per day and 160g protein')

if not TOKEN:
    st.error('Add AIRTABLE_TOKEN in Streamlit secrets before running this app.')
    st.stop()

try:
    meals_raw, weighins_raw, profile_raw = load_data()
except Exception as e:
    st.error(f'Could not load Airtable data: {e}')
    st.stop()

meals, weighins, profiles = map(to_df, [meals_raw, weighins_raw, profile_raw])
profile = profiles.iloc[0].to_dict() if not profiles.empty else {}
daily_target = int(profile.get('Daily Calorie Target', 2050) or 2050)
protein_target = int(profile.get('Daily Protein Target g', 160) or 160)
maintenance_calories = resolve_maintenance_calories(profile, daily_target)
start_weight = float(profile.get('Starting Weight kg', 96) or 96)
goal_weight = float(profile.get('Goal Weight kg', 80) or 80)

today = pd.Timestamp.now(tz='Europe/London').date()
if not meals.empty and 'Logged At' in meals:
    meals['Logged At'] = pd.to_datetime(meals['Logged At'], errors='coerce', utc=True)
    meals['Logged Local'] = meals['Logged At'].dt.tz_convert('Europe/London')
    meals['Date'] = meals['Logged Local'].dt.date
    today_meals = meals[meals['Date'] == today].copy()
else:
    today_meals = pd.DataFrame()

today_calories = int(today_meals.get('Calories Estimate', pd.Series(dtype=float)).fillna(0).sum()) if not today_meals.empty else 0
today_protein = float(today_meals.get('Protein g', pd.Series(dtype=float)).fillna(0).sum()) if not today_meals.empty else 0
cal_remaining = max(0, daily_target - today_calories)
protein_remaining = max(0, protein_target - today_protein)
macro_html = None

latest_weight = start_weight
if not weighins.empty and {'Date', 'Weight kg'}.issubset(weighins.columns):
    weighins['Date'] = pd.to_datetime(weighins['Date'], errors='coerce')
    weighins = weighins.sort_values('Date')
    valid = weighins.dropna(subset=['Weight kg'])
    if not valid.empty:
        latest_weight = float(valid.iloc[-1]['Weight kg'])

lost = max(0, start_weight - latest_weight)
remaining = max(0, latest_weight - goal_weight)
progress = 0 if start_weight <= goal_weight else min(100, max(0, lost / (start_weight - goal_weight) * 100))
cal_pct = min(100, today_calories / max(1, daily_target) * 100)

st.markdown(f'''
<div class="hero">
  <div class="hero-grid">
    <div class="hero-main">
      <div class="muted">TODAY</div>
      <div class="hero-value">{today_calories:,} <span class="hero-subvalue">/ {daily_target:,} kcal</span></div>
      <div class="progress"><div class="fill" style="width:{cal_pct:.1f}%"></div></div>
      <div class="muted" style="margin-top:9px">{cal_remaining:,} kcal remaining</div>
    </div>
    <div class="hero-side">
      <div class="muted">WEIGHT PROGRESS</div>
      <div class="hero-value">{latest_weight:.1f} kg</div>
      <div class="muted">{remaining:.1f} kg to goal</div>
      <div class="progress"><div class="fill" style="width:{progress:.1f}%"></div></div>
      <div class="muted" style="margin-top:9px">{progress:.0f}% complete</div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric('Calories today', f'{today_calories:,}', f'{cal_remaining:,} remaining')
c2.metric('Protein today', f'{today_protein:.0f} g', f'{protein_remaining:.0f} g remaining')
c3.metric('Current weight', f'{latest_weight:.1f} kg', f'{lost:.1f} kg lost')
c4.metric('Goal weight', f'{goal_weight:.1f} kg', f'{remaining:.1f} kg remaining')

st.divider()
left, right = st.columns([1.6, 1])
with left:
    st.subheader('Weight trend')
    if not weighins.empty and {'Date', 'Weight kg'}.issubset(weighins.columns):
        chart = weighins.dropna(subset=['Date', 'Weight kg'])[['Date', 'Weight kg']].set_index('Date')
        if not chart.empty:
            st.line_chart(chart, use_container_width=True)
        else:
            st.info('Add more weigh-ins to see your trend.')
    else:
        st.info('No weigh-ins yet.')
    if not meals.empty and 'Date' in meals.columns:
        recent_days = pd.date_range(end=pd.Timestamp(today), periods=7, freq='D')
        agg_map = {}
        if 'Calories Estimate' in meals.columns:
            agg_map['Calories Estimate'] = 'sum'
        if 'Protein g' in meals.columns:
            agg_map['Protein g'] = 'sum'
        if agg_map:
            macro_daily = meals.groupby('Date', dropna=True).agg(agg_map).reindex(recent_days.date, fill_value=0)
            calorie_days = []
            protein_days = []
            for dt in recent_days:
                label = dt.strftime('%a %-d') if os.name != 'nt' else dt.strftime('%a %d').replace(' 0', ' ')
                cal_value = float(macro_daily.loc[dt.date(), 'Calories Estimate']) if 'Calories Estimate' in macro_daily.columns else 0
                protein_value = float(macro_daily.loc[dt.date(), 'Protein g']) if 'Protein g' in macro_daily.columns else 0
                day_meals = meals[meals['Date'] == dt.date()].copy()
                calorie_tooltip = build_day_meal_tooltip(day_meals, metric='calories')
                protein_tooltip = build_day_meal_tooltip(day_meals, metric='protein')
                calorie_days.append({
                    'label': label,
                    'value': cal_value,
                    'color': '#76d986' if cal_value <= daily_target else '#e47572',
                    'tooltip': calorie_tooltip,
                })
                protein_days.append({
                    'label': label,
                    'value': protein_value,
                    'color': '#76d986' if protein_value >= protein_target else '#5a84e8',
                    'tooltip': protein_tooltip,
                })
            macro_html = (
                '<div class="macro-panel">'
                + build_macro_section('CALORIES', calorie_days, daily_target, 'bar = eaten • shaded = maintenance • line = target', maintenance=maintenance_calories)
                + build_macro_section('PROTEIN', protein_days, protein_target, 'line = goal')
                + '</div>'
            )
with right:
    st.subheader('Last 7 days')
    if not meals.empty and 'Date' in meals.columns:
        cutoff = today - pd.Timedelta(days=6)
        last7 = meals[meals['Date'] >= cutoff]
        if not last7.empty:
            by_day = last7.groupby('Date', dropna=True)
            st.metric('Average daily calories', f"{by_day['Calories Estimate'].sum().mean():,.0f}")
            st.metric('Average daily protein', f"{by_day['Protein g'].sum().mean():.0f} g")
            st.metric('Meals logged', f'{len(last7)}')
        else:
            st.info('No meals logged in the past 7 days.')

if macro_html:
    st.markdown(macro_html, unsafe_allow_html=True)

st.divider()
st.subheader('Recent meals')
if meals.empty:
    st.info('No meals logged yet. Upload a food photo in ChatGPT and ask to save it.')
else:
    cols = [c for c in ['Logged Local', 'Meal', 'Meal Type', 'Calories Estimate', 'Calories Low', 'Calories High', 'Protein g', 'Carbohydrates g', 'Fat g', 'Confidence', 'Notes'] if c in meals.columns]
    recent_source = meals.sort_values('Logged Local', ascending=False).head(20).copy()
    recent = recent_source[cols].copy()
    recent['Photo'] = recent_source.apply(meal_image_url, axis=1)
    if 'Logged Local' in recent.columns:
        recent['Logged Local'] = recent['Logged Local'].dt.strftime('%d/%m/%Y %H:%M')
    if recent['Photo'].notna().any():
        for _, row in recent.iterrows():
            image_col, details_col = st.columns([1.05, 1.25], gap='medium')
            with image_col:
                if pd.notna(row['Photo']):
                    safe_url = html.escape(str(row['Photo']), quote=True)
                    safe_alt = html.escape(str(row.get('Meal') or 'Meal photo'))
                    st.markdown(
                        f'<div class="meal-photo-frame"><img src="{safe_url}" alt="{safe_alt}"></div>',
                        unsafe_allow_html=True,
                    )
            with details_col:
                title = row.get('Meal') or row.get('Meal Type') or 'Meal'
                st.markdown(f'<h4 class="meal-card-title">{title}</h4>', unsafe_allow_html=True)
                meta = []
                if row.get('Logged Local'):
                    meta.append(str(row['Logged Local']))
                if row.get('Meal Type'):
                    meta.append(str(row.get('Meal Type')))
                if meta:
                    st.caption(' | '.join(meta))

                summary = []
                for label, value in [
                    ('Calories', format_meal_value(row.get('Calories Estimate'), ' kcal')),
                    ('Protein', format_meal_value(row.get('Protein g'), ' g')),
                    ('Carbs', format_meal_value(row.get('Carbohydrates g'), ' g')),
                    ('Fat', format_meal_value(row.get('Fat g'), ' g')),
                    ('Confidence', format_meal_value(row.get('Confidence'))),
                ]:
                    if value:
                        summary.append(f'**{label}:** {value}')
                if summary:
                    st.markdown(' | '.join(summary))

                range_text = (
                    f"{format_meal_value(row.get('Calories Low'))} - {format_meal_value(row.get('Calories High'))} kcal"
                    if row.get('Calories Low') is not None and pd.notna(row.get('Calories Low'))
                    and row.get('Calories High') is not None and pd.notna(row.get('Calories High'))
                    else None
                )
                if range_text:
                    st.caption(f'Range: {range_text}')
                if row.get('Notes'):
                    st.caption(str(row.get('Notes')))
            st.divider()
    st.subheader('Meal history')
    st.dataframe(recent[cols], use_container_width=True, hide_index=True)

st.caption('Reads live data from Airtable and refreshes approximately once per minute.')
