import React from "react";
import type { Customer } from "../types/statement";

interface Props {
  customer: Customer;
  setCustomer: (c: Customer) => void;
}

export default function CustomerInfoForm({
  customer,
  setCustomer
}: Props) {
  return (
    <div>
      <h3>Customer Info</h3>

      <input
        placeholder="Customer Name"
        value={customer.name}
        onChange={(e) => setCustomer({ ...customer, name: e.target.value })}
      /><br />

      <input
        placeholder="Customer ID"
        value={customer.customer_id}
        onChange={(e) => setCustomer({ ...customer, customer_id: e.target.value })}
      /><br />

      <input
        placeholder="Address"
        value={customer.address}
        onChange={(e) => setCustomer({ ...customer, address: e.target.value })}
      /><br />

      <input
        placeholder="Phone Number"
        value={customer.phone}
        onChange={(e) => setCustomer({ ...customer, phone: e.target.value })}
      /><br />

      <input
        placeholder="Email Address"
        value={customer.email}
        onChange={(e) => setCustomer({ ...customer, email: e.target.value })}
      /><br />
    </div>
  );
}