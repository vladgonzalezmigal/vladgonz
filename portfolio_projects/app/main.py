import json
from datetime import datetime
from fund_data_utils import get_fund_data

def sort(array):
    """Sort array by netExpenseRatio, converting percentages to numbers for sorting"""
    return sorted(array, key=lambda x: x['netExpenseRatio'])

def process(data):
    # Clean the expense ratio columns by removing percentage signs
    for fund in data:
        if fund['netExpenseRatio'] != "N/A" and fund['netExpenseRatio'].endswith('%'):
            fund['netExpenseRatio'] = fund['netExpenseRatio'][:-1]
        if fund['grossExpenseRatio'] != "N/A" and fund['grossExpenseRatio'].endswith('%'):
            fund['grossExpenseRatio'] = fund['grossExpenseRatio'][:-1]
    
    cleaned_data = sort(data)
    return cleaned_data

def get_fund_data_json():
    """Get fund data and return as JSON structure"""
    processed_data = process(get_fund_data())
    metadata = {
        "created": datetime.now().strftime("%Y-%m-%d")
    }
    
    result = {
        "data": processed_data,
        "metadata": metadata
    }
    
    return result

if __name__ == '__main__':
    result = get_fund_data_json()
    print(json.dumps(result, indent=2)) # print and save in file as needed