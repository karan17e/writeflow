import React from 'react';
import { Badge } from '../../components/Badge';
import { formatDate } from '../../utils/formatters';
import { History, Check, X, RotateCcw } from 'lucide-react';

export const VersionHistory = ({
  versions = [],
  currentVersionNum,
  onSelectVersion,
  onClose
}) => {
  return (
    <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex flex-col gap-4 animate-fade-in">
      <div className="flex items-center justify-between pb-2 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <History className="w-4 h-4 text-indigo-400" />
          <h3 className="text-sm font-bold text-slate-100">Version History</h3>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      <div className="flex flex-col gap-3 max-h-[400px] overflow-y-auto pr-1">
        {versions.map((ver) => {
          const isActive = ver.version === currentVersionNum;
          return (
            <div
              key={ver.id || ver.version}
              onClick={() => onSelectVersion(ver)}
              className={`p-3.5 rounded-xl border text-left cursor-pointer transition-all duration-200 flex flex-col gap-2 ${
                isActive
                  ? 'bg-indigo-500/10 border-indigo-500/40 ring-1 ring-indigo-500/30'
                  : 'bg-slate-900/60 hover:bg-slate-800/80 border-slate-800/80'
              }`}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant={isActive ? 'indigo' : 'slate'}>
                    Version #{ver.version}
                  </Badge>
                  <span className="text-xs font-semibold text-slate-300 capitalize">
                    {ver.action.replace('_', ' ')}
                  </span>
                </div>

                {isActive ? (
                  <span className="text-[11px] font-bold text-indigo-400 flex items-center gap-1">
                    <Check className="w-3 h-3" /> Active
                  </span>
                ) : (
                  <span className="text-[11px] text-slate-400 flex items-center gap-1 hover:text-slate-200">
                    <RotateCcw className="w-3 h-3" /> Restore
                  </span>
                )}
              </div>

              <p className="text-xs text-slate-300 line-clamp-2 italic">
                "{ver.content.slice(0, 100)}..."
              </p>

              <div className="flex items-center justify-between text-[11px] text-slate-400">
                <span>{ver.word_count} words</span>
                <span>{formatDate(ver.created_at)}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
