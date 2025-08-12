class FundsTable extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
  }

  connectedCallback() {
    this.render();
  }

  set data(funds) {
    this._data = funds;
    this.render();
  }

  formatExpenseRatio(ratio) {
    if (ratio == null) return "-";
    if (ratio < 1) return (ratio * 100).toFixed(2) + "%";
    return parseFloat(ratio).toFixed(2) + "%";
  }

  formatDate(dateStr) {
    if (!dateStr) return "-";
    // Accepts MM/DD/YYYY or YYYY-MM-DD
    let d;
    // If dateStr is MM/DD/YYYY
    if (/^\d{2}\/\d{2}\/\d{4}$/.test(dateStr)) {
      const [month, day, year] = dateStr.split("/");
      d = new Date(`${year}-${month}-${day}`);
    } else {
      // Try parsing as ISO or fallback
      d = new Date(dateStr);
    }
    if (isNaN(d.getTime())) return dateStr;
    return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
  }

  escapeHtml(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  render() {
    if (!this._data) return;

    const rows = this._data
      .map(r => `
        <tr>
          <td><strong>${this.escapeHtml(r.ticker)}</strong></td>
          <td>${this.escapeHtml(r.name)}</td>
          <td class="muted">${this.escapeHtml(r.type)}</td>
          <td>${this.formatExpenseRatio(r.net_expense_ratio)}</td>
          <td>${this.formatDate(r.updated_at)}</td>
        </tr>
      `)
      .join("");

    this.shadowRoot.innerHTML = `
      <style>
        .table-wrap {
          max-width: 1000px;
          margin: 24px auto;
          padding: 0 12px;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        }
        thead th {
          text-align: left;
          padding: 10px 12px;
          border-bottom: 2px solid #e6e6e6;
          font-weight: 600;
          background: #fafafa;
        }
        tbody td {
          padding: 10px 12px;
          border-bottom: 1px solid #f0f0f0;
        }
        tbody tr:hover { background: #fcfcfc; }
        .muted { color: #666; font-size: 0.95em; }
        @media (max-width: 600px) {
          .table-wrap { overflow-x: auto; }
        }
      </style>
      <div class="table-wrap" aria-live="polite">
        <table role="table" aria-label="Funds and ETFs">
          <thead>
            <tr>
              <th scope="col">Ticker</th>
              <th scope="col">Full name</th>
              <th scope="col">Type</th>
              <th scope="col">Net Expense Ratio</th>
              <th scope="col">Last updated</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
    `;
  }
}

customElements.define("funds-table", FundsTable);
