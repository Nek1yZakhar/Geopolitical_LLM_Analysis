import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.dates as mdates
import numpy as np

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

# Точки и подписи для каждой санкции
for i, row in sanctions.iterrows():
    # Цвет зависит от подтипа (законодательство/отмена) или уровня
    subtype = row['event_subtype']
    if subtype in type_colors:
        color = type_colors[subtype]
    else:
        level = int(row['chip_restriction_level'])
        color = level_colors.get(level, '#999999')
    
    # Цветная точка
    ax.scatter(row['date_parsed'], i, 
               s=120, color=color, zorder=5, edgecolors='white', linewidth=1.5)
    
    # Название СЛЕВА от точки
    ax.text(row['date_parsed'] - pd.Timedelta(days=45), i,
            row['event_name'],
            fontsize=9, color='#222222', ha='right', va='center', fontweight='normal')
    
    # Год СПРАВА от точки
    ax.text(row['date_parsed'] + pd.Timedelta(days=45), i,
            row['date_parsed'].strftime('%Y-%m'),
            fontsize=8, color='#666666', ha='left', va='center')

# Ось X снизу — только годы
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.tick_params(axis='x', labelsize=9)
ax.yaxis.set_visible(False)
ax.spines[['top', 'right', 'left']].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')

# Легенда
level_patches = [mpatches.Patch(color=level_colors[k], label=f'Уровень {k}') for k in [1, 2, 3]]
type_labels = {'legislation': 'Законодательство (CHIPS)', 'policy_reversal': 'Отмена ограничений'}
type_patches  = [mpatches.Patch(color=type_colors[k], label=type_labels.get(k, k.capitalize())) for k in type_colors]
ax.legend(handles=level_patches + type_patches, loc='lower right', fontsize=8.5, framealpha=0.95, edgecolor='#cccccc')

ax.set_title('Рисунок 1 — Санкционные раунды США в сфере ИИ\nи полупроводников (2019–2025)',
             fontsize=12, fontweight='bold', pad=12, loc='left')
ax.text(0.0, -0.08, 'Источник: BIS Federal Register; congress.gov. Составлено автором.',
        transform=ax.transAxes, fontsize=7.5, color='#999999')

plt.tight_layout()
plt.savefig('output/module1_sanctions_timeline.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ График 1 сохранён (ГОСТ)")


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
    'Trump EO — Biden Diffusion Rule Revocation': 'Trump EO'
}

fig, ax = plt.subplots(figsize=(14, 18), facecolor='white')
ax.set_facecolor('white')
plt.subplots_adjust(top=0.93, bottom=0.07, left=0.12, right=0.88)
ax.set_xlim(pd.Timestamp('2023-01-01'), pd.Timestamp('2025-09-01'))
ax.set_ylim(-0.5, len(releases) - 0.5)

# Горизонтальные направляющие
for i in range(len(releases)):
    ax.axhline(y=i, color='#f0f0f0', linewidth=0.5, zorder=0)

# Вертикальные линии санкций
level_colors_s = {1: '#f4a582', 2: '#d6604d', 3: '#8b0000'}
type_colors_s  = {'legislation': '#4A90D9', 'policy_reversal': '#E8A838'}

sanctions_2023 = sanctions[sanctions['date_parsed'] >= pd.Timestamp('2023-01-01')].sort_values(['date_parsed', 'event_name']).copy()
last_date = None
collision_count = 0

for _, row in sanctions_2023.iterrows():
    subtype = row['event_subtype']
    color = type_colors_s.get(subtype, level_colors_s.get(int(row['chip_restriction_level']), '#999999'))
    
    ax.axvline(x=row['date_parsed'], color=color, linewidth=1.0, linestyle='--', alpha=0.5, zorder=1)
    
    # Исключение наложений
    if row['date_parsed'] == last_date:
        collision_count += 1
    else:
        collision_count = 0
        last_date = row['date_parsed']
    
    x_offset_days = 5 + (collision_count * 15)
    # Сдвигаем подписи на высоту, обозначенную пользователем (центр графика)
    # По визуальной оценке линии это примерно y=17
    y_pos = 17
    x_pos = row['date_parsed'] - pd.Timedelta(days=x_offset_days)
    
    # Сокращенное название
    label_text = abbreviations.get(row['event_name'], row['event_name'][:20])
    ax.text(x_pos, y_pos, label_text, fontsize=8, rotation=90, va='center', ha='right', 
            color=color, alpha=0.95, zorder=6)

# Точки моделей (с Jitter по Y для плотных кластеров)
releases['y_pos'] = range(len(releases))
releases['y_pos'] = releases['y_pos'].astype(float)
# Добавляем jitter для кластера 2023-06
cluster_2023_06 = releases[releases['date_parsed'] == '2023-06-01']
if not cluster_2023_06.empty:
    offsets = [-0.15, 0.0, 0.15]
    for idx, (original_idx, row) in enumerate(cluster_2023_06.iterrows()):
        releases.loc[original_idx, 'y_pos'] += offsets[idx % len(offsets)]

for _, row in releases.iterrows():
    actor = row['actor']
    color = color_map.get(actor, '#999999')
    is_open = bool(row['open_weight'])
    
    # Открытый вес = закрашенная точка, Закрытый (проприетарный) = пустой круг
    if is_open:
        ax.scatter(row['date_parsed'], row['y_pos'], s=100, color=color, zorder=5, edgecolors='white', linewidth=1.2)
    else:
        ax.scatter(row['date_parsed'], row['y_pos'], s=100, facecolors='none', zorder=5, edgecolors=color, linewidth=1.5)
    
    ax.text(row['date_parsed'] + pd.Timedelta(days=12), row['y_pos'], row['event_name'], fontsize=8, color='#222222', ha='left', va='center')
    ax.text(row['date_parsed'] - pd.Timedelta(days=12), row['y_pos'], row['date_parsed'].strftime('%Y-%m'), fontsize=7.5, color='#888888', ha='right', va='center')

ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1,4,7,10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.tick_params(axis='x', rotation=45, labelsize=8)
ax.yaxis.set_visible(False)
ax.spines[['top','right','left']].set_visible(False)
ax.spines['bottom'].set_color('#cccccc')

# Легенда
from matplotlib.lines import Line2D
legend_elements = [mpatches.Patch(color=v, label=k) for k, v in color_map.items() if k in releases['actor'].values]
legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Open-source', markerfacecolor='gray', markersize=7, linestyle='None'))
legend_elements.append(Line2D([0], [0], marker='o', color='gray', label='Proprietary (closed)', markerfacecolor='none', markersize=7, linestyle='None'))
legend_elements.append(Line2D([0], [0], color='#d6604d', linewidth=1.2, linestyle='--', label='Экспортный контроль'))
legend_elements.append(Line2D([0], [0], color='#4A90D9', linewidth=1.2, linestyle='--', label='Законодательство (CHIPS)'))
legend_elements.append(Line2D([0], [0], color='#E8A838', linewidth=1.2, linestyle='--', label='Отмена ограничений'))

ax.legend(handles=legend_elements, title='Организация и тип', loc='upper left', fontsize=8, title_fontsize=8.5, framealpha=0.95, edgecolor='#cccccc')

ax.set_title('Рисунок 2 — Релизы китайских open-source моделей ИИ\nна фоне санкционных раундов США (2023–2025)',
             fontsize=12, fontweight='bold', pad=12, loc='left')
ax.text(0.0, -0.08, 'Источник: GitHub; Hugging Face; Meinhardt et al., 2025. Составлено автором.',
        transform=ax.transAxes, fontsize=7.5, color='#999999')

plt.tight_layout()
plt.savefig('output/module1_releases_bar.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.close()
print("✅ График 2 сохранён (ГОСТ)")
