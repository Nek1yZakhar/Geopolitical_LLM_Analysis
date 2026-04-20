"""
TICKET-05 (v3) — Совмещённый таймлайн санкций и релизов китайских open-source моделей ИИ.
Два горизонтальных ряда (swim lanes) для разгрузки зоны 2023-2025.
Сохраняет output/module1_timeline.png
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # без GUI
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from pathlib import Path

# ─── Пути ────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent.parent
DATA  = BASE / 'data'  / 'module1_timeline.csv'
OUT   = BASE / 'output' / 'module1_timeline.png'
OUT.parent.mkdir(exist_ok=True)

# ─── Данные ──────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA)
df['date_parsed'] = pd.to_datetime(df['date'], format='%Y-%m')

sanctions = df[df['event_type'] == 'sanction'].copy()
releases  = df[df['event_type'] == 'model_release'].copy().reset_index(drop=True)

print(f"Санкций: {len(sanctions)}, релизов: {len(releases)}")

# ─── Цветовая схема по actor ─────────────────────────────────────────────────
ACTOR_COLORS = {
    'DeepSeek AI':             '#1f77b4',
    'Alibaba Cloud':           '#ff7f0e',
    'Tsinghua / Zhipu AI':    '#2ca02c',
    'Shanghai AI Laboratory':  '#9467bd',
    '01.AI':                   '#8c564b',
    'Baichuan AI':             '#e377c2',
    'Moonshot AI':             '#17becf',
    'IDEA Research':           '#bcbd22',
}

# ─── Swim lanes ───────────────────────────────────────────────────────────────
# Верхний ряд — крупные коммерческие лаборатории
top_lane_actors    = ['DeepSeek AI', 'Alibaba Cloud', 'Moonshot AI']
# Нижний ряд — академические и малые лаборатории
bottom_lane_actors = ['Tsinghua / Zhipu AI', 'Shanghai AI Laboratory',
                      '01.AI', 'Baichuan AI', 'IDEA Research']

def get_base_y(actor):
    return 0.35 if actor in top_lane_actors else -0.35

releases['y_base'] = releases['actor'].apply(get_base_y)

np.random.seed(42)
releases['y_jitter'] = releases['y_base'] + np.random.uniform(-0.12, 0.12, len(releases))

# Показывать подпись только крупным моделям и всем DeepSeek
show_label = (releases['params_B'] >= 20) | (releases['actor'] == 'DeepSeek AI')

# Размер маркера санкции по уровню жёсткости
def sanction_marker_size(level):
    lvl = int(float(level)) if pd.notna(level) else 2
    return {1: 80, 2: 140, 3: 200}.get(lvl, 140)

# ─── Фигура ───────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(22, 12), facecolor='white')
ax.set_facecolor('white')

# ─── Разделительная линия между рядами ───────────────────────────────────────
ax.axhline(y=0, color='#cccccc', linewidth=0.8, linestyle='-', alpha=0.5, zorder=1)

# ─── Подписи рядов слева ──────────────────────────────────────────────────────
ax.text(pd.Timestamp('2018-10-01'),  0.35, 'DeepSeek · Qwen · Kimi',
        fontsize=8, color='#666666', va='center', style='italic')
ax.text(pd.Timestamp('2018-10-01'), -0.35, 'ChatGLM · InternLM · Yi · Baichuan · YAYI',
        fontsize=8, color='#666666', va='center', style='italic')

# ─── СЛОЙ 1: Санкции (вертикальные линии + чередующиеся метки) ───────────────
sanctions_sorted = sanctions.sort_values('date_parsed')
for i, (_, row) in enumerate(sanctions_sorted.iterrows()):
    d  = row['date_parsed']
    ax.axvline(x=d, color='#d62728', alpha=0.7, linewidth=1.5, linestyle='--')
    sz = sanction_marker_size(row['chip_restriction_level'])
    # Чередование высоты, чтобы метки не сливались в плотной зоне
    marker_y = 1.05 if i % 2 == 0 else 1.12
    label_y  = 1.08 if i % 2 == 0 else 1.16
    ax.scatter(d, marker_y, marker='v', color='#d62728', s=sz, zorder=5)
    ax.text(d, label_y, row['event_name'],
            rotation=45, fontsize=7.5, color='#d62728',
            ha='left', va='bottom')

# ─── СЛОЙ 2: Релизы моделей (swim lanes) ─────────────────────────────────────
for idx, row in releases.iterrows():
    color = ACTOR_COLORS.get(row['actor'], '#7f7f7f')
    mkr   = 'D' if row['architecture_note'] == 'MoE' else 'o'
    sz    = 100 if row['architecture_note'] == 'MoE' else 80
    y     = row['y_jitter']

    ax.scatter(row['date_parsed'], y,
               color=color, marker=mkr, s=sz,
               zorder=5, alpha=0.85,
               edgecolors='white', linewidths=0.5)

    if show_label[idx]:
        label = row['event_name'].split('(')[0].strip()
        ax.annotate(label,
                    xy=(row['date_parsed'], y),
                    xytext=(0, 10),
                    textcoords='offset points',
                    fontsize=6.5, rotation=30,
                    ha='center', va='bottom',
                    color=color)

# ─── Ось X ───────────────────────────────────────────────────────────────────
ax.set_xlim(pd.Timestamp('2018-09-01'), pd.Timestamp('2025-09-01'))

locator   = mdates.MonthLocator(interval=6)
formatter = mdates.DateFormatter('%Y-%m')
ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax.tick_params(axis='x', labelsize=9)

# ─── Ось Y ───────────────────────────────────────────────────────────────────
ax.yaxis.set_visible(False)
ax.set_ylim(-1.0, 1.6)

# ─── Заголовок ───────────────────────────────────────────────────────────────
ax.set_title(
    'Санкции США и релизы китайских open-source моделей ИИ (2019–2025)',
    fontsize=14, fontweight='bold', pad=20
)

# ─── Легенда ─────────────────────────────────────────────────────────────────
family_labels = {
    'DeepSeek':  '#1f77b4',
    'Qwen':      '#ff7f0e',
    'ChatGLM':   '#2ca02c',
    'InternLM':  '#9467bd',
    'Yi':        '#8c564b',
    'Baichuan':  '#e377c2',
    'Kimi':      '#17becf',
    'YAYI':      '#bcbd22',
}
family_handles = [
    mpatches.Patch(color=c, label=l)
    for l, c in family_labels.items()
]

arch_handles = [
    mlines.Line2D([], [], marker='D', color='gray', linestyle='None',
                  markersize=8, label='MoE (ромб)'),
    mlines.Line2D([], [], marker='o', color='gray', linestyle='None',
                  markersize=8, label='Dense (круг)'),
]

sanction_handles = [
    mlines.Line2D([], [], color='#d62728', linestyle='--', linewidth=1.5,
                  label='Санкционное событие'),
    mlines.Line2D([], [], marker='v', color='#d62728', linestyle='None',
                  markersize=6,  label='Уровень 1 (s=80)'),
    mlines.Line2D([], [], marker='v', color='#d62728', linestyle='None',
                  markersize=9,  label='Уровень 2 (s=140)'),
    mlines.Line2D([], [], marker='v', color='#d62728', linestyle='None',
                  markersize=12, label='Уровень 3 (s=200)'),
]

sep = mpatches.Patch(color='none', label=' ')
all_handles = family_handles + [sep] + arch_handles + [sep] + sanction_handles

ax.legend(
    handles=all_handles,
    bbox_to_anchor=(1.01, 1), loc='upper left',
    fontsize=8, frameon=True, framealpha=0.9,
    title='Легенда', title_fontsize=9,
    borderpad=0.8, labelspacing=0.5
)

# ─── Аннотация источников ────────────────────────────────────────────────────
ax.annotate(
    'Источники: Federal Register (BIS), GitHub, Hugging Face. Составлено автором.',
    xy=(1, 0), xycoords='axes fraction',
    fontsize=8, color='gray', ha='right', va='top',
    xytext=(0, -40), textcoords='offset points'
)

# ─── Рамка ───────────────────────────────────────────────────────────────────
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

# ─── Сохранение ──────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(OUT), dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()
print(f"Сохранено: {OUT}")
