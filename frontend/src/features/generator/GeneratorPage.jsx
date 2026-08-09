import React, { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { postApi } from '../../api/postApi';
import { InputForm } from './InputForm';
import { PostPreview } from './PostPreview';
import { RefinementToolbar } from './RefinementToolbar';
import { QualityPanel } from './QualityPanel';
import { Check } from 'lucide-react';

export const GeneratorPage = () => {
  const [currentPost, setCurrentPost] = useState(null);
  const [lastFormData, setLastFormData] = useState(null);
  const [qualityScores, setQualityScores] = useState(null);
  const [copied, setCopied] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

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
      triggerToast('Post generated successfully!');
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
      const actionLabels = {
        regenerate: 'Post regenerated',
        improve_hook: 'Hook improved',
        make_personal: 'Post personalized',
        make_shorter: 'Post shortened',
        remove_buzzwords: 'Buzzwords removed'
      };
      triggerToast(actionLabels[actionId] || 'Post updated!');
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
      triggerToast('Quality breakdown updated!');
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
    triggerToast('Post copied to clipboard!');
    setTimeout(() => setCopied(false), 2500);
  };

  const triggerToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3000);
  };

  const isLoading = generateMutation.isPending || refineMutation.isPending;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 flex flex-col gap-6">
      {/* Toast Notification */}
      {toastMessage && (
        <div className="fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-4 py-2.5 rounded-lg shadow-xl border border-slate-700 text-xs font-semibold flex items-center gap-2 animate-slide-up">
          <Check className="w-4 h-4 text-emerald-400" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Main 2-Column Responsive Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* LEFT: Post Creation Form (5 Cols) */}
        <div className="lg:col-span-5 flex flex-col gap-6">
          <InputForm onGenerate={handleGenerate} isLoading={isLoading} />
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
