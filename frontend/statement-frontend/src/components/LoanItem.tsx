import type { Loan } from "../types/statement";

interface Props {
  loan: Loan;
  index: number;
  updateLoan: (index: number, field: keyof Loan, value: string) => void;
}

export default function LoanItem({ loan, index, updateLoan }: Props) {
  return (
    <div style={{ marginBottom: "1rem", borderBottom: "1px solid #ccc" }}>
      <input
        placeholder="Loan Type"
        value={loan.loan_type}
        onChange={(e) => updateLoan(index, "loan_type", e.target.value)}
      />
      <input
  placeholder="Loan ID"
  value={loan.loan_id}
  onChange={(e) => updateLoan(index, "loan_id", e.target.value)}
/>
<input
  placeholder="Term (months)"
  value={loan.term_months}
  onChange={(e) => updateLoan(index, "term_months", e.target.value)}
/>
      <input
        placeholder="Principal"
        value={loan.principal}
        onChange={(e) => updateLoan(index, "principal", e.target.value)}
      />
      <input
        placeholder="Interest Rate"
        value={loan.interest_rate}
        onChange={(e) => updateLoan(index, "interest_rate", e.target.value)}
      />
      <input
        placeholder="Current Balance"
        value={loan.current_balance}
        onChange={(e) => updateLoan(index, "current_balance", e.target.value)}
      />
        <span style={{ display: "inline-block", marginLeft: "1rem" }}>Payment Due Date:
      <input
        type="date"
        placeholder="Payment Due Date"
        value={loan.payment_due_date}
        onChange={(e) => updateLoan(index, "payment_due_date", e.target.value)}
      /></span>
      <input
  placeholder="Monthly Payment"
  value={loan.monthly_payment}
  onChange={(e) => updateLoan(index, "monthly_payment", e.target.value)}
/>
    </div>
  );
}