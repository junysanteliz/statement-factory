import type { Loan } from "../types/statement";
import LoanItem from "./LoanItem";

interface Props {
  loans: Loan[];
  setLoans: (loans: Loan[]) => void;
}

export default function LoanList({ loans, setLoans }: Props) {
  const updateLoan = (index: number, field: keyof Loan, value: string) => {
    const updated = [...loans];
    updated[index][field] = value;
    setLoans(updated);
  };

  const addLoan = () => {
  setLoans([
    ...loans,
    {
      loan_id: "",
      loan_type: "",
      principal: "",
      interest_rate: "",
      term_months: "",
      current_balance: "",
      payment_due_date: "",
        monthly_payment: ""
    }
  ]);
};


  return (
    <div>
      <h3>Loans</h3>

      {loans.map((loan, index) => (
        <LoanItem
          key={index}
          loan={loan}
          index={index}
          updateLoan={updateLoan}
        />
      ))}

      <button type="button" onClick={addLoan}>
        Add Loan
      </button>
    </div>
  );
}