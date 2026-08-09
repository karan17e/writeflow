import React from 'react';
import { Badge } from '../../components/Badge';
import { countWords, estimateReadingTime } from '../../utils/formatters';
import { Copy, Check, ThumbsUp, MessageSquare, Repeat2, Send, FileText, AlertCircle, Globe } from 'lucide-react';

export const PostPreview = ({
  post,
  isLoading,
  error,
  copied,
  onCopy,
}) => {
  const content = post?.post || '';
  const wordCount = post?.metadata?.word_count || countWords(content);
  const readingTime = estimateReadingTime(wordCount);
  const postType = post?.metadata?.post_type || 'Draft';

  // Empty state
  if (!isLoading && !error && !content) {
    return (
      <div className="saas-card p-10 flex flex-col items-center justify-center text-center min-h-[440px]">
        <div className="w-14 h-14 rounded-2xl bg-blue-50 border border-blue-100 flex items-center justify-center text-[#0a66c2] mb-4">
          <FileText className="w-7 h-7" />
        </div>
        <h3 className="text-base font-bold text-slate-900 mb-1">Your Post Preview</h3>
        <p className="text-xs text-slate-500 max-w-sm leading-relaxed">
          Fill out the topic and preferences on the left and click <span className="font-semibold text-slate-700">"Generate Post"</span> to build your post.
        </p>
      </div>
    );
  }

  // Loading state (Skeleton Loader)
  if (isLoading) {
    return (
      <div className="saas-card-focus p-6 flex flex-col gap-4 animate-pulse min-h-[440px]">
        <div className="flex items-center justify-between pb-3.5 border-b border-slate-100">
          <div className="h-5 w-36 bg-slate-200 rounded-md" />
          <div className="h-5 w-24 bg-slate-200 rounded-md" />
        </div>

        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-full bg-slate-200 flex-shrink-0" />
          <div className="flex flex-col gap-1.5 flex-1">
            <div className="h-4 w-32 bg-slate-200 rounded" />
            <div className="h-3 w-48 bg-slate-200 rounded" />
          </div>
        </div>

        <div className="flex flex-col gap-2.5 py-4">
          <div className="h-4 w-full bg-slate-200 rounded" />
          <div className="h-4 w-11/12 bg-slate-200 rounded" />
          <div className="h-4 w-4/5 bg-slate-200 rounded" />
          <div className="h-4 w-full bg-slate-200 rounded" />
          <div className="h-4 w-3/4 bg-slate-200 rounded" />
        </div>

        <div className="mt-auto pt-3 border-t border-slate-100 flex items-center justify-between">
          <div className="h-6 w-16 bg-slate-200 rounded" />
          <div className="h-6 w-16 bg-slate-200 rounded" />
          <div className="h-6 w-16 bg-slate-200 rounded" />
          <div className="h-6 w-16 bg-slate-200 rounded" />
        </div>
      </div>
    );
  }

  // Error state
  if (error) {
    return (
      <div className="saas-card border-rose-200 p-8 flex flex-col items-center justify-center text-center min-h-[440px]">
        <div className="w-12 h-12 rounded-full bg-rose-50 border border-rose-100 flex items-center justify-center text-rose-500 mb-3">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h3 className="text-base font-bold text-slate-900 mb-1">Generation Request Error</h3>
        <p className="text-xs text-rose-600 max-w-md leading-relaxed">{error}</p>
      </div>
    );
  }

  return (
    <div className="saas-card-focus overflow-hidden flex flex-col transition-all">
      {/* Header bar */}
      <div className="px-5 py-3.5 bg-slate-50/80 border-b border-slate-200/80 flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-[#0a66c2]" />
          <h3 className="text-sm font-bold text-slate-900">Your Generated Post</h3>
          <Badge variant="blue">{postType}</Badge>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-xs text-slate-500 font-medium hidden sm:flex items-center gap-1.5">
            <span>{wordCount} words</span>
            <span>•</span>
            <span>{readingTime}</span>
          </div>

          <button
            onClick={onCopy}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all shadow-xs ${
              copied
                ? 'bg-emerald-600 text-white shadow-emerald-600/20'
                : 'bg-[#0a66c2] hover:bg-[#004182] text-white shadow-blue-600/20'
            }`}
          >
            {copied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied!' : 'Copy Post'}</span>
          </button>
        </div>
      </div>

      {/* Mock LinkedIn Post Card Body */}
      <div className="p-6 bg-white flex-1 flex flex-col gap-4">
        {/* Author Header */}
        <div className="flex items-center gap-3">
          <div className="w-11 h-11 rounded-full bg-[#0a66c2] text-white flex items-center justify-center font-bold text-sm shadow-xs flex-shrink-0">
            YOU
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-1.5">
              <h4 className="text-sm font-bold text-slate-900 truncate">Your Name</h4>
              <span className="text-xs text-slate-400 font-normal flex-shrink-0">• 1st</span>
            </div>
            <p className="text-xs text-slate-500 truncate">Founder & Builder • Creating products that matter</p>
            <p className="text-[11px] text-slate-400 flex items-center gap-1 mt-0.5">
              <span>Just now</span> • <Globe className="w-3 h-3 text-slate-400 inline" />
            </p>
          </div>
        </div>

        {/* Post Text Content (Visual Focal Point) */}
        <div className="text-sm sm:text-base text-slate-900 leading-relaxed whitespace-pre-wrap font-sans py-2 selection:bg-blue-100 selection:text-[#0a66c2] break-words">
          {content}
        </div>

        {/* Mock LinkedIn Reaction Bar */}
        <div className="mt-auto pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500 font-semibold">
          <button className="flex items-center gap-1.5 hover:text-[#0a66c2] transition-colors py-1.5 px-2.5 rounded-md hover:bg-slate-50">
            <ThumbsUp className="w-4 h-4" />
            <span className="hidden sm:inline">Like</span>
          </button>
          <button className="flex items-center gap-1.5 hover:text-[#0a66c2] transition-colors py-1.5 px-2.5 rounded-md hover:bg-slate-50">
            <MessageSquare className="w-4 h-4" />
            <span className="hidden sm:inline">Comment</span>
          </button>
          <button className="flex items-center gap-1.5 hover:text-[#0a66c2] transition-colors py-1.5 px-2.5 rounded-md hover:bg-slate-50">
            <Repeat2 className="w-4 h-4" />
            <span className="hidden sm:inline">Repost</span>
          </button>
          <button className="flex items-center gap-1.5 hover:text-[#0a66c2] transition-colors py-1.5 px-2.5 rounded-md hover:bg-slate-50">
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Send</span>
          </button>
        </div>
      </div>
    </div>
  );
};
