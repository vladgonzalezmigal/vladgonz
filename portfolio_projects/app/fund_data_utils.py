import requests
from datetime import datetime

from lxml import html

def parse_fxaix(data):
    fxaix_data = data.json()
    details = fxaix_data.get('details',None).get('subjectAreaData',None)
    if details:
        gross_expense_ratio = details.get('grossExpenseRatio',None)
        net_expense_ratio = details.get('netExpenseRatio',None)
        gross_expense_ratio['grossAsOfDate'] = gross_expense_ratio.pop('asOfDate', 'N/A')
        gross_expense_ratio['grossExpenseRatio'] = gross_expense_ratio.pop('amount', 'N/A')
        net_expense_ratio['netExpenseRatio'] = net_expense_ratio.pop('amount', 'N/A')
        net_expense_ratio['netAsOfDate'] = net_expense_ratio.pop('asOfDate', 'N/A')
        return gross_expense_ratio | net_expense_ratio

def parse_voo(data):
    voo_data = data.json()
    expense_ratio = voo_data.get('expenseRatio',None)
    as_of_date = voo_data.get('expenseRatioAsOfDate',None)
    as_of_date = datetime.fromisoformat(as_of_date).strftime("%m/%d/%Y")
    return {'grossAsOfDate' : as_of_date, 'netAsOfDate' : as_of_date, 'netExpenseRatio' : expense_ratio, 'grossExpenseRatio' : expense_ratio }

def parse_swpxx(data):
    tree = html.fromstring(data.text)
    
    # Extract gross expense ratio
    gross_expense_ratio = None
    gross_row = tree.xpath("//th[contains(text(), 'Gross Expense Ratio')]/following-sibling::td[@class='data']")
    if gross_row:
        gross_expense_ratio = gross_row[0].text_content().strip()
    
    # Extract net expense ratio
    net_expense_ratio = None
    net_row = tree.xpath("//th[contains(text(), 'Net Expense Ratio')]/following-sibling::td[@class='data']")
    if net_row:
        net_expense_ratio = net_row[0].text_content().strip()
    
    # Extract the as of date
    as_of_date = None
    date_td = tree.xpath("//td[@class='asOfDate fright']")
    if date_td:
        as_of_date = date_td[0].text_content().strip()
        if as_of_date.lower().startswith("as of "):
            as_of_date = as_of_date[6:].strip()

    return {'grossAsOfDate' : as_of_date, 'netAsOfDate' : as_of_date, 'netExpenseRatio' : net_expense_ratio, 'grossExpenseRatio' : gross_expense_ratio }

def parse_spy(data):
    tree = html.fromstring(data.text)
    
    # Extract the date from h2 with "Fund Information"
    date_span = tree.xpath("//h2[contains(text(), 'Fund Information')]/span[@class='date']/text()")
    date = None
    if date_span:
        # Remove "as of " prefix and get just the date
        date = date_span[0].strip().replace("as of ", "")
        date = datetime.strptime(date, "%b %d %Y").strftime("%m/%d/%Y")
    
    # Extract gross expense ratio
    gross_expense_ratio = None
    gross_row = tree.xpath("//tr[.//td[@class='label'][contains(text(), 'Gross Expense Ratio')]]//td[@class='data']/text()")
    if gross_row:
        gross_expense_ratio = gross_row[0].strip()
    
    return {'grossAsOfDate' : date, 'netAsOfDate' : date, 'netExpenseRatio' : gross_expense_ratio, 'grossExpenseRatio' : gross_expense_ratio }


def parse_ivv(data):
    tree = html.fromstring(data.text)
    
    # Extract expense ratio by finding the span with "Fees as stated in the prospectus" and getting the next sibling
    expense_ratio = None
    fees_span = tree.xpath("//span[contains(text(), 'Fees as stated in the prospectus')]")
    
    if fees_span:
        # Get the next sibling element which should contain the expense ratio
        next_sibling = fees_span[0].getnext()
        if next_sibling is not None:
            text = next_sibling.text_content().strip()
            if "Expense Ratio:" in text:
                expense_ratio = text.split("Expense Ratio:")[1].strip()
    else:
        print("no fees span found")
    
    current_date = datetime.now()
    first_day = current_date.replace(day=1).strftime("%m/%d/%Y")

    return {'grossAsOfDate' : first_day, 'netAsOfDate' : first_day, 'netExpenseRatio' : expense_ratio, 'grossExpenseRatio' : expense_ratio }

sp500_funds = {
    "FXAIX": {
        "url": "https://fundresearch.fidelity.com/mutual-funds/api/v1/investments/315911750/summary?funduniverse=RETAIL",
        "public_url" : "https://fundresearch.fidelity.com/mutual-funds/summary/315911750",
        "headers": None,
        "name": "Fidelity 500 Index Fund",
        "type" : "Mutual Fund",
        "parser": parse_fxaix,
    },
    "VOO": {
        "url": "https://investor.vanguard.com/vmf/api/VOO/expense",
        "public_url" : "https://investor.vanguard.com/investment-products/etfs/profile/voo",
        "headers": None,
        "name": "Vanguard S&P 500 ETF",
        "type" : "ETF",
        "parser": parse_voo,
    },
    "SWPXX": {
        "url": "https://www.schwab.wallst.com/Prospect/Research/mutualfunds/fees.asp?symbol=swppx#schwab-responsive-iframe--58091",
        "public_url" : "https://www.schwabassetmanagement.com/products/swppx",
        "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }, 
        "name": "Schwab S&P 500 Index Fund SWPPX",
        "type" : "Mutual Fund",
        "parser": parse_swpxx,
    },
    "SPY": {
        "url": "https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy",
        "public_url" : "https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy",
        "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Content-Type": "application/json"
            }, 
        "name": "SPDR S&P 500 ETF",
        "type" : "ETF",
        "parser": parse_spy,
    },
    "IVV": {
        "url": "https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf",
        "public_url" : "https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf",
        "headers": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Content-Type": "application/json"
        }, 
        "name": "iShares Core S&P 500 ETF",
        "type": "ETF", 
        "parser": parse_ivv,
    }
}

def get_fund_data():
    funds_table = []
    for ticker in sp500_funds:
        fund_data = { "ticker" : ticker, "url": sp500_funds[ticker]["public_url"], 
                     "type" : sp500_funds[ticker]["type"],
                     "fullName" :  sp500_funds[ticker]["name"] }
        expense_ratio_data = {'grossAsOfDate' : "N/A", 'netAsOfDate' :  "N/A", 'netExpenseRatio' :  "N/A", 'grossExpenseRatio' :  "N/A" }
        response = requests.get(sp500_funds[ticker]["url"],headers=sp500_funds[ticker]["headers"])
        if response.status_code == 200:
            expense_ratio_data = sp500_funds[ticker]["parser"](response)
        else:
            print(f"Error getting data for {ticker}, {response.status_code}: {response.text}")
        funds_table.append(fund_data | expense_ratio_data)
    return funds_table