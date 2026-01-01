// Update to handle both single and multi-customer
import type { StatementRequest, MultiCustomerStatementRequest } from "../types/statement";

// Keep original for backward compatibility
export async function generateStatement(payload: StatementRequest): Promise<Blob> {
  const response = await fetch("http://localhost:8000/api/statements", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Failed to generate statement: ${response.statusText}`);
  }

  return await response.blob();
}

// New function for multiple customers
export async function generateMultiCustomerStatement(payload: MultiCustomerStatementRequest): Promise<Blob> {
  const response = await fetch("http://localhost:8000/api/generate-statement", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Failed to generate multi-customer statement: ${response.statusText}`);
  }

  return await response.blob();
}