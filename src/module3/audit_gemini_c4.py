import pandas as pd

df = pd.read_csv('data/module3/module3_classified.csv')

print('--- GEMINI C4 ---')
gemini_c4 = df[(df['model_short'] == 'gemini-3.1fl') & (df['prompt_id'] == 'C4')]
for i, row in gemini_c4.iterrows():
    text_val = str(row['response'])
    print(f'Row {i}: Text={repr(text_val[:200])}..., Sanction={row["sanction_frame"]}')
