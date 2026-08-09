import React from 'react';
import { BarChart3, CheckCircle2 } from 'lucide-react';

export const QualityPanel = ({ scores, isLoading, onAnalyze }) => {
  if (!scores && !isLoading) {
    return (
      <div className="saas-card p-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-[#0a66c2]" />
          <div>
            <h4 className="text-xs font-bold text-slate-900">Post Quality Analysis</h4>
            <p className="text-[11px] text-slate-500">Analyze hook strength, readability, and voice clarity</p>
          </div>
        </div>

        <button
          onClick={onAnalyze}
          className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-blue-50 text-[#0a66c2] hover:bg-blue-100 border border-blue-200 transition-colors shadow-2xs"
        >
          Analyze Quality
        </button>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="saas-card p-5 flex flex-col gap-3 animate-pulse">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100">
          <div className="h-4 w-32 bg-slate-200 rounded" />
          <div className="h-4 w-12 bg-slate-200 rounded" />
        </div>
        <div className="grid grid-cols-2 gap-3 py-2">
          <div className="h-3 w-full bg-slate-200 rounded" />
          <div className="h-3 w-full bg-slate-200 rounded" />
          <div className="h-3 w-full bg-slate-200 rounded" />
          <div className="h-3 w-full bg-slate-200 rounded" />
        </div>
      </div>
    );
  }

  const metrics = [
    { key: 'hook_strength', label: 'Hook Strength', score: scores.hook_strength || 8 },
    { key: 'clarity', label: 'Clarity & Flow', score: scores.clarity || 9 },
    { key: 'specificity', label: 'Specificity', score: scores.specificity || 7 },
    { key: 'readability', label: 'Readability', score: scores.readability || 9 },
    { key: 'personal_voice', label: 'Personal Voice', score: scores.personal_voice || 8 },
    { key: 'generic_language', label: 'Generic Filler (Lower = Better)', score: 10 - (scores.generic_language || 2) },
    { key: 'buzzword_usage', label: 'Buzzwords (Lower = Better)', score: 10 - (scores.buzzword_usage || 1) },
    { key: 'repetition', label: 'Sentence Monotony (Lower = Better)', score: 10 - (scores.repetition || 2) },
  ];

  const overallScore = scores.overall_score || 8;

  return (
    <div className="saas-card p-5 flex flex-col gap-4 animate-fade-in">
      {/* Header with Overall Score */}
      <div className="flex items-center justify-between pb-3 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-blue-50 flex items-center justify-center text-[#0a66c2]">
            <BarChart3 className="w-4 h-4" />
          </div>
          <div>
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-800">
              Post Quality Breakdown
            </h4>
            <p className="text-[11px] text-slate-500">Structure, clarity & tone analysis</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <div className="text-right">
            <span className="text-lg font-black text-[#0a66c2]">{overallScore}</span>
            <span className="text-xs font-bold text-slate-400">/10</span>
          </div>
          <button
            onClick={onAnalyze}
            className="text-[11px] text-[#0a66c2] hover:underline font-semibold"
          >
            Re-analyze
          </button>
        </div>
      </div>

      {/* Metric Progress Bars Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-3">
        {metrics.map((item) => {
          const percentage = Math.min(100, Math.max(10, item.score * 10));
          return (
            <div key={item.key} className="flex flex-col gap-1">
              <div className="flex items-center justify-between text-xs font-medium text-slate-700">
                <span>{item.label}</span>
                <span className="font-bold text-slate-900">{item.score}/10</span>
              </div>
              <div className="w-full h-1.5 bg-slate-100 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${
                    item.score >= 8
                      ? 'bg-emerald-500'
                      : item.score >= 6
                      ? 'bg-[#0a66c2]'
                      : 'bg-amber-500'
                  }`}
                  style={{ width: `${percentage}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>

      {/* Suggestions List */}
      {scores.suggestions && scores.suggestions.length > 0 && (
        <div className="pt-3 border-t border-slate-100 flex flex-col gap-1.5">
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
            Actionable Suggestions
          </span>
          <div className="flex flex-col gap-1">
            {scores.suggestions.map((sug, i) => (
              <div key={i} className="flex items-start gap-1.5 text-xs text-slate-700">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 flex-shrink-0 mt-0.5" />
                <span>{sug}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
