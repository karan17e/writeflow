import React, { useState } from 'react';
import { Badge } from '../../components/Badge';
import { formatDate } from '../../utils/formatters';
import { Copy, Check, Trash2, Calendar, FileText, ExternalLink, RotateCcw } from 'lucide-react';

export const HistoryCard = ({ item, onRestore, onDelete, onOpenDetail }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = (e) => {
    e.stopPropagation();
    if (!item.post) return;
    navigator.clipboard.writeText(item.post);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const postType = item.post_type || 'Story';
  const language = item.language || 'English';
  const topic = item.topic || 'Untitled Post';
  const postContent = item.post || '';
  const wordCount = item.word_count || (postContent ? postContent.split(/\s+/).length : 0);
  const createdAt = item.created_at || new Date().toISOString();

  const getLanguageBadge = (lang) => {
    if (lang === 'Hindi') return <Badge variant="indigo">🇮🇳 Hindi</Badge>;
    if (lang === 'Hinglish') return <Badge variant="amber">🇮🇳 Hinglish</Badge>;
    return <Badge variant="slate">🇬🇧 English</Badge>;
  };

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 flex flex-col justify-between gap-4 shadow-sm hover:shadow-md hover:border-slate-300 transition-all duration-200">
      <div className="flex flex-col gap-2.5">
        {/* Header & Meta Badges */}
        <div className="flex items-center justify-between gap-2">
          <div className="flex items-center gap-1.5 flex-wrap">
            {getLanguageBadge(language)}
            <Badge variant="blue">{postType}</Badge>
            {item.action && item.action !== 'generate' && (
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-slate-100 text-slate-600 border border-slate-200 capitalize">
                {item.action.replace('_', ' ')}
              </span>
            )}
          </div>
          <span className="text-[11px] font-medium text-slate-400 flex items-center gap-1 flex-shrink-0">
            <Calendar className="w-3 h-3 text-slate-400" />
            {formatDate(createdAt)}
          </span>
        </div>

        {/* Topic Title */}
        <h3 className="text-sm font-bold text-slate-900 line-clamp-1 mt-0.5" title={topic}>
          {topic}
        </h3>

        {/* Post Preview Snippet */}
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 text-xs text-slate-700 line-clamp-4 whitespace-pre-wrap leading-relaxed">
          {postContent}
        </div>
      </div>

      {/* Card Action Buttons */}
      <div className="flex items-center justify-between pt-3 border-t border-slate-100 text-xs text-slate-500">
        <span className="flex items-center gap-1 text-[11px] font-medium text-slate-500">
          <FileText className="w-3.5 h-3.5 text-slate-400" />
          {wordCount} words
        </span>

        <div className="flex items-center gap-1.5">
          {/* Open Detail */}
          {onOpenDetail && (
            <button
              type="button"
              onClick={() => onOpenDetail(item)}
              className="px-2.5 py-1.5 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 font-semibold flex items-center gap-1 transition-colors"
              title="Open full post details"
            >
              <ExternalLink className="w-3.5 h-3.5" />
              <span>Open</span>
            </button>
          )}

          {/* Restore to Editor */}
          {onRestore && (
            <button
              type="button"
              onClick={() => onRestore(item)}
              className="px-2.5 py-1.5 rounded-lg bg-blue-50 hover:bg-blue-100 text-[#0a66c2] border border-blue-200/80 font-bold flex items-center gap-1 transition-all shadow-2xs"
              title="Restore this post and its settings into the editor (0 AI tokens)"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Restore</span>
            </button>
          )}

          {/* Copy Post */}
          <button
            type="button"
            onClick={handleCopy}
            className={`px-2.5 py-1.5 rounded-lg font-semibold flex items-center gap-1 transition-all ${
              copied
                ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                : 'bg-slate-100 hover:bg-slate-200 text-slate-700 border border-slate-200'
            }`}
            title="Copy exact post to clipboard"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>

          {/* Delete */}
          {onDelete && (
            <button
              type="button"
              onClick={() => onDelete(item)}
              className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
              title="Delete from history"
            >
              <Trash2 className="w-3.5 h-3.5" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
