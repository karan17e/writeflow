import React, { useState, useEffect } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { postApi } from '../../api/postApi';
import { InputForm } from './InputForm';
import { PostPreview } from './PostPreview';
import { RefinementToolbar } from './RefinementToolbar';
import { QualityPanel } from './QualityPanel';
import { Check, AlertTriangle } from 'lucide-react';

export const GeneratorPage = ({ restoredItem, onClearRestoredItem }) => {
  const queryClient = useQueryClient();

  const [currentPost, setCurrentPost] = useState(null);
  const [lastFormData, setLastFormData] = useState(null);
  const [restoredFormData, setRestoredFormData] = useState(null);
  const [qualityScores, setQualityScores] = useState(null);
  const [copied, setCopied] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [toastType, setToastType] = useState('success');
  const [errorMsg, setErrorMsg] = useState('');

  // Handle restoring a post from history
  useEffect(() => {
    if (restoredItem) {
      setCurrentPost({
        post: restoredItem.post,
        metadata: restoredItem.metadata || {
          word_count: restoredItem.word_count,
          reading_time: restoredItem.reading_time,
          language: restoredItem.language,
          topic: restoredItem.topic,
          post_type: restoredItem.post_type,
          tone: restoredItem.tone,
          selected_structure: restoredItem.post_type
        }
      });

      const restoredForm = {
        topic: restoredItem.topic || '',
        post_type: restoredItem.post_type || 'Story',
        tone: restoredItem.tone || 'Conversational',
        language: restoredItem.language || 'English',
        target_audience: restoredItem.target_audience || '',
        personal_context: restoredItem.personal_context || '',
        key_points: restoredItem.key_points || '',
        length: restoredItem.length || 'Medium',
        writing_style: restoredItem.writing_style || ''
      };

      setLastFormData(restoredForm);
      setRestoredFormData(restoredForm);
      setQualityScores(null);
      setErrorMsg('');
      triggerToast('Post restored from history! (0 AI tokens used)', 'success');

      if (onClearRestoredItem) {
        onClearRestoredItem();
      }
    }
  }, [restoredItem, onClearRestoredItem]);

  // 1. Initial Generation Mutation
  const generateMutation = useMutation({
    mutationFn: (formData) => {
      console.log('1. User input received by frontend:', formData);
      return postApi.generatePost(formData);
    },
    onSuccess: (data, formData) => {
      console.log('7. Final response received by frontend:', data);
      setCurrentPost(data);
      setLastFormData(formData);
      setQualityScores(null);
      setErrorMsg('');
      
      // Invalidate history query so History page is automatically updated
      queryClient.invalidateQueries({ queryKey: ['history'] });

      if (data.metadata?.history_save_error) {
        triggerToast("Post generated successfully, but we couldn't save it to history.", 'warning');
      } else {
        triggerToast('Post generated & saved to history!', 'success');
      }
    },
    onError: (err) => {
      console.error('Generation Error:', err);
      const detail = err.response?.data?.detail || err.message || 'Unable to generate your post. Please check backend connection.';
      setErrorMsg(detail);
      setCurrentPost(null);
    }
  });

  // 2. Refinement Mutation
  const refineMutation = useMutation({
    mutationFn: async ({ actionId, content }) => {
      console.log(`Refining post (${actionId})...`);
      const payload = {
        post: content,
        language: lastFormData?.language || 'English'
      };
      switch (actionId) {
        case 'regenerate':
          if (!lastFormData) throw new Error('No previous form data to regenerate');
          return await postApi.generatePost(lastFormData);
        case 'improve_hook':
          return await postApi.improveHook(payload);
        case 'make_personal':
          return await postApi.humanizePost(payload);
        case 'make_shorter':
          return await postApi.shortenPost(payload);
        case 'remove_buzzwords':
          return await postApi.rewritePost({
            ...payload,
            additional_instructions: 'Strip corporate buzzwords and replace with clear plain speech.'
          });
        default:
          return await postApi.rewritePost(payload);
      }
    },
    onSuccess: (data, { actionId }) => {
      setCurrentPost(data);
      setQualityScores(null);
      setErrorMsg('');

      // Invalidate history query
      queryClient.invalidateQueries({ queryKey: ['history'] });

      const actionLabels = {
        regenerate: 'Post regenerated & saved to history',
        improve_hook: 'Hook improved & saved to history',
        make_personal: 'Post personalized & saved to history',
        make_shorter: 'Post shortened & saved to history',
        remove_buzzwords: 'Buzzwords removed & saved to history'
      };

      if (data.metadata?.history_save_error) {
        triggerToast("Post updated, but could not save new version to history.", 'warning');
      } else {
        triggerToast(actionLabels[actionId] || 'Post updated & saved to history!', 'success');
      }
    },
    onError: (err) => {
      const detail = err.response?.data?.detail || err.message || 'Failed to refine post.';
      setErrorMsg(detail);
    }
  });

  // 3. Quality Analysis Mutation
  const qualityMutation = useMutation({
    mutationFn: (content) => postApi.analyzeQuality({ post: content }),
    onSuccess: (scores) => {
      setQualityScores(scores);
      setErrorMsg('');
      triggerToast('Quality breakdown updated!', 'success');
    },
    onError: (err) => {
      const detail = err.response?.data?.detail || err.message || 'Failed to analyze post quality.';
      setErrorMsg(detail);
    }
  });

  const handleGenerate = (formData) => {
    setErrorMsg('');
    setCurrentPost(null);
    generateMutation.mutate(formData);
  };

  const handleRefine = (actionId) => {
    if (!currentPost?.post && actionId !== 'regenerate') return;
    setErrorMsg('');
    refineMutation.mutate({
      actionId,
      content: currentPost?.post || ''
    });
  };

  const handleAnalyzeQuality = () => {
    if (!currentPost?.post) return;
    setErrorMsg('');
    qualityMutation.mutate(currentPost.post);
  };

  const handleCopy = () => {
    if (!currentPost?.post) return;
    navigator.clipboard.writeText(currentPost.post);
    setCopied(true);
    triggerToast('Post copied to clipboard!', 'success');
    setTimeout(() => setCopied(false), 2500);
  };

  const triggerToast = (msg, type = 'success') => {
    setToastMessage(msg);
    setToastType(type);
    setTimeout(() => setToastMessage(''), 3500);
  };

  const isLoading = generateMutation.isPending || refineMutation.isPending;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div
          className={`fixed bottom-6 right-6 z-50 px-4 py-2.5 rounded-lg shadow-xl border text-xs font-semibold flex items-center gap-2 animate-slide-up ${
            toastType === 'warning'
              ? 'bg-amber-900 text-amber-100 border-amber-700'
              : 'bg-slate-900 text-white border-slate-700'
          }`}
        >
          {toastType === 'warning' ? (
            <AlertTriangle className="w-4 h-4 text-amber-400" />
          ) : (
            <Check className="w-4 h-4 text-emerald-400" />
          )}
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Main 2-Column Responsive Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* LEFT: Post Creation Form (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <InputForm
            onGenerate={handleGenerate}
            isLoading={isLoading}
            restoredFormData={restoredFormData}
          />
        </div>

        {/* RIGHT: Generated Post Preview, Refinements & Quality Panel (7 Cols) */}
        <div className="lg:col-span-7 flex flex-col gap-5">
          <PostPreview
            post={currentPost}
            isLoading={isLoading}
            error={errorMsg}
            copied={copied}
            onCopy={handleCopy}
          />

          {/* Refinement Toolbar */}
          <RefinementToolbar
            onRefine={handleRefine}
            onCopy={handleCopy}
            copied={copied}
            isLoading={isLoading}
            disabled={!currentPost?.post || isLoading}
          />

          {/* Post Quality Analysis Panel */}
          {currentPost?.post && (
            <QualityPanel
              scores={qualityScores}
              isLoading={qualityMutation.isPending}
              onAnalyze={handleAnalyzeQuality}
            />
          )}
        </div>
      </div>
    </div>
  );
};
