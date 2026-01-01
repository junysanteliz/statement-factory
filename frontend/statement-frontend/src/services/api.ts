// services/api.ts
import type { 
  SingleCustomerStatementRequest, 
  MultiCustomerStatementRequest,
  Customer,
  Loan
} from "../types/statement";

// Single customer endpoint
export async function generateSingleStatement(
  payload: SingleCustomerStatementRequest
): Promise<Blob> {
  const response = await fetch("http://localhost:8000/api/statements", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Single statement error: ${response.status} ${errorText}`);
  }

  return await response.blob();
}

// Multi-customer endpoint  
export async function generateMultiCustomerStatement(
  payload: MultiCustomerStatementRequest
): Promise<Blob> {
  const response = await fetch("http://localhost:8000/api/generate-statement", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Multi-customer statement error: ${response.status} ${errorText}`);
  }

  return await response.blob();
}

// Smart function that routes automatically
export async function generateStatement(
  customers: Customer[],
  loans: Loan[],
  billingStart: string,
  billingEnd: string,
  format: "pdf" | "xlsx" | "txt"
): Promise<Blob> {
  if (customers.length === 1) {
    const payload: SingleCustomerStatementRequest = {
      customer: customers[0],
      loans,
      billing_period_start: billingStart,
      billing_period_end: billingEnd,
      statement_format: format
    };
    return generateSingleStatement(payload);
  } else {
    const payload: MultiCustomerStatementRequest = {
      customers,
      loans,
      billing_period_start: billingStart,
      billing_period_end: billingEnd,
      statement_format: format
    };
    return generateMultiCustomerStatement(payload);
  }
}