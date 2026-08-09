import React from 'react';
import {
  RefreshCw,
  Sparkles,
  UserCheck,
  Scissors,
  Zap,
  Copy,
  Check
} from 'lucide-react';

export const RefinementToolbar = ({
  onRefine,
  onCopy,
  copied,
  isLoading,
  disabled
}) => {
  const actionButtons = [
    { id: 'regenerate', label: 'Regenerate', icon: RefreshCw, color: 'hover:bg-slate-100 text-slate-700 border-slate-200' },
    { id: 'improve_hook', label: 'Improve Hook', icon: Sparkles, color: 'hover:bg-blue-50 text-[#0a66c2] border-blue-200' },
    { id: 'make_personal', label: 'Make More Personal', icon: UserCheck, color: 'hover:bg-indigo-50 text-indigo-700 border-indigo-200' },
    { id: 'make_shorter', label: 'Make Shorter', icon: Scissors, color: 'hover:bg-amber-50 text-amber-700 border-amber-200' },
    { id: 'remove_buzzwords', label: 'Remove Buzzwords', icon: Zap, color: 'hover:bg-emerald-50 text-emerald-700 border-emerald-200' },
  ];

  return (
    <div className="saas-card p-4 flex flex-col gap-3">
      <div className="flex items-center justify-between">
        <h4 className="text-[11px] font-bold uppercase tracking-wider text-slate-500">
          Refine & Edit Post
        </h4>

        {/* Copy Button */}
        <button
          onClick={onCopy}
          disabled={disabled}
          className={`px-3 py-1 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all border ${
            copied
              ? 'bg-emerald-50 text-emerald-700 border-emerald-300'
              : 'bg-blue-50 text-[#0a66c2] border-blue-200 hover:bg-blue-100'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : 'active:scale-98'}`}
        >
          {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
          <span>{copied ? 'Copied to Clipboard!' : 'Copy Post'}</span>
        </button>
      </div>

      {/* Refinement Action Buttons Row */}
      <div className="flex flex-wrap items-center gap-2">
        {actionButtons.map((btn) => {
          const Icon = btn.icon;
          return (
            <button
              key={btn.id}
              disabled={disabled || isLoading}
              onClick={() => onRefine(btn.id)}
              className={`px-3 py-2 rounded-lg border text-xs font-semibold bg-white flex items-center gap-1.5 transition-all ${btn.color} ${
                disabled || isLoading ? 'opacity-50 cursor-not-allowed' : 'active:scale-98 shadow-2xs'
              }`}
            >
              <Icon className="w-3.5 h-3.5 flex-shrink-0" />
              <span>{btn.label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
