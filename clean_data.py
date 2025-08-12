#!/usr/bin/env python3
"""
Data cleaning script for Coffee Shop Sales Analysis
"""

import sys
sys.path.append('.')
from src.utils.data_loader import DataLoader
from src.data_processing.data_cleaner import clean_coffee_shop_data
from config.config import RAW_DATA_FILE, CLEANED_DATA_PATH, REPORTS_PATH, get_config

def main():
    print('🧹 Starting data cleaning process...')

    try:
        # Load raw data
        loader = DataLoader(RAW_DATA_FILE)
        raw_data = loader.load_data(sheet_name='Transactions')
        print(f'📊 Loaded raw data: {raw_data.shape[0]:,} rows × {raw_data.shape[1]} columns')

        # Clean data
        config = get_config()
        cleaned_data, cleaner = clean_coffee_shop_data(raw_data, config)

        # Show cleaning summary
        summary = cleaner.get_cleaning_summary()
        print(f'\n📈 Cleaning Summary:')
        print(f'   Original rows: {summary["original_shape"][0]:,}')
        print(f'   Final rows: {summary["final_shape"][0]:,}')
        print(f'   Rows removed: {summary["rows_removed"]:,}')
        print(f'   Retention rate: {summary["retention_rate"]:.2f}%')

        # Save cleaned data
        cleaned_file_path = CLEANED_DATA_PATH / 'coffee_shop_sales_cleaned.csv'
        cleaned_data.to_csv(cleaned_file_path, index=False)

        # Save cleaning log
        cleaner.save_cleaning_log(REPORTS_PATH)

        print(f'\n💾 Files saved:')
        print(f'   Cleaned data: {cleaned_file_path}')
        print(f'   Cleaning log: {REPORTS_PATH / "data_cleaning_log.txt"}')
        print(f'\n🎉 Data cleaning completed successfully!')
        
        return True
        
    except Exception as e:
        print(f'❌ Error during cleaning: {str(e)}')
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
