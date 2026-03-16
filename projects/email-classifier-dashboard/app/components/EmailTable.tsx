"use client";

import { useState, useMemo } from "react";
import { Email, getCategoryBreakdown } from "../data/emails";

function Badge({ category }: { category: string }) {
  return (
    <span className="inline-block px-2 py-0.5 text-[11px] font-medium rounded-full bg-cyan-900/40 text-cyan-300 border border-cyan-800/50">
      {category}
    </span>
  );
}

function ConfidenceBar({ value }: { value: number }) {
  const pct = Math.round(value * 100);
  const color = pct >= 90 ? "bg-emerald-500" : pct >= 80 ? "bg-cyan-500" : "bg-amber-500";
  return (
    <div className="flex items-center gap-2">
      <div className="w-16 h-1.5 bg-zinc-800 rounded-full overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${pct}%` }} />
      </div>
      <span className="text-[11px] text-zinc-400 font-mono">{pct}%</span>
    </div>
  );
}

export default function EmailTable({ emails }: { emails: Email[] }) {
  const [filter, setFilter] = useState("");
  const [search, setSearch] = useState("");
  const categories = getCategoryBreakdown();

  const filtered = useMemo(() => {
    let result = emails;
    if (filter) result = result.filter((e) => e.category === filter);
    if (search) {
      const q = search.toLowerCase();
      result = result.filter(
        (e) =>
          e.subject.toLowerCase().includes(q) ||
          e.from.toLowerCase().includes(q)
      );
    }
    return result.slice(0, 50);
  }, [emails, filter, search]);

  return (
    <div>
      <div className="flex flex-col sm:flex-row gap-3 mb-4">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-300 focus:outline-none focus:border-cyan-600"
        >
          <option value="">All Categories</option>
          {categories.map((c) => (
            <option key={c.category} value={c.category}>
              {c.category} ({c.count.toLocaleString()})
            </option>
          ))}
        </select>
        <input
          type="text"
          placeholder="Search subject or sender..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg px-3 py-2 text-sm text-zinc-300 placeholder-zinc-600 focus:outline-none focus:border-cyan-600"
        />
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-zinc-800">
              <th className="text-left text-zinc-500 text-xs uppercase tracking-wider py-2 px-3">Date</th>
              <th className="text-left text-zinc-500 text-xs uppercase tracking-wider py-2 px-3">Subject</th>
              <th className="text-left text-zinc-500 text-xs uppercase tracking-wider py-2 px-3">From</th>
              <th className="text-left text-zinc-500 text-xs uppercase tracking-wider py-2 px-3">Category</th>
              <th className="text-left text-zinc-500 text-xs uppercase tracking-wider py-2 px-3">Confidence</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((email) => (
              <tr
                key={email.id}
                className="border-b border-zinc-800/50 hover:bg-zinc-800/30 transition-colors"
              >
                <td className="py-2.5 px-3 text-zinc-400 text-xs font-mono whitespace-nowrap">
                  {new Date(email.date).toLocaleDateString("en-GB", {
                    day: "2-digit",
                    month: "short",
                    year: "numeric",
                  })}
                </td>
                <td className="py-2.5 px-3 text-zinc-200 max-w-xs truncate">{email.subject}</td>
                <td className="py-2.5 px-3 text-zinc-400 text-xs max-w-[200px] truncate">{email.from}</td>
                <td className="py-2.5 px-3">
                  <Badge category={email.category} />
                </td>
                <td className="py-2.5 px-3">
                  <ConfidenceBar value={email.confidence} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="text-xs text-zinc-600 mt-3">
        Showing {filtered.length} of {emails.length} emails
        {filter && ` in "${filter}"`}
      </p>
    </div>
  );
}
