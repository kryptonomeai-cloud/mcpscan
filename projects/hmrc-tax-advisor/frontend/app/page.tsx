"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

interface Citation {
  section_id: string;
  manual: string;
  title: string;
  url: string;
}

interface Message {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
  confidence?: "HIGH" | "MEDIUM" | "LOW";
  confidence_score?: number;
  elapsed?: number;
}

const confidenceConfig = {
  HIGH: { color: "bg-green-500/20 text-green-400 border-green-500/30", label: "High Confidence" },
  MEDIUM: { color: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30", label: "Medium Confidence" },
  LOW: { color: "bg-red-500/20 text-red-400 border-red-500/30", label: "Low Confidence" },
};

function LoadingDots() {
  return (
    <div className="flex items-center gap-1.5 py-4 px-1">
      <div className="loading-dot w-2 h-2 rounded-full bg-cyan-400" />
      <div className="loading-dot w-2 h-2 rounded-full bg-cyan-400" />
      <div className="loading-dot w-2 h-2 rounded-full bg-cyan-400" />
    </div>
  );
}

function CitationLink({ citation }: { citation: Citation }) {
  return (
    <a
      href={citation.url}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs
        bg-cyan-500/10 text-cyan-400 border border-cyan-500/20
        hover:bg-cyan-500/20 hover:border-cyan-500/40 transition-all"
    >
      <svg className="w-3 h-3 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101" />
        <path strokeLinecap="round" strokeLinejoin="round" d="M10.172 13.828a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
      </svg>
      <span className="font-mono font-medium">{citation.section_id}</span>
      <span className="text-zinc-500 truncate max-w-[200px]">{citation.title}</span>
    </a>
  );
}

function ConfidenceBadge({ level }: { level: "HIGH" | "MEDIUM" | "LOW" }) {
  const config = confidenceConfig[level];
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium border ${config.color}`}>
      <span className="w-1.5 h-1.5 rounded-full bg-current" />
      {config.label}
    </span>
  );
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e?: React.FormEvent) => {
    e?.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/api/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error(`API error: ${res.status}`);

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          citations: data.citations,
          confidence: data.confidence,
          confidence_score: data.confidence_score,
          elapsed: data.elapsed,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, I couldn't process your question. Please check the backend is running and try again.",
          confidence: "LOW",
        },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="flex flex-col h-screen max-w-4xl mx-auto">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-zinc-800/60">
        <div className="flex items-center gap-3">
          <Image
            src="/mindfizz-logo.png"
            alt="MindFizz"
            width={120}
            height={32}
            className="h-7 w-auto"
            priority
          />
          <div className="w-px h-6 bg-zinc-700" />
          <h1 className="text-sm font-medium text-zinc-400">HMRC Tax Advisor</h1>
        </div>
        <span className="text-[10px] text-zinc-600 uppercase tracking-wider">Beta</span>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-6 py-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center gap-4 -mt-16">
            <div className="w-16 h-16 rounded-2xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center">
              <svg className="w-8 h-8 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 006 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 016 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 016-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0018 18a8.967 8.967 0 00-6 2.292m0-14.25v14.25" />
              </svg>
            </div>
            <div>
              <h2 className="text-xl font-semibold text-zinc-200 mb-2">HMRC Tax Advisor</h2>
              <p className="text-sm text-zinc-500 max-w-md">
                Ask questions about UK tax. Answers are sourced from official HMRC manuals
                with direct citations and confidence scoring.
              </p>
            </div>
            <div className="flex flex-wrap justify-center gap-2 mt-4">
              {[
                "Can I claim my laptop as a business expense?",
                "What is the VAT registration threshold?",
                "How does capital gains tax work on property?",
              ].map((q) => (
                <button
                  key={q}
                  onClick={() => {
                    setInput(q);
                    inputRef.current?.focus();
                  }}
                  className="px-3 py-1.5 text-xs text-zinc-400 bg-zinc-800/50 border border-zinc-700/50
                    rounded-lg hover:border-cyan-500/30 hover:text-cyan-400 transition-all"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="space-y-6">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`max-w-[85%] ${msg.role === "user" ? "ml-12" : "mr-12"}`}>
                {msg.role === "user" ? (
                  <div className="bg-cyan-500/15 border border-cyan-500/20 rounded-2xl rounded-tr-sm px-4 py-3">
                    <p className="text-sm text-zinc-100 whitespace-pre-wrap">{msg.content}</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {msg.confidence && (
                      <div className="flex items-center gap-2">
                        <ConfidenceBadge level={msg.confidence} />
                        {msg.elapsed && (
                          <span className="text-[10px] text-zinc-600">{msg.elapsed}s</span>
                        )}
                      </div>
                    )}
                    <div className="bg-zinc-900/80 border border-zinc-800/60 rounded-2xl rounded-tl-sm px-4 py-3">
                      <div className="answer-content text-sm text-zinc-300 whitespace-pre-wrap leading-relaxed">
                        {msg.content}
                      </div>
                    </div>
                    {msg.citations && msg.citations.length > 0 && (
                      <div className="space-y-1.5">
                        <p className="text-[10px] text-zinc-600 uppercase tracking-wider font-medium">Sources</p>
                        <div className="flex flex-wrap gap-1.5">
                          {msg.citations.map((c, j) => (
                            <CitationLink key={j} citation={c} />
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-zinc-900/80 border border-zinc-800/60 rounded-2xl rounded-tl-sm px-4">
                <LoadingDots />
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input */}
      <footer className="px-6 pb-6 pt-2">
        <form onSubmit={handleSubmit} className="relative">
          <textarea
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a UK tax question..."
            rows={1}
            className="w-full resize-none rounded-xl bg-zinc-900/80 border border-zinc-700/50
              px-4 py-3 pr-12 text-sm text-zinc-100 placeholder-zinc-600
              focus:outline-none focus:border-cyan-500/50 focus:ring-1 focus:ring-cyan-500/20
              transition-all"
          />
          <button
            type="submit"
            disabled={!input.trim() || loading}
            className="absolute right-2 top-1/2 -translate-y-1/2 p-2 rounded-lg
              text-zinc-500 hover:text-cyan-400 hover:bg-cyan-500/10
              disabled:opacity-30 disabled:cursor-not-allowed transition-all"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5" />
            </svg>
          </button>
        </form>
        <p className="text-center text-[10px] text-zinc-700 mt-2">
          ⚠ This provides HMRC guidance, not personal tax advice. Consult a qualified tax adviser for your specific situation.
        </p>
      </footer>
    </div>
  );
}
