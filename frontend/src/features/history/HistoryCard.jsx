import React, { useState } from 'react';
import { Badge } from '../../components/Badge';
import { formatDate, countWords } from '../../utils/formatters';
import { Copy, Check, Trash2, Calendar, FileText } from 'lucide-react';

export const HistoryCard = ({ post, onDelete }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    if (!post.current_content) return;
    navigator.clipboard.writeText(post.current_content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="glass-card p-5 rounded-2xl border border-slate-800 flex flex-col justify-between gap-4 hover:border-slate-700 transition-all duration-200 shadow-lg">
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Badge variant="indigo">{post.post_type}</Badge>
            <Badge variant="slate">{post.tone}</Badge>
          </div>
          <span className="text-[11px] text-slate-400 flex items-center gap-1">
            <Calendar className="w-3 h-3" />
            {formatDate(post.created_at)}
          </span>
        </div>

        <h3 className="text-sm font-bold text-slate-100 line-clamp-1 mt-1">
          {post.topic}
        </h3>

        <div className="p-3 rounded-xl bg-slate-900/90 border border-slate-800/80 text-xs text-slate-300 line-clamp-4 whitespace-pre-wrap font-sans">
          {post.current_content}
        </div>
      </div>

      <div className="flex items-center justify-between pt-2 border-t border-slate-800/60 text-xs text-slate-400">
        <span className="flex items-center gap-1">
          <FileText className="w-3.5 h-3.5" />
          {post.word_count} words • v{post.latest_version}
        </span>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className={`px-2.5 py-1 rounded-lg font-medium flex items-center gap-1 transition-colors ${
              copied
                ? 'bg-emerald-600/20 text-emerald-400 border border-emerald-500/30'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-300'
            }`}
          >
            {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
            {copied ? 'Copied' : 'Copy'}
          </button>

          <button
            onClick={() => onDelete(post.id)}
            className="p-1.5 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
            title="Delete saved post"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
