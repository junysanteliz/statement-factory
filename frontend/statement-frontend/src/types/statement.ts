export interface Customer {
  customer_id: string;
  name: string;
  address: string;
  phone: string;
  email: string;
}

export interface Loan {
  loan_id: string;
  loan_type: string;
  principal: number | string;
  interest_rate: number | string;
  term_months: number | string;
  current_balance: number | string;
  payment_due_date: string;
  monthly_payment: number | string; // NEW
}

export interface StatementRequest {
  customer: Customer;
  billing_period_start: string;
  billing_period_end: string;
  loans: Loan[];
  statement_format: "pdf" | "xlsx" | "txt";
}

// New interface for multiple customers
export interface MultiCustomerStatementRequest {
  customers: Customer[];
  billing_period_start: string;
  billing_period_end: string;
  loans: Loan[];
  statement_format: "pdf" | "xlsx" | "txt";
}