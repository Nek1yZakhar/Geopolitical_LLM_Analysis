import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# Create output directory if it doesn't exist
os.makedirs('output', exist_ok=True)

# 1. Load Data
df = pd.read_csv('data/module3/module3_classified.csv')

# 2. Preprocessing
# Model name mapping
model_map = {
    'deepseek-v3': 'DS-V3',
    'qwen3': 'Qwen3',
    'kimi-k2': 'Kimi-K2',
    'gpt-5.4m': 'GPT-5.4m',
    'gemini-3.1fl': 'Gem-3.1f'
}
df['model_short'] = df['model_short'].replace(model_map)

# Prompt ID sorting
prompt_order = [f"{b}{i}" for b in ['A', 'B', 'C'] for i in range(1, 5)]
df['prompt_id'] = pd.Categorical(df['prompt_id'], categories=prompt_order, ordered=True)

# Fill NaNs
df['tone'] = df['tone'].fillna('NaN')
df['sanction_frame'] = df['sanction_frame'].fillna('no_frame')
df['refusal_type'] = df['refusal_type'].fillna('NaN')

# 3. Generate Stats CSV
stats_list = []
for (model, block), group in df.groupby(['model_short', 'prompt_block']):
    total = len(group)
    tone_counts = group['tone'].value_counts().to_dict()
    sf_counts = group['sanction_frame'].value_counts().to_dict()
    rt_counts = group['refusal_type'].value_counts().to_dict()
    
    entry = {
        'model': model,
        'block': block,
        'n_total': total
    }
    for t in ['pro_CN', 'neutral', 'pro_US', 'NaN']:
        count = tone_counts.get(t, 0)
        entry[f'tone_{t}_count'] = count
        entry[f'tone_{t}_pct'] = round(count / total * 100, 2)
    for sf in ['threat', 'stimulus', 'necessity', 'no_frame']:
        count = sf_counts.get(sf, 0)
        entry[f'sf_{sf}_count'] = count
        entry[f'sf_{sf}_pct'] = round(count / total * 100, 2)
    for rt in ['hard_refusal', 'soft_refusal', 'no_refusal', 'NaN']:
        count = rt_counts.get(rt, 0)
        entry[f'rt_{rt}_count'] = count
        entry[f'rt_{rt}_pct'] = round(count / total * 100, 2)
        
    stats_list.append(entry)

stats_df = pd.DataFrame(stats_list)
stats_df.to_csv('data/module3/stats.csv', index=False)
print("Stats saved to data/module3/stats.csv")

# 4. Visualization Setup
colors = {
    'pro_CN': "#c0392b",
    'neutral': "#95a5a6",
    'pro_US': "#2980b9",
    'NaN_tone': "#dcdde1",        # Darker light grey
    'rt_NaN_refusal': "#7f8c8d",   # Dark grey for better visibility
    'hard_refusal': "#e74c3c",
    'soft_refusal': "#e67e22",
    'no_refusal': "#27ae60",
    'NaN_refusal': "#bdc3c7",
    'threat': "#8e44ad",
    'stimulus': "#27ae60",
    'necessity': "#2980b9",
    'no_frame': "#95a5a6"
}

model_order = ['DS-V3', 'Qwen3', 'Kimi-K2', 'GPT-5.4m', 'Gem-3.1f']

fig = make_subplots(
    rows=1, cols=3,
    column_widths=[0.5, 0.25, 0.25],
    subplot_titles=("Тональность по моделям и промптам", "Санкционный фрейминг (B4+C4)", "Типы ответов и отказов"),
    horizontal_spacing=0.08
)

# --- PANEL 1: HEATMAP ---
tone_map_idx = {'pro_CN': -1, 'neutral': 0, 'pro_US': 1, 'NaN': -2}
heatmap_data = []

# Map tone to numerical for heatmap
df['tone_num'] = df['tone'].map(tone_map_idx).fillna(-2)

for model in model_order:
    model_row = []
    for prompt in prompt_order:
        subset = df[(df['model_short'] == model) & (df['prompt_id'] == prompt)]
        if not subset.empty:
            val = subset['tone_num'].iloc[0]
        else:
            val = -2 # NaN
        model_row.append(val)
    heatmap_data.append(model_row)

fig.add_trace(
    go.Heatmap(
        z=heatmap_data,
        x=prompt_order,
        y=model_order,
        zmin=-2,
        zmax=1,
        colorscale=[
            [0.0, colors['NaN_tone']], [0.25, colors['NaN_tone']],
            [0.25, colors['pro_CN']], [0.5, colors['pro_CN']],
            [0.5, colors['neutral']], [0.75, colors['neutral']],
            [0.75, colors['pro_US']], [1.0, colors['pro_US']]
        ],
        showscale=False,
        name="Тональность"
    ),
    row=1, col=1
)

# Dummy traces for Heatmap legend (Panel 1)
tone_legend_map = {
    'pro_CN': 'Про-КНР',
    'neutral': 'Нейтрально',
    'pro_US': 'Про-США',
    'NaN_tone': 'Нет данных'
}
for tone_key, tone_label in tone_legend_map.items():
    fig.add_trace(
        go.Bar(
            name=tone_label,
            x=[None], y=[None],
            marker=dict(color=colors[tone_key]),
            legend="legend1",
            showlegend=True
        ),
        row=1, col=1
    )

# Add vertical lines between A/B and B/C
fig.add_vline(x=3.5, line_width=2, line_dash="dash", line_color="white", row=1, col=1)
fig.add_vline(x=7.5, line_width=2, line_dash="dash", line_color="white", row=1, col=1)

# --- PANEL 2: GROUPED BAR (B4+C4) ---
df_b4c4 = df[df['prompt_id'].isin(['B4', 'C4'])]
sf_map = {
    'threat': 'Угроза',
    'stimulus': 'Стимул',
    'necessity': 'Необходимость',
    'no_frame': 'Без фрейма'
}

for sf_key, sf_label in sf_map.items():
    sf_counts = []
    for model in model_order:
        count = len(df_b4c4[(df_b4c4['model_short'] == model) & (df_b4c4['sanction_frame'] == sf_key)])
        sf_counts.append(count)
    
    # Convert to percentages
    total_responses = 4 # 2 prompts * 2 runs
    pcts = [(c / total_responses) * 100 for c in sf_counts]
    
    fig.add_trace(
        go.Bar(
            name=sf_label,
            x=model_order,
            y=pcts,
            marker_color=colors[sf_key],
            legend="legend2",
            showlegend=True,
            offsetgroup=sf_key
        ),
        row=1, col=2
    )

# --- PANEL 3: STACKED BAR 100% (MANUAL STACKING) ---
rt_map = {
    'NaN': 'Нет данных',
    'hard_refusal': 'Жесткий отказ',
    'soft_refusal': 'Мягкий отказ',
    'no_refusal': 'Без отказа'
}
rt_cumulative = {model: 0 for model in model_order}

for rt_key, rt_label in rt_map.items():
    current_pcts = []
    bases = []
    for model in model_order:
        model_group = df[df['model_short'] == model]
        if len(model_group) > 0:
            count = len(model_group[model_group['refusal_type'] == rt_key])
            pct = count / len(model_group) * 100
        else:
            pct = 0
        current_pcts.append(pct)
        bases.append(rt_cumulative[model])
        rt_cumulative[model] += pct
    
    fig.add_trace(
        go.Bar(
            name=rt_label,
            x=model_order,
            y=current_pcts,
            base=bases,
            marker_color=colors[rt_key if rt_key != 'NaN' else 'NaN_refusal'],
            legend="legend3",
            showlegend=True,
            offsetgroup="rt_stack"
        ),
        row=1, col=3
    )

# 5. Global Layout Styling with Multiple Legends
fig.update_layout(
    title_text="Рис. 3. Классификация нарративов в ответах LLM на геополитические промпты (n=120)",
    title_x=0.5,
    title_font_size=16,
    template="plotly_white",
    width=1800,
    height=650, # Slightly increased to accommodate legends
    
    # Legend for Panel 1 (Tone)
    legend1=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.22,
        font=dict(size=10)
    ),
    # Legend for Panel 2 (Sanction Frame)
    legend2=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.61,
        font=dict(size=10)
    ),
    # Legend for Panel 3 (Refusal Type)
    legend3=dict(
        orientation="h",
        yanchor="top",
        y=-0.15,
        xanchor="center",
        x=0.90,
        font=dict(size=10)
    ),
    
    font=dict(size=11),
    margin=dict(t=80, b=150, l=60, r=40),
)

fig.update_xaxes(tickfont=dict(size=11), title_standoff=10)
fig.update_yaxes(tickfont=dict(size=11), gridcolor='lightgrey')
fig.update_yaxes(range=[0, 100], row=1, col=3) # Force 100% scale for panel 3

# Save
fig.write_image("output/fig3_combined.png", scale=2)
print("Figure saved to output/fig3_combined.png")
