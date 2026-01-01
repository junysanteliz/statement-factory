import type { StatementRequest } from "../types/statement";

const API_URL = "http://localhost:8000/api";

export async function generateStatement(data: StatementRequest) {
  const res = await fetch(`${API_URL}/statements`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  const blob = await res.blob();
  return blob;
}