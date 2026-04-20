import pandas as pd
import json
import glob
import os

# Paths
RAW_CSV = r'c:\Users\Admin\Desktop\All_modules\data\data_module_2\module2_responses.csv'
BATCH_DIR = r'c:\Users\Admin\Desktop\All_modules\data\data_module_3'
OUTPUT_CSV = r'c:\Users\Admin\Desktop\All_modules\data\data_module_3\module3_classified.csv'

def merge_batches():
    # Load raw data
    df = pd.read_csv(RAW_CSV)
    
    # Collect all classifications
    all_classifications = []
    batch_files = glob.glob(os.path.join(BATCH_DIR, 'batch_*_classified.json'))
    
    for f in batch_files:
        with open(f, 'r', encoding='utf-8') as jfile:
            data = json.load(jfile)
            all_classifications.extend(data)
    
    # Create classification DF
    class_df = pd.DataFrame(all_classifications)
    
    # Merge on index
    # We use 'index' column from JSON to align with original DF indices
    result_df = df.copy()
    
    # Initialize new columns
    result_df['tone'] = None
    result_df['sanction_frame'] = None
    result_df['refusal_type'] = None
    
    for _, item in class_df.iterrows():
        idx = int(item['index'])
        result_df.at[idx, 'tone'] = item['tone']
        result_df.at[idx, 'sanction_frame'] = item['sanction_frame']
        result_df.at[idx, 'refusal_type'] = item['refusal_type']
    
    # Save
    result_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Final dataset saved to {OUTPUT_CSV}")
    print(f"Total rows: {len(result_df)}")
    print(f"Classified rows: {class_df.shape[0]}")

if __name__ == "__main__":
    merge_batches()
