interface Props {
  format: string;
  setFormat: (v: "pdf" | "xlsx" | "txt") => void;
}

export default function FormatSelector({ format, setFormat }: Props) {
  return (
    <div>
      <h3>Output Format</h3>

      <select
        value={format}
        onChange={(e) => setFormat(e.target.value as "pdf" | "xlsx" | "txt")}
      >
        <option value="pdf">PDF</option>
        <option value="xlsx">Excel</option>
        <option value="txt">Text</option>
      </select>
    </div>
  );
}