export default function StatsCard({
  label,
  value,
  sub,
}: {
  label: string;
  value: string | number;
  sub?: string;
}) {
  return (
    <div className="bg-zinc-900/80 border border-zinc-800 rounded-xl p-5">
      <p className="text-zinc-500 text-xs uppercase tracking-wider mb-1">{label}</p>
      <p className="text-2xl font-semibold text-white">
        {typeof value === "number" ? value.toLocaleString() : value}
      </p>
      {sub && <p className="text-zinc-500 text-xs mt-1">{sub}</p>}
    </div>
  );
}
