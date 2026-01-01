// CustomerList.tsx
import React from "react";
import type { Customer } from "../types/statement";
import CustomerItem from "./CustomerItem";

interface Props {
  customers: Customer[];
  setCustomers: (customers: Customer[]) => void;
}

export default function CustomerList({ customers, setCustomers }: Props) {
  const updateCustomer = (index: number, field: keyof Customer, value: string) => {
    const updated = [...customers];
    updated[index][field] = value;
    setCustomers(updated);
  };

  const addCustomer = () => {
    setCustomers([
      ...customers,
      {
        name: "",
        customer_id: "",
        address: "",
        phone: "",
        email: ""
      }
    ]);
  };

  const removeCustomer = (index: number) => {
    if (customers.length <= 1) {
      alert("At least one customer is required");
      return;
    }
    const updated = customers.filter((_, i) => i !== index);
    setCustomers(updated);
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "1rem" }}>
        <h3 style={{ margin: 0 }}>Customer Information</h3>
        <button 
          type="button" 
          onClick={addCustomer}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: "#4CAF50",
            color: "white",
            border: "none",
            borderRadius: "4px",
            cursor: "pointer"
          }}
        >
          + Add Customer
        </button>
      </div>

      {customers.map((customer, index) => (
        <div key={index} style={{ position: "relative" }}>
          <CustomerItem
            customer={customer}
            index={index}
            updateCustomer={updateCustomer}
          />
          {customers.length > 1 && (
            <button
              type="button"
              onClick={() => removeCustomer(index)}
              style={{
                position: "absolute",
                top: "1rem",
                right: "1rem",
                backgroundColor: "#ff4444",
                color: "white",
                border: "none",
                borderRadius: "4px",
                padding: "0.25rem 0.5rem",
                cursor: "pointer",
                fontSize: "0.8rem"
              }}
            >
              Remove
            </button>
          )}
        </div>
      ))}
    </div>
  );
}