import React from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../../api/postApi';
import { HistoryCard } from './HistoryCard';
import { History, FileText, AlertCircle } from 'lucide-react';

export const HistoryPage = () => {
  const queryClient = useQueryClient();

  const { data: posts = [], isLoading, isError } = useQuery({
    queryKey: ['posts'],
    queryFn: () => postApi.listPosts(0, 50),
  });

  const deleteMutation = useMutation({
    mutationFn: (id) => postApi.deletePost(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
    }
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <History className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Post History</h1>
            <p className="text-xs text-slate-400">Review, copy, or manage your past generated posts</p>
          </div>
        </div>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="h-48 rounded-2xl bg-slate-900/60 animate-pulse border border-slate-800" />
          ))}
        </div>
      ) : isError ? (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-400 text-sm flex items-center gap-2">
          <AlertCircle className="w-4 h-4" />
          <span>Could not load saved posts. Make sure backend API is running.</span>
        </div>
      ) : posts.length === 0 ? (
        <div className="glass-panel p-12 rounded-2xl border border-slate-800 flex flex-col items-center justify-center text-center">
          <FileText className="w-12 h-12 text-slate-600 mb-3" />
          <h3 className="text-base font-bold text-slate-300">No Saved Posts Yet</h3>
          <p className="text-xs text-slate-400 max-w-sm mt-1">
            Generated posts will automatically appear in your history so you never lose an idea.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {posts.map((post) => (
            <HistoryCard
              key={post.id}
              post={post}
              onDelete={(id) => deleteMutation.mutate(id)}
            />
          ))}
        </div>
      )}
    </div>
  );
};
