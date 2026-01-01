// CustomerItem.tsx
import React from "react";
import type { Customer } from "../types/statement";

interface Props {
  customer: Customer;
  index: number;
  updateCustomer: (index: number, field: keyof Customer, value: string) => void;
}

export default function CustomerItem({ customer, index, updateCustomer }: Props) {
  return (
    <div style={{ 
      marginBottom: "1rem", 
      padding: "1rem",
      border: "1px solid #ddd",
      borderRadius: "8px",
      backgroundColor: "#f9f9f9"
    }}>
      <h4 style={{ marginTop: 0, marginBottom: "1rem", color: "#333" }}>
        Customer {index + 1}
      </h4>
      
      <input
        placeholder="Customer Name"
        value={customer.name}
        onChange={(e) => updateCustomer(index, "name", e.target.value)}
        style={{ marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
      /><br />

      <input
        placeholder="Customer ID"
        value={customer.customer_id}
        onChange={(e) => updateCustomer(index, "customer_id", e.target.value)}
        style={{ marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
      /><br />

      <input
        placeholder="Address"
        value={customer.address}
        onChange={(e) => updateCustomer(index, "address", e.target.value)}
        style={{ marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
      /><br />

      <input
        placeholder="Phone Number"
        value={customer.phone}
        onChange={(e) => updateCustomer(index, "phone", e.target.value)}
        style={{ marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
      /><br />

      <input
        placeholder="Email Address"
        value={customer.email}
        onChange={(e) => updateCustomer(index, "email", e.target.value)}
        style={{ marginBottom: "0.5rem", width: "100%", padding: "0.5rem" }}
      />
    </div>
  );
}