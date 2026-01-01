import { useState } from "react";
import CustomerInfoForm from "../components/CustomerInfoForm";
import BillingPeriodForm from "../components/BillingPeriodForm";
import LoanList from "../components/LoanList";
import FormatSelector from "../components/FormatSelector";
import type { Loan, StatementRequest } from "../types/statement";
import { generateStatement } from "../services/api";

export default function StatementGeneratorPage() {
  const [billingStart, setBillingStart] = useState("");
  const [billingEnd, setBillingEnd] = useState("");
  const [format, setFormat] = useState<"pdf" | "xlsx" | "txt">("pdf");
  const [customer, setCustomer] = useState({
        customer_id: "",
        name: "",
        address: "",
        phone: "",
        email: ""
    });

  const [loans, setLoans] = useState<Loan[]>([
  {
    loan_id: "", loan_type: "",
    principal: "", interest_rate: "",
    term_months: "", current_balance: "",
    payment_due_date: "", monthly_payment: "" 
  }]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const payload: StatementRequest = {
        customer,
        billing_period_start: billingStart,
        billing_period_end: billingEnd,
        loans,
        statement_format: format
    };

    const blob = await generateStatement(payload);

    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `statement.${format}`;
    a.click();
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "700px", margin: "auto" }}>
      <h1>Loan Statement Generator</h1>

      <form onSubmit={handleSubmit}>
        <CustomerInfoForm
            customer={customer}
            setCustomer={setCustomer}
        />


        <BillingPeriodForm
          billingStart={billingStart}
          billingEnd={billingEnd}
          setBillingStart={setBillingStart}
          setBillingEnd={setBillingEnd}
        />

        <LoanList loans={loans} setLoans={setLoans} />

        <FormatSelector format={format} setFormat={setFormat} />

        <br />
        <button type="submit">Generate Statement</button>
      </form>
    </div>
  );
}