const FXAIX_URL = "https://fundresearch.fidelity.com/mutual-funds/api/v1/investments/315911750/summary?funduniverse=RETAIL"

function sortByNetExpenseRatio(arr) {
  return [...arr].sort((a, b) => {
    const aRatio = a.net_expense_ratio;
    const bRatio = b.net_expense_ratio;

    if (aRatio == null && bRatio == null) return 0;
    if (aRatio == null) return 1;
    if (bRatio == null) return -1;

    return aRatio - bRatio;
  });
}

