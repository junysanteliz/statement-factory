interface Props {
  billingStart: string;
  billingEnd: string;
  setBillingStart: (v: string) => void;
  setBillingEnd: (v: string) => void;
}

export default function BillingPeriodForm({
  billingStart,
  billingEnd,
  setBillingStart,
  setBillingEnd
}: Props) {
  return (
    <div>
      <h3>Billing Period</h3>

      <input
        type="date"
        value={billingStart}
        onChange={(e) => setBillingStart(e.target.value)}
      />

      <input
        type="date"
        value={billingEnd}
        onChange={(e) => setBillingEnd(e.target.value)}
      />
    </div>
  );
}