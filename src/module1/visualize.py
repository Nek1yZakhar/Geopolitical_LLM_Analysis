import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import numpy as np
import os

# ─── Загрузка данных ─────────────────────────────────────────────────────────
df = pd.read_csv('data/module1/timeline.csv')
df['date_parsed'] = pd.to_datetime(df['date'], format='%Y-%m')
sanctions = df[df['event_type'] == 'sanction'].sort_values('date_parsed').reset_index(drop=True)
releases = df[df['event_type'] == 'model_release'].sort_values('date_parsed').reset_index(drop=True)

## ═══ ГРАФИК 1: output/module1_sanctions_timeline.png ═══════════════
## Горизонтальный таймлайн — каждая санкция = строка таблицы

level_colors = {1: '#f4a582', 2: '#d6604d', 3: '#8b0000'}
type_colors  = {'legislation': '#4A90D9', 'policy_reversal': '#E8A838'}

fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
ax.set_facecolor('white')

# Горизонтальная ось — время
ax.set_xlim(pd.Timestamp('2018-06-01'), pd.Timestamp('2025-10-01'))
ax.set_ylim(-0.5, len(sanctions) - 0.5)

# Горизонтальные направляющие
for i in range(len(sanctions)):
    ax.axhline(y=i, color='#e0e0e0', linewidth=0.5, zorder=0)

# Маппинг событий на библиографические индексы
bib_indices = {
    'Huawei Entity List': '[1]',
    'SMIC Entity List': '[2]',
    'CHIPS and Science Act': '[8]',
    'Advanced Computing Rule — A100/H100 Ban': '[9]',
    'Executive Order — Outbound Investment': '[5]',
    'Advanced Computing Rule — A800/H800 Ban': '[10]',
    'Third-Country Circumvention Controls': '[3]',
    'AI Diffusion Rule': '[7]',
    'Nvidia H20 Export Ban': '[50]',
    'Trump EO — Biden Diffusion Rule Revocation': '[11]',
    'YMTC Entity List': '[4]',
    'Biren and Moore Threads Entity List': '[6]'
}

for i, row in sanctions.iterrows():
    subtype = row['event_subtype']
    if subtype in type_colors:
        color = type_colors[subtype]
    else:
        level = int(row['chip_restriction_level'] or 2)
        color = level_colors.get(level, '#999999')
    
    ax.scatter(row['date_parsed'], i, 
               s=140, color=color, zorder=5, edgecolors='white', linewidth=1.5)
    
    # Регулярное название + индекс
    display_name = row['event_name']
    bib_idx = bib_indices.get(display_name, '')
    full_label = f"{display_name} {bib_idx}".strip()
    
    ax.text(row['date_parsed'] - pd.Timedelta(days=50), i,
            full_label,
            fontsize=11.5, color='#222222', ha='right', va='center', fontweight='normal')
    
    ax.text(row['date_parsed'] + pd.Timedelta(days=50), i,
            row['date_parsed'].strftime('%Y-%m'),
            fontsize=10.5, color='#666666', ha='left', va='center')

# Ось X снизу — только годы
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.tick_params(axis='x', labelsize=11.5)
ax.yaxis.set_visible(False)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')

# Легенда
level_patches = [mpatches.Patch(color=level_colors[k], label=f'Уровень {k}') for k in [1, 2, 3]]
type_labels = {'legislation': 'Законодательство [8]', 'policy_reversal': 'Отмена ограничений [11]'}
type_patches  = [mpatches.Patch(color=type_colors[k], label=type_labels.get(k, k.capitalize())) for k in type_colors]
ax.legend(handles=level_patches + type_patches, loc='lower right', fontsize=11, framealpha=0.95, edgecolor='#cccccc')

fig.text(0.5, 0.05, 'Рисунок 1 — Санкционные раунды США в сфере ИИ и полупроводников (2019–2025)',
         ha='center', fontsize=16, fontweight='bold')
plt.figtext(0.5, 0.02, 'Источник: составлено автором по [1–11, 50].', 
            ha='center', fontsize=12, style='italic')

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('output/module1_sanctions_timeline.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ График 1 сохранён")


## ═══ ГРАФИК 2: output/module1_releases_bar.png ═══════════════════════
## Горизонтальный барчарт: релизы и санкции

color_map = {
    'DeepSeek AI':              '#1f77b4',
    'Alibaba Cloud':            '#ff7f0e',
    'Tsinghua / Zhipu AI':      '#2ca02c',
    'Shanghai AI Laboratory':   '#9467bd',
    '01.AI':                    '#8c564b',
    'Baichuan AI':              '#e377c2',
    'Moonshot AI':              '#17becf',
    'IDEA Research':            '#bcbd22',
}

abbreviations = {
    'Advanced Computing Rule — A100/H100 Ban': 'ACR-22',
    'Advanced Computing Rule — A800/H800 Ban': 'ACR-23',
    'Third-Country Circumvention Controls': 'TCC',
    'AI Diffusion Rule': 'ADR',
    'Nvidia H20 Export Ban': 'H20',
    'Trump EO — Biden Diffusion Rule Revocation': 'Trump EO',
    'YMTC Entity List': 'YMTC EL',
    'Biren and Moore Threads Entity List': 'Biren EL'
}

fig, ax = plt.subplots(figsize=(14, 18), facecolor='white')
ax.set_facecolor('white')
plt.subplots_adjust(top=0.93, bottom=0.07, left=0.12, right=0.88)
ax.set_xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2025-09-01'))
ax.set_ylim(-8, len(releases) - 0.5) # Увеличили область снизу для надписей санкций

# Направляющие
for i in range(len(releases)):
    ax.axhline(y=i, color='#f0f0f0', linewidth=0.5, zorder=0)

sanctions_2023 = sanctions[sanctions['date_parsed'] >= pd.Timestamp('2023-01-01')].copy()
# Координаты для ступенчатого расположения надписей в «подвале» под графиком
y_levels = [-2, -4, -6]
last_date = None
collision_count = 0
for idx, (_, row) in enumerate(sanctions_2023.iterrows()):
    subtype = row['event_subtype']
    color = type_colors.get(subtype, level_colors.get(int(row['chip_restriction_level'] or 2), '#999999'))
    ax.axvline(x=row['date_parsed'], color=color, linewidth=1.0, linestyle='--', alpha=0.5, zorder=1)
    
    if row['date_parsed'] == last_date: collision_count += 1
    else: collision_count = 0; last_date = row['date_parsed']
    
    x_offset = 5 + (collision_count * 12) # Уменьшил шаг по X, так как теперь есть разнос по Y
    y_pos = y_levels[idx % len(y_levels)] 
    
    label_text = abbreviations.get(row['event_name'], row['event_name'][:15])
    ax.text(row['date_parsed'] - pd.Timedelta(days=x_offset), y_pos, label_text, 
            fontsize=10.5, rotation=90, va='center', ha='right', color=color, alpha=0.95, fontweight='bold')

# Точки моделей
releases['y_pos'] = range(len(releases))
releases['y_pos'] = releases['y_pos'].astype(float)
cluster_2023_06 = releases[releases['date_parsed'] == '2023-06-01']
if not cluster_2023_06.empty:
    offsets = [-0.15, 0.0, 0.15]
    for idx, (orig_idx, _) in enumerate(cluster_2023_06.iterrows()):
        releases.loc[orig_idx, 'y_pos'] += offsets[idx % len(offsets)]

model_bib_indices = {
    'DeepSeek-LLM': '[60]', 'DeepSeek-V1': '[60]', 'DeepSeek-V1 (67B)': '[60]', 
    'DeepSeek-V2': '[62]', 'DeepSeek-V2 (236B MoE)': '[62]',
    'DeepSeek-V2.5': '[63]', 'DeepSeek-V3': '[64]', 'DeepSeek-V3 (671B MoE)': '[64]',
    'DeepSeek-Coder-V2': '[59]', 'DeepSeek-Coder-V2 (16B/236B)': '[59]',
    'DeepSeek-R1': '[61]', 'DeepSeek-R1 (671B MoE)': '[61]', 'DeepSeek-R1-Zero': '[61]',
    'Qwen-1': '[69]', 'Qwen-1 (7B/14B)': '[69]', 'Qwen-7B': '[69]', 'Qwen1.5': '[69]', 'Qwen1.5 (72B)': '[69]',
    'Qwen2': '[69]', 'Qwen2 (72B)': '[69]', 'Qwen2.5': '[69]', 'Qwen2.5 (72B)': '[69]',
    'Qwen2.5-Coder-32B': '[69]', 'Qwen2.5-Max': '[69]', 'Qwen-Max': '[69]', 
    'Qwen-Max (proprietary baseline)': '[69]', 'QwQ-32B': '[69]',
    'Qwen3': '[70]', 'Qwen3-235B': '[70]', 'Qwen3-Coder': '[71]',
    'Kimi-k1.5': '[66]', 'Kimi k1.5': '[66]', 'Kimi K2': '[26]', 'Kimi K2 (1T MoE)': '[26]', 'Kimi-K2': '[26]', 'Kimi-VL': '[66]',
    'Yi': '[55]', 'Yi-34B': '[55]', 'Yi-1.5': '[56]', 'Yi-1.5 (34B)': '[56]',
    'Baichuan-1': '[57]', 'Baichuan-1 (7B/13B)': '[57]', 'Baichuan-13B': '[57]', 
    'Baichuan-2': '[58]', 'Baichuan-2 (7B/13B)': '[58]', 'Baichuan2': '[58]',
    'ChatGLM2-6B': '[72]', 'ChatGLM3': '[73]', 'ChatGLM3-6B': '[73]', 
    'CodeGeeX2': '[74]', 'CodeGeeX2-6B': '[74]', 'GLM-4': '[75]', 'GLM-4 (9B)': '[75]',
    'InternLM-20B': '[65]', 'InternLM-7B': '[65]', 'InternLM1': '[65]', 'InternLM2': '[65]', 'InternLM2.5': '[65]',
    'InternLM': '[65]', 'InternLM-1': '[65]', 'InternLM-1 (7B/20B)': '[65]', 
    'InternLM-2': '[65]', 'InternLM-2 (20B)': '[65]', 'InternLM-2.5': '[65]', 'InternLM-2.5 (7B/20B)': '[65]',
    'InternVL': '[68]', 'InternVL2-Llama3': '[68]', 'InternVL2-Llama3 (76B)': '[68]',
    'YAYI': '[76]', 'YAYI-1': '[76]', 'YAYI-1 (7B)': '[76]', 'YAYI2': '[77]', 'YAYI-2': '[77]', 'YAYI-2 (30B)': '[77]',
    'Aquila-7B': '[52]'
}

for _, row in releases.iterrows():
    actor = row['actor']
    color = color_map.get(actor, '#999999')
    mkr_y = row['y_pos']
    if bool(row['open_weight']):
        ax.scatter(row['date_parsed'], mkr_y, s=140, color=color, zorder=5, edgecolors='white', linewidth=1.2)
    else:
        ax.scatter(row['date_parsed'], mkr_y, s=140, facecolors='none', zorder=5, edgecolors=color, linewidth=1.5)
    
    m_name = row['event_name']
    bib = model_bib_indices.get(m_name, model_bib_indices.get(m_name.split('(')[0].strip(), '[Источник не указан]'))
    ax.text(row['date_parsed'] + pd.Timedelta(days=15), mkr_y, f"{m_name} {bib}".strip(), 
            fontsize=12, color='#222222', ha='left', va='center')
    ax.text(row['date_parsed'] - pd.Timedelta(days=15), mkr_y, row['date_parsed'].strftime('%Y-%m'), 
            fontsize=10.5, color='#888888', ha='right', va='center')

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.tick_params(axis='x', rotation=45, labelsize=11)
ax.yaxis.set_visible(False)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')

legend_elements = [mpatches.Patch(color=v, label=k) for k, v in color_map.items() if k in releases['actor'].values]
legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Open-source', markerfacecolor='gray', markersize=8, linestyle='None'))
legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Proprietary', markerfacecolor='none', markersize=8, linestyle='None'))
ax.legend(handles=legend_elements, title='Организация и тип', loc='upper left', fontsize=11, title_fontsize=13)

fig.text(0.5, 0.05, 'Рисунок 2 — Релизы китайских моделей ИИ на фоне санкционных раундов (2023–2025)',
         ha='center', fontsize=16, fontweight='bold')
plt.figtext(0.5, 0.02, 'Источник: составлено автором по [34, 37, 49, 53–77].', 
            ha='center', fontsize=12, style='italic')

plt.tight_layout(rect=[0, 0.08, 1, 1])
plt.savefig('output/module1_releases_bar.png', dpi=180, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ График 2 сохранён")


## ═══ ГРАФИК 3: output/module1_lags_by_wave.png ═══════════════════════
## Медианный инновационный лаг по санкционным волнам (2022–2025)

lags_csv = 'data/module1/lags.csv'
if os.path.exists(lags_csv):
    lag_df_raw = pd.read_csv(lags_csv)
    
    def map_wave(sanction):
        s_low = str(sanction).lower()
        if 'ymtc' in s_low: return 'YMTC EL\n(Dec 2022)'
        elif 'biren' in s_low or 'moore' in s_low: return 'Biren/Moore EL\n(Oct 2023)'
        elif 'third-country' in s_low or 'diffusion' in s_low: return 'Third-Country\n(Jan 2025)'
        elif 'h20' in s_low: return 'H20 Ban\n(Apr 2025)'
        return None

    lag_df_raw['wave'] = lag_df_raw['preceding_sanction'].apply(map_wave)
    lag_df_raw = lag_df_raw.dropna(subset=['wave'])

    wave_order = [
        'YMTC EL\n(Dec 2022)',
        'Biren/Moore EL\n(Oct 2023)',
        'Third-Country\n(Jan 2025)',
        'H20 Ban\n(Apr 2025)'
    ]
    
    median_lags = lag_df_raw.groupby('wave')['lag_months'].median().reindex(wave_order).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 7), facecolor='white')
    colors = ['#ADD8E6', '#6495ED', '#DC143C', '#8B0000']
    
    bars = ax.bar(median_lags['wave'], median_lags['lag_months'], color=colors, edgecolor='black', linewidth=0.8)
    
    # Линия тренда
    x_num = np.arange(len(median_lags))
    y_vals = median_lags['lag_months'].values.astype(float)
    z = np.polyfit(x_num, y_vals, 1)
    p = np.poly1d(z)
    ax.plot(median_lags['wave'], p(x_num), color='gray', linestyle='--', linewidth=1.5, label='Тренд')

    ax.set_ylabel('Лаг (мес.)', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.1, f'{height:.1f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    fig.text(0.5, 0.05, 'Рисунок 3 — Медианный инновационный лаг по санкционным волнам (2022–2025)',
             ha='center', fontsize=16, fontweight='bold')
    plt.figtext(0.5, 0.02, f'Источник: рассчитано автором на базе данных [3, 4, 6, 7, 9, 10, 50, 53–77].', 
                ha='center', fontsize=12, style='italic')

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.savefig('output/module1_lags_by_wave.png', dpi=180, bbox_inches='tight', facecolor='white')
    plt.close()
    print("✅ График 3 сохранён (Волны)")
else:
    print("⚠️ Файл data/module1/lags.csv не найден")
