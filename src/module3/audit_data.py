import pandas as pd

df = pd.read_csv('data/module3/module3_classified.csv')

print('--- KIMI C4 ---')
kimi_c4 = df[(df['model_short'] == 'kimi-k2') & (df['prompt_id'] == 'C4')]
for i, row in kimi_c4.iterrows():
    text_val = str(row['response'])
    print(f'Row {i}: Text={repr(text_val[:100])}..., Refusal={row["refusal_type"]}')

print('\n--- GEMINI B-BLOCK SAMPLES ---')
gemini_b = df[(df['model_short'] == 'gemini-3.1fl') & (df['prompt_id'].str.startswith('B'))].head(4)
for i, row in gemini_b.iterrows():
    text_val = str(row['response'])
    print(f'Row {i}: Prompt={row["prompt_id"]}, Sanction={row["sanction_frame"]}, Text={repr(text_val[:150])}...')
