import StatsCard from "./components/StatsCard";
import BarChart from "./components/BarChart";
import EmailTable from "./components/EmailTable";
import { TOTAL_EMAILS, getCategoryBreakdown, recentEmails } from "./data/emails";

export default function Home() {
  const categories = getCategoryBreakdown();
  const avgConfidence = Math.round(
    recentEmails.reduce((sum, e) => sum + e.confidence, 0) / recentEmails.length * 100
  );

  return (
    <main className="min-h-screen p-6 md:p-10 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <h1 className="text-2xl font-bold tracking-tight">
            Email Classifier
          </h1>
        </div>
        <p className="text-zinc-500 text-sm">
          AI-powered email classification • {TOTAL_EMAILS.toLocaleString()} emails • 30 categories • All labelled in Gmail
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatsCard label="Total Classified" value={TOTAL_EMAILS} sub="100% coverage" />
        <StatsCard label="Categories" value={30} sub="Fully labelled" />
        <StatsCard label="Avg Confidence" value={`${avgConfidence}%`} sub="Model accuracy" />
        <StatsCard label="Top Category" value={categories[0]?.category || "—"} sub={`${categories[0]?.count.toLocaleString()} emails`} />
      </div>

      {/* Category Breakdown */}
      <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6 mb-8">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <span className="text-cyan-400">▎</span>
          Category Breakdown
        </h2>
        <BarChart data={categories} />
      </div>

      {/* Recent Classifications */}
      <div className="bg-zinc-900/50 border border-zinc-800 rounded-xl p-6">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <span className="text-cyan-400">▎</span>
          Recent Classifications
        </h2>
        <EmailTable emails={recentEmails} />
      </div>

      {/* Footer */}
      <footer className="mt-8 text-center text-zinc-600 text-xs">
        Email Classifier Dashboard • Built with Next.js + Tailwind CSS • Data from Gmail API classification pipeline
      </footer>
    </main>
  );
}
