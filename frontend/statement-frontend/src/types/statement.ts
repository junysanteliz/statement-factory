// types/statement.ts

export interface Customer {
  name: string;
  customer_id: string;
  address: string;
  phone: string;
  email: string;
}

export interface Loan {
  loan_id: string;
  loan_type: string;
  principal: string;
  interest_rate: string;
  term_months: string;
  current_balance: string;
  payment_due_date: string;
  monthly_payment: string;
}

// ✅ SINGLE CUSTOMER REQUEST (for /statements endpoint)
export interface SingleCustomerStatementRequest {
  customer: Customer;  // Required single customer
  loans: Loan[];
  billing_period_start: string;
  billing_period_end: string;
  statement_format: "pdf" | "xlsx" | "txt";
}

// ✅ MULTI-CUSTOMER REQUEST (for /generate-statement endpoint)  
export interface MultiCustomerStatementRequest {
  customers: Customer[];  // Required array of customers
  loans: Loan[];
  billing_period_start: string;
  billing_period_end: string;
  statement_format: "pdf" | "xlsx" | "txt";
}

// Type guard to check if request is single customer
export function isSingleCustomerRequest(
  request: SingleCustomerStatementRequest | MultiCustomerStatementRequest
): request is SingleCustomerStatementRequest {
  return 'customer' in request && !('customers' in request);
}

// Type guard to check if request is multi-customer
export function isMultiCustomerRequest(
  request: SingleCustomerStatementRequest | MultiCustomerStatementRequest
): request is MultiCustomerStatementRequest {
  return 'customers' in request && Array.isArray(request.customers);
}

// Helper to get customers from either request type
export function getCustomersFromRequest(
  request: SingleCustomerStatementRequest | MultiCustomerStatementRequest
): Customer[] {
  if (isSingleCustomerRequest(request)) {
    return [request.customer];
  } else if (isMultiCustomerRequest(request)) {
    return request.customers;
  } else {
    throw new Error("Invalid request type: Must be either single or multi-customer");
  }
}

// Helper to create the appropriate request based on customer count
export function createStatementRequest(
  customers: Customer[],
  loans: Loan[],
  billingStart: string,
  billingEnd: string,
  format: "pdf" | "xlsx" | "txt"
): SingleCustomerStatementRequest | MultiCustomerStatementRequest {
  if (customers.length === 1) {
    return {
      customer: customers[0],
      loans,
      billing_period_start: billingStart,
      billing_period_end: billingEnd,
      statement_format: format
    } as SingleCustomerStatementRequest;
  } else {
    return {
      customers,
      loans,
      billing_period_start: billingStart,
      billing_period_end: billingEnd,
      statement_format: format
    } as MultiCustomerStatementRequest;
  }
}