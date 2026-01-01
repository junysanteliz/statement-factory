import { useState } from "react";
import CustomerList from "../components/CustomerList";
import BillingPeriodForm from "../components/BillingPeriodForm";
import LoanList from "../components/LoanList";
import FormatSelector from "../components/FormatSelector";
import type { Customer, Loan } from "../types/statement";
import { generateStatement } from "../services/api"; // This is now the smart function

export default function StatementGeneratorPage() {
  const [billingStart, setBillingStart] = useState("");
  const [billingEnd, setBillingEnd] = useState("");
  const [format, setFormat] = useState<"pdf" | "xlsx" | "txt">("pdf");
  
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

    console.log(`Submitting ${customers.length} customer(s):`, customers);

    try {
      // ✅ Use the new generateStatement function that accepts separate parameters
      const blob = await generateStatement(
        customers,      // Customer array
        loans,          // Loan array  
        billingStart,   // Billing start
        billingEnd,     // Billing end
        format          // Format
      );
      
      // Create filename
      let filename = "statement";
      if (customers.length === 1 && customers[0].name.trim()) {
        const customerName = customers[0].name.trim();
        filename = customerName ? customerName.replace(/\s+/g, "_") + "_statement" : "statement";
      } else if (customers.length > 1) {
        // Get first names for joint statement
        const firstNames = customers
          .map(c => {
            const nameParts = c.name.trim().split(' ');
            return nameParts.length > 0 && nameParts[0] ? nameParts[0] : "";
          })
          .filter(name => name)
          .join('_');
        
        filename = firstNames ? `${firstNames}_joint_statement` : "joint_statement";
      }
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${filename}.${format}`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error("Error generating statement:", error);
      alert(`Error: ${error instanceof Error ? error.message : 'Failed to generate statement'}`);
    }
  };

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

      <form onSubmit={handleSubmit}>
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
          
          {/* Status indicator */}
          <div style={{ 
            marginTop: "0.5rem",
            fontSize: "0.8rem",
            color: customers.length > 1 ? "#27ae60" : "#7f8c8d"
          }}>
            {customers.length > 1 
              ? `✓ Will generate joint statement via /generate-statement endpoint` 
              : `✓ Will generate single statement via /statements endpoint`}
          </div>
        </div>
      </form>
    </div>
  );
}