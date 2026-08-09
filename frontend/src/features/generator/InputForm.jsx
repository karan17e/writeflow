import React, { useState, useEffect } from 'react';
import { POST_TYPES, TONES, LENGTHS } from '../../utils/constants';
import { Button } from '../../components/Button';
import { Textarea } from '../../components/Textarea';
import { Select } from '../../components/Select';
import { Sparkles, PenTool, Check, Trash2, BookOpen, Plus, X, Lightbulb } from 'lucide-react';

const LOCAL_STORAGE_STYLE_KEY = 'postcraft_writing_style';
const LOCAL_STORAGE_SAMPLES_KEY = 'postcraft_writing_samples';

export const InputForm = ({ onGenerate, isLoading }) => {
  const [formData, setFormData] = useState({
    topic: '',
    post_type: 'Story',
    tone: 'Conversational',
    target_audience: '',
    personal_context: '',
    key_points: '',
    length: 'Medium',
    writing_style: '',
  });

  const [writingSamples, setWritingSamples] = useState(['']);
  const [showSamplesSection, setShowSamplesSection] = useState(false);

  const [error, setError] = useState('');
  const [saveFeedback, setSaveFeedback] = useState('');
  const [sampleFeedback, setSampleFeedback] = useState('');

  // Load saved writing style & samples from localStorage on mount
  useEffect(() => {
    try {
      const savedStyle = localStorage.getItem(LOCAL_STORAGE_STYLE_KEY);
      if (savedStyle) {
        setFormData((prev) => ({ ...prev, writing_style: savedStyle }));
      }

      const savedSamples = localStorage.getItem(LOCAL_STORAGE_SAMPLES_KEY);
      if (savedSamples) {
        const parsed = JSON.parse(savedSamples);
        if (Array.isArray(parsed) && parsed.length > 0) {
          setWritingSamples(parsed);
        }
      }
    } catch (e) {
      console.warn('Could not load settings from localStorage', e);
    }
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!formData.topic.trim()) {
      setError('Please enter a topic or main idea for your post.');
      return;
    }
    setError('');

    const validSamples = writingSamples.filter((s) => s.trim().length > 0);

    onGenerate({
      ...formData,
      writing_samples: validSamples
    });
  };

  const handleChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (field === 'topic' && value.trim()) setError('');
  };

  const handleAppendContextHint = (hint) => {
    setFormData((prev) => {
      const existing = prev.personal_context ? prev.personal_context.trim() + '\n' : '';
      return { ...prev, personal_context: existing + hint };
    });
  };

  const handleSaveStyle = () => {
    try {
      localStorage.setItem(LOCAL_STORAGE_STYLE_KEY, formData.writing_style || '');
      setSaveFeedback('Style saved!');
      setTimeout(() => setSaveFeedback(''), 2500);
    } catch (e) {
      console.error('Failed to save style', e);
    }
  };

  const handleClearStyle = () => {
    try {
      localStorage.removeItem(LOCAL_STORAGE_STYLE_KEY);
      setFormData((prev) => ({ ...prev, writing_style: '' }));
      setSaveFeedback('Style cleared');
      setTimeout(() => setSaveFeedback(''), 2500);
    } catch (e) {
      console.error('Failed to clear style', e);
    }
  };

  // Samples Management
  const handleSampleChange = (index, value) => {
    const updated = [...writingSamples];
    updated[index] = value;
    setWritingSamples(updated);
  };

  const handleAddSample = () => {
    if (writingSamples.length < 5) {
      setWritingSamples([...writingSamples, '']);
    }
  };

  const handleRemoveSample = (index) => {
    if (writingSamples.length > 1) {
      const updated = writingSamples.filter((_, i) => i !== index);
      setWritingSamples(updated);
    } else {
      setWritingSamples(['']);
    }
  };

  const handleSaveSamples = () => {
    try {
      const valid = writingSamples.filter((s) => s.trim().length > 0);
      localStorage.setItem(LOCAL_STORAGE_SAMPLES_KEY, JSON.stringify(valid));
      setSampleFeedback('Samples saved!');
      setTimeout(() => setSampleFeedback(''), 2500);
    } catch (e) {
      console.error('Failed to save samples', e);
    }
  };

  const handleClearSamples = () => {
    try {
      localStorage.removeItem(LOCAL_STORAGE_SAMPLES_KEY);
      setWritingSamples(['']);
      setSampleFeedback('Samples cleared');
      setTimeout(() => setSampleFeedback(''), 2500);
    } catch (e) {
      console.error('Failed to clear samples', e);
    }
  };

  const activeSamplesCount = writingSamples.filter((s) => s.trim()).length;

  const contextPrompts = [
    "What specific tasks/project did you work on?",
    "What core Python / technical skills did you gain?",
    "What was your biggest learning or takeaway?",
    "What challenge did you overcome?"
  ];

  return (
    <form onSubmit={handleSubmit} className="saas-card p-6 flex flex-col gap-5">
      <div className="flex items-center gap-2.5 pb-3 border-b border-slate-100">
        <div className="w-8 h-8 rounded-lg bg-blue-50 flex items-center justify-center text-[#0a66c2]">
          <Sparkles className="w-4 h-4" />
        </div>
        <div>
          <h2 className="text-base font-bold text-slate-900">Post Creator</h2>
          <p className="text-xs text-slate-500">Provide a topic to generate a focused, natural post</p>
        </div>
      </div>

      {/* 1. Topic / Idea */}
      <Textarea
        id="topic"
        label="1. Topic / Idea"
        sublabel="Required • Primary Subject"
        placeholder="e.g. 3 months Python internship..."
        rows={3}
        value={formData.topic}
        onChange={(e) => handleChange('topic', e.target.value)}
        error={error}
      />

      {/* 2 & 3. Post Type & Tone Dropdowns */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Select
          id="post_type"
          label="2. Post Type"
          options={POST_TYPES}
          value={formData.post_type}
          onChange={(e) => handleChange('post_type', e.target.value)}
        />
        <Select
          id="tone"
          label="3. Tone"
          options={TONES}
          value={formData.tone}
          onChange={(e) => handleChange('tone', e.target.value)}
        />
      </div>

      {/* 4. Target Audience */}
      <div className="flex flex-col gap-1">
        <label htmlFor="target_audience" className="text-xs font-semibold uppercase tracking-wider text-slate-600">
          4. Target Audience
        </label>
        <input
          type="text"
          id="target_audience"
          placeholder="e.g. Recruiter, Engineers, Tech Community (Frames post style)"
          value={formData.target_audience}
          onChange={(e) => handleChange('target_audience', e.target.value)}
          className="w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#0a66c2]/20 focus:border-[#0a66c2] transition-all shadow-2xs"
        />
      </div>

      {/* Writing Style & Instructions Section */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-slate-700">
            <PenTool className="w-3.5 h-3.5 text-[#0a66c2]" />
            <span>WRITING STYLE & INSTRUCTIONS</span>
          </div>
          {saveFeedback && (
            <span className="text-xs font-semibold text-emerald-600 animate-fade-in">
              {saveFeedback}
            </span>
          )}
        </div>

        <p className="text-[11px] text-slate-500">
          Tell the AI how you want your post written. Example: Use 3 emojis, short sentences, simple English, and no hashtags.
        </p>

        <Textarea
          id="writing_style"
          placeholder="Use 3 emojis, short sentences, simple English, and no hashtags."
          rows={2}
          value={formData.writing_style}
          onChange={(e) => handleChange('writing_style', e.target.value)}
        />

        <div className="flex items-center justify-end gap-2">
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={handleClearStyle}
            disabled={!formData.writing_style}
            icon={Trash2}
          >
            Clear Style
          </Button>

          <Button
            type="button"
            variant="secondary"
            size="sm"
            onClick={handleSaveStyle}
            disabled={!formData.writing_style.trim()}
            icon={Check}
            className="text-[#0a66c2] bg-blue-50 hover:bg-blue-100 border-blue-200"
          >
            Save Style
          </Button>
        </div>
      </div>

      {/* My Writing Samples Section */}
      <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 flex flex-col gap-3">
        <div className="flex items-center justify-between">
          <button
            type="button"
            onClick={() => setShowSamplesSection(!showSamplesSection)}
            className="flex items-center gap-2 text-left"
          >
            <BookOpen className="w-3.5 h-3.5 text-[#0a66c2]" />
            <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
              My Writing Samples {activeSamplesCount > 0 && `(${activeSamplesCount}/5 Saved)`}
            </span>
          </button>

          {sampleFeedback && (
            <span className="text-xs font-semibold text-emerald-600 animate-fade-in">
              {sampleFeedback}
            </span>
          )}
        </div>

        {showSamplesSection && (
          <div className="flex flex-col gap-3 pt-1 animate-fade-in">
            {writingSamples.map((sample, idx) => (
              <div key={idx} className="flex flex-col gap-1">
                <div className="flex items-center justify-between text-[11px] font-semibold text-slate-600">
                  <span>Sample {idx + 1}</span>
                  {writingSamples.length > 1 && (
                    <button
                      type="button"
                      onClick={() => handleRemoveSample(idx)}
                      className="text-slate-400 hover:text-rose-500 transition-colors"
                    >
                      <X className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
                <Textarea
                  placeholder={`Paste writing sample ${idx + 1} here...`}
                  rows={2}
                  value={sample}
                  onChange={(e) => handleSampleChange(idx, e.target.value)}
                />
              </div>
            ))}

            <div className="flex items-center justify-between pt-2 border-t border-slate-200">
              {writingSamples.length < 5 ? (
                <button
                  type="button"
                  onClick={handleAddSample}
                  className="text-xs text-[#0a66c2] hover:text-[#004182] font-semibold flex items-center gap-1"
                >
                  <Plus className="w-3.5 h-3.5" />
                  <span>Add Sample</span>
                </button>
              ) : (
                <span className="text-[11px] text-slate-400">Max 5 samples</span>
              )}

              <div className="flex items-center gap-2">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={handleClearSamples}
                  disabled={activeSamplesCount === 0}
                  icon={Trash2}
                >
                  Clear Samples
                </Button>

                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={handleSaveSamples}
                  disabled={activeSamplesCount === 0}
                  icon={Check}
                  className="text-[#0a66c2] bg-blue-50 hover:bg-blue-100 border-blue-200"
                >
                  Save Samples
                </Button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 5. Personal Experience / Context */}
      <div className="flex flex-col gap-2">
        <Textarea
          id="personal_context"
          label="5. Personal Experience / Context"
          sublabel="Optional • Helps avoid generic writing"
          placeholder="e.g. Worked on async backend APIs, learned FastAPI, built 2 mini projects..."
          rows={2}
          value={formData.personal_context}
          onChange={(e) => handleChange('personal_context', e.target.value)}
        />

        {/* Helpful Context Prompt Chips */}
        <div className="flex flex-col gap-1.5 p-3 rounded-lg bg-blue-50/50 border border-blue-100">
          <div className="flex items-center gap-1.5 text-[11px] font-bold text-[#0a66c2]">
            <Lightbulb className="w-3.5 h-3.5 flex-shrink-0" />
            <span>Want a more specific post? Click to add context:</span>
          </div>
          <div className="flex flex-wrap gap-1.5">
            {contextPrompts.map((promptText, i) => (
              <button
                key={i}
                type="button"
                onClick={() => handleAppendContextHint(promptText + " ")}
                className="text-[11px] text-slate-700 bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-300 px-2.5 py-1 rounded-md transition-colors text-left"
              >
                + {promptText}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 6. Key Points */}
      <Textarea
        id="key_points"
        label="6. Key Points to Include"
        sublabel="Optional"
        placeholder="e.g. Learned OOP principles, focus on clean code..."
        rows={2}
        value={formData.key_points}
        onChange={(e) => handleChange('key_points', e.target.value)}
      />

      {/* 7. Post Length */}
      <div className="flex flex-col gap-1.5">
        <label className="text-xs font-semibold uppercase tracking-wider text-slate-600">
          7. Post Length
        </label>
        <div className="grid grid-cols-3 gap-2">
          {LENGTHS.map((item) => {
            const isSelected = formData.length === item.value;
            return (
              <button
                type="button"
                key={item.value}
                onClick={() => handleChange('length', item.value)}
                className={`py-2 px-3 rounded-lg border text-xs font-semibold transition-all text-center ${
                  isSelected
                    ? 'bg-blue-50 border-[#0a66c2] text-[#0a66c2] shadow-xs'
                    : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                <div>{item.label}</div>
                <div className="text-[10px] font-normal text-slate-400 mt-0.5">{item.desc}</div>
              </button>
            );
          })}
        </div>
      </div>

      {/* 8. Generate Post Button */}
      <Button
        type="submit"
        variant="primary"
        size="lg"
        isLoading={isLoading}
        icon={Sparkles}
        className="w-full mt-2 bg-[#0a66c2] hover:bg-[#004182] text-white"
      >
        Generate Post
      </Button>
    </form>
  );
};
