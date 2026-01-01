import { useState } from "react";
import CustomerList from "../components/CustomerList";  // Changed from CustomerInfoForm to CustomerList
import BillingPeriodForm from "../components/BillingPeriodForm";
import LoanList from "../components/LoanList";
import FormatSelector from "../components/FormatSelector";
import type { Customer, Loan, StatementRequest } from "../types/statement";
import { generateStatement } from "../services/api";

export default function StatementGeneratorPage() {
  const [billingStart, setBillingStart] = useState("");
  const [billingEnd, setBillingEnd] = useState("");
  const [format, setFormat] = useState<"pdf" | "xlsx" | "txt">("pdf");
  
  // Changed from single customer to array of customers
  const [customers, setCustomers] = useState<Customer[]>([{
    customer_id: "",
    name: "",
    address: "",
    phone: "",
    email: ""
  }]);

  const [loans, setLoans] = useState<Loan[]>([{
    loan_id: "", 
    loan_type: "",
    principal: "", 
    interest_rate: "",
    term_months: "", 
    current_balance: "",
    payment_due_date: "", 
    monthly_payment: "" 
  }]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // For backward compatibility with current backend that expects single customer
    // You have 3 options:

    // OPTION 1: Use first customer only (temporary until backend is updated)
    const payload: StatementRequest = {
      customer: customers[0],  // Just use the first customer for now
      billing_period_start: billingStart,
      billing_period_end: billingEnd,
      loans,
      statement_format: format
    };

    // OPTION 2: If you want to send all customers to updated backend:
    /*
    const payload = {
      customers,  // Send array instead of single customer
      billing_period_start: billingStart,
      billing_period_end: billingEnd,
      loans,
      statement_format: format
    };
    */

    // OPTION 3: Generate separate statements for each customer
    /*
    for (const customer of customers) {
      const payload: StatementRequest = {
        customer,
        billing_period_start: billingStart,
        billing_period_end: billingEnd,
        loans,
        statement_format: format
      };
      const blob = await generateStatement(payload);
      // Download each separately or combine
    }
    */

    try {
      const blob = await generateStatement(payload);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      
      // Create a filename with customer names if multiple
      let filename = "statement";
      if (customers.length === 1 && customers[0].name) {
        filename = customers[0].name.replace(/\s+/g, "_") + "_statement";
      } else if (customers.length > 1) {
        filename = "multi_customer_statement";
      }
      
      a.href = url;
      a.download = `${filename}.${format}`;
      a.click();
    } catch (error) {
      console.error("Error generating statement:", error);
      alert("Error generating statement. Please check the console for details.");
    }
  };

  // Optional: Show a warning if backend doesn't support multiple customers
  const showBackendWarning = customers.length > 1;

  return (
    <div style={{ 
      padding: "2rem", 
      maxWidth: "800px", 
      margin: "auto",
      backgroundColor: "#f8f9fa",
      borderRadius: "12px",
      boxShadow: "0 4px 12px rgba(0,0,0,0.1)"
    }}>
      <h1 style={{ 
        textAlign: "center", 
        color: "#2c3e50",
        marginBottom: "1.5rem",
        fontSize: "2.2rem"
      }}>
        Statement Generator
      </h1>

      {showBackendWarning && (
        <div style={{
          backgroundColor: "#fff3cd",
          border: "1px solid #ffeaa7",
          borderRadius: "8px",
          padding: "1rem",
          marginBottom: "1.5rem",
          color: "#856404"
        }}>
          ⚠️ <strong>Note:</strong> The backend currently supports single customer only. 
          Only the first customer will be included in the statement. 
          Update your backend to support multiple customers.
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {/* Replace CustomerInfoForm with CustomerList */}
        <div style={{
          backgroundColor: "white",
          padding: "1.5rem",
          borderRadius: "8px",
          marginBottom: "1.5rem",
          boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
        }}>
          <CustomerList 
            customers={customers}
            setCustomers={setCustomers}
          />
        </div>

        <div style={{
          backgroundColor: "white",
          padding: "1.5rem",
          borderRadius: "8px",
          marginBottom: "1.5rem",
          boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
        }}>
          <BillingPeriodForm
            billingStart={billingStart}
            billingEnd={billingEnd}
            setBillingStart={setBillingStart}
            setBillingEnd={setBillingEnd}
          />
        </div>

        <div style={{
          backgroundColor: "white",
          padding: "1.5rem",
          borderRadius: "8px",
          marginBottom: "1.5rem",
          boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
        }}>
          <LoanList loans={loans} setLoans={setLoans} />
        </div>

        <div style={{
          backgroundColor: "white",
          padding: "1.5rem",
          borderRadius: "8px",
          marginBottom: "1.5rem",
          boxShadow: "0 2px 4px rgba(0,0,0,0.05)"
        }}>
          <FormatSelector format={format} setFormat={setFormat} />
        </div>

        <div style={{ 
          textAlign: "center",
          marginTop: "2rem"
        }}>
          <button 
            type="submit"
            style={{
              padding: "0.8rem 2rem",
              fontSize: "1.1rem",
              backgroundColor: "#3498db",
              color: "white",
              border: "none",
              borderRadius: "8px",
              cursor: "pointer",
              fontWeight: "bold",
              transition: "background-color 0.3s",
              minWidth: "200px"
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = "#2980b9"}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = "#3498db"}
          >
            Generate Statement
          </button>
          
          <div style={{ 
            marginTop: "1rem",
            fontSize: "0.9rem",
            color: "#7f8c8d"
          }}>
            {customers.length} customer(s) • {loans.length} loan(s)
          </div>
        </div>
      </form>
    </div>
  );
}