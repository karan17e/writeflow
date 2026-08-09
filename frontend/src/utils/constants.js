export const POST_TYPES = [
  { value: 'Achievement', label: '🏆 Achievement' },
  { value: 'Project', label: '🚀 Project' },
  { value: 'Learning', label: '💡 Learning' },
  { value: 'Career', label: '📈 Career' },
  { value: 'Opinion', label: '💬 Opinion' },
  { value: 'Story', label: '📖 Story' },
  { value: 'Educational', label: '📚 Educational' },
  { value: 'Personal Experience', label: '🤝 Personal Experience' },
];

export const TONES = [
  { value: 'Professional', label: '💼 Professional' },
  { value: 'Conversational', label: '☕ Conversational' },
  { value: 'Casual', label: '😊 Casual' },
  { value: 'Confident', label: '⚡ Confident' },
  { value: 'Thoughtful', label: '🧠 Thoughtful' },
  { value: 'Storytelling', label: '🎭 Storytelling' },
];

export const LENGTHS = [
  { value: 'Short', label: 'Short', desc: '~50-80 words' },
  { value: 'Medium', label: 'Medium', desc: '~80-150 words' },
  { value: 'Long', label: 'Long', desc: '~150-250 words' },
];

export const LANGUAGES = [
  { value: 'English', label: '🇬🇧 English' },
  { value: 'Hindi', label: '🇮🇳 Hindi' },
  { value: 'Hinglish', label: '🇮🇳 Hinglish' },
];

export const REFINEMENT_ACTIONS = [
  { id: 'regenerate', label: 'Regenerate', icon: 'RefreshCw', color: 'bg-slate-100 text-slate-700 hover:bg-slate-200 border-slate-300' },
  { id: 'improve_hook', label: 'Improve Hook', icon: 'Sparkles', color: 'bg-blue-50 text-blue-700 hover:bg-blue-100 border-blue-200' },
  { id: 'make_personal', label: 'Make More Personal', icon: 'UserCheck', color: 'bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border-indigo-200' },
  { id: 'make_shorter', label: 'Make Shorter', icon: 'Scissors', color: 'bg-amber-50 text-amber-700 hover:bg-amber-100 border-amber-200' },
  { id: 'remove_buzzwords', label: 'Remove Buzzwords', icon: 'Zap', color: 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100 border-emerald-200' },
];
