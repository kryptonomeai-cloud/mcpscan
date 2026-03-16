"use client";

import { CategoryCount } from "../data/emails";

export default function BarChart({ data }: { data: CategoryCount[] }) {
  const maxCount = data[0]?.count || 1;

  return (
    <div className="space-y-1.5 max-h-[600px] overflow-y-auto pr-2">
      {data.map((item) => (
        <div key={item.category} className="group flex items-center gap-3">
          <span className="text-xs text-zinc-400 w-28 text-right shrink-0 truncate">
            {item.category}
          </span>
          <div className="flex-1 h-6 bg-zinc-800/50 rounded overflow-hidden relative">
            <div
              className="h-full bg-gradient-to-r from-cyan-600 to-cyan-400 rounded transition-all duration-500"
              style={{ width: `${(item.count / maxCount) * 100}%` }}
            />
            <span className="absolute right-2 top-1/2 -translate-y-1/2 text-[11px] text-zinc-300 font-mono">
              {item.count.toLocaleString()}
            </span>
          </div>
          <span className="text-[11px] text-zinc-500 w-12 text-right font-mono">
            {item.percentage.toFixed(1)}%
          </span>
        </div>
      ))}
    </div>
  );
}
