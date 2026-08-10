import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../../api/postApi';
import { HistoryCard } from './HistoryCard';
import { Button } from '../../components/Button';
import { LANGUAGES, POST_TYPES } from '../../utils/constants';
import { formatDate } from '../../utils/formatters';
import {
  History,
  FileText,
  AlertCircle,
  Search,
  Trash2,
  X,
  Check,
  Copy,
  RotateCcw,
  Sparkles,
  Filter
} from 'lucide-react';

export const HistoryPage = ({ onRestorePost, onNavigateToGenerator }) => {
  const queryClient = useQueryClient();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('All');
  const [selectedPostType, setSelectedPostType] = useState('All');

  // Confirmation Modals State
  const [itemToDelete, setItemToDelete] = useState(null);
  const [showClearAllModal, setShowClearAllModal] = useState(false);
  const [detailItem, setDetailItem] = useState(null);

  // Toast feedback
  const [toastMessage, setToastMessage] = useState('');
  const [detailCopied, setDetailCopied] = useState(false);

  const triggerToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3000);
  };

  // Fetch History from API
  const { data: historyItems = [], isLoading, isError } = useQuery({
    queryKey: ['history', searchQuery, selectedLanguage, selectedPostType],
    queryFn: () => postApi.listHistory({
      q: searchQuery || undefined,
      language: selectedLanguage !== 'All' ? selectedLanguage : undefined,
      post_type: selectedPostType !== 'All' ? selectedPostType : undefined,
      limit: 100
    }),
  });

  // Single Delete Mutation
  const deleteMutation = useMutation({
    mutationFn: (id) => postApi.deleteHistoryItem(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
      setItemToDelete(null);
      triggerToast('Post deleted from history');
    },
    onError: (err) => {
      triggerToast(err.response?.data?.detail || 'Failed to delete post');
    }
  });

  // Clear All Mutation
  const clearAllMutation = useMutation({
    mutationFn: () => postApi.clearAllHistory(),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['history'] });
      setShowClearAllModal(false);
      triggerToast('All post history cleared');
    },
    onError: (err) => {
      triggerToast(err.response?.data?.detail || 'Failed to clear history');
    }
  });

  const handleRestore = (item) => {
    if (onRestorePost) {
      onRestorePost(item);
    }
  };

  const handleCopyDetail = (postText) => {
    navigator.clipboard.writeText(postText);
    setDetailCopied(true);
    triggerToast('Post copied to clipboard!');
    setTimeout(() => setDetailCopied(false), 2000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-4 py-2.5 rounded-lg shadow-xl border border-slate-700 text-xs font-semibold flex items-center gap-2 animate-slide-up">
          <Check className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-[#0a66c2]">
            <History className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-slate-900">Post History</h1>
            <p className="text-xs text-slate-500">
              All generated and refined posts are automatically saved here
            </p>
          </div>
        </div>

        {historyItems.length > 0 && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowClearAllModal(true)}
            icon={Trash2}
            className="text-rose-600 border-rose-200 hover:bg-rose-50 self-start sm:self-auto"
          >
            Clear All History
          </Button>
        )}
      </div>

      {/* Search & Filter Toolbar */}
      <div className="p-4 rounded-xl bg-white border border-slate-200 shadow-2xs flex flex-col sm:flex-row items-center justify-between gap-4">
        {/* Search Input */}
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by topic or content..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3.5 py-2 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-[#0a66c2]/20 focus:border-[#0a66c2] transition-all"
          />
        </div>

        {/* Filter Selects */}
        <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
          <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <span>Filters:</span>
          </div>

          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 font-medium focus:outline-none focus:border-[#0a66c2]"
          >
            <option value="All">All Languages</option>
            <option value="English">English</option>
            <option value="Hindi">Hindi</option>
            <option value="Hinglish">Hinglish</option>
          </select>

          <select
            value={selectedPostType}
            onChange={(e) => setSelectedPostType(e.target.value)}
            className="px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-800 font-medium focus:outline-none focus:border-[#0a66c2]"
          >
            <option value="All">All Types</option>
            {POST_TYPES.map((pt) => (
              <option key={pt.value} value={pt.value}>
                {pt.value}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Main Grid View */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div key={i} className="h-56 rounded-2xl bg-slate-100 animate-pulse border border-slate-200" />
          ))}
        </div>
      ) : isError ? (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-medium flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-500 flex-shrink-0" />
          <span>Could not load saved post history. Please ensure the backend server is running.</span>
        </div>
      ) : historyItems.length === 0 ? (
        <div className="saas-card p-12 flex flex-col items-center justify-center text-center">
          <div className="w-12 h-12 rounded-full bg-blue-50 flex items-center justify-center text-[#0a66c2] mb-3 border border-blue-100">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="text-base font-bold text-slate-900">No Posts Yet</h3>
          <p className="text-xs text-slate-500 max-w-sm mt-1 mb-4">
            Your generated and refined LinkedIn posts will automatically appear here.
          </p>
          <Button
            variant="primary"
            size="sm"
            onClick={onNavigateToGenerator}
            icon={Sparkles}
            className="bg-[#0a66c2] hover:bg-[#004182]"
          >
            Generate Your First Post
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {historyItems.map((item) => (
            <HistoryCard
              key={item.id}
              item={item}
              onRestore={handleRestore}
              onDelete={(target) => setItemToDelete(target)}
              onOpenDetail={(target) => setDetailItem(target)}
            />
          ))}
        </div>
      )}

      {/* MODAL 1: Individual Item Delete Confirmation */}
      {itemToDelete && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full border border-slate-200 shadow-2xl flex flex-col gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center border border-rose-100">
                <Trash2 className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">Delete Post?</h3>
                <p className="text-xs text-slate-500">This action cannot be undone.</p>
              </div>
            </div>

            <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-700 font-medium line-clamp-2">
              "{itemToDelete.topic}"
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setItemToDelete(null)}
                disabled={deleteMutation.isPending}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={() => deleteMutation.mutate(itemToDelete.id)}
                isLoading={deleteMutation.isPending}
                className="bg-rose-600 hover:bg-rose-700 text-white border-rose-700"
              >
                Delete
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL 2: Clear All History Confirmation */}
      {showClearAllModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 max-w-md w-full border border-slate-200 shadow-2xl flex flex-col gap-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center border border-rose-100">
                <AlertCircle className="w-5 h-5" />
              </div>
              <div>
                <h3 className="text-base font-bold text-slate-900">Clear All Post History?</h3>
                <p className="text-xs text-slate-500">
                  Are you sure you want to delete all post history? This action cannot be undone.
                </p>
              </div>
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowClearAllModal(false)}
                disabled={clearAllMutation.isPending}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                onClick={() => clearAllMutation.mutate()}
                isLoading={clearAllMutation.isPending}
                className="bg-rose-600 hover:bg-rose-700 text-white border-rose-700"
              >
                Clear History
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* MODAL 3: Open Post Detail */}
      {detailItem && (
        <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-white rounded-2xl p-6 max-w-2xl w-full max-h-[85vh] flex flex-col gap-4 border border-slate-200 shadow-2xl overflow-hidden">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100">
              <div>
                <h3 className="text-base font-bold text-slate-900">{detailItem.topic}</h3>
                <p className="text-xs text-slate-500">
                  {detailItem.language} • {detailItem.post_type} • {formatDate(detailItem.created_at)}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setDetailItem(null)}
                className="p-1 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-800 whitespace-pre-wrap leading-relaxed font-sans">
              {detailItem.post}
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-slate-100">
              <span className="text-xs text-slate-500">
                {detailItem.word_count || detailItem.post.split(/\s+/).length} words
              </span>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCopyDetail(detailItem.post)}
                  icon={detailCopied ? Check : Copy}
                >
                  {detailCopied ? 'Copied!' : 'Copy Post'}
                </Button>

                <Button
                  variant="primary"
                  size="sm"
                  onClick={() => {
                    setDetailItem(null);
                    handleRestore(detailItem);
                  }}
                  icon={RotateCcw}
                  className="bg-[#0a66c2] hover:bg-[#004182] text-white"
                >
                  Restore to Editor
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
