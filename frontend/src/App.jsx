import React, { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { GeneratorPage } from './features/generator/GeneratorPage';
import { HistoryPage } from './features/history/HistoryPage';
import { Sparkles, History } from 'lucide-react';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export default function App() {
  const [activeTab, setActiveTab] = useState('generator');
  const [restoredItem, setRestoredItem] = useState(null);

  const handleRestorePost = (item) => {
    setRestoredItem(item);
    setActiveTab('generator');
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900 selection:bg-[#0a66c2] selection:text-white">
        {/* Navigation Header */}
        <header className="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/80 px-4 sm:px-8 py-3 flex items-center justify-between shadow-2xs">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-[#0a66c2] flex items-center justify-center text-white shadow-xs">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <span className="font-extrabold text-base tracking-tight text-slate-900">WriteFlow</span>
              <span className="ml-2 text-[10px] font-bold uppercase tracking-wider text-[#0a66c2] bg-blue-50 px-2 py-0.5 rounded-full border border-blue-200">
                Smart Post Creator
              </span>
            </div>
          </div>

          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg border border-slate-200">
            <button
              onClick={() => setActiveTab('generator')}
              className={`px-3.5 py-1.5 rounded-md text-xs font-bold flex items-center gap-1.5 transition-all ${
                activeTab === 'generator'
                  ? 'bg-white text-[#0a66c2] shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>Generator</span>
            </button>

            <button
              onClick={() => setActiveTab('history')}
              className={`px-3.5 py-1.5 rounded-md text-xs font-bold flex items-center gap-1.5 transition-all ${
                activeTab === 'history'
                  ? 'bg-white text-[#0a66c2] shadow-xs'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <History className="w-3.5 h-3.5" />
              <span>History</span>
            </button>
          </nav>
        </header>

        {/* Main Content Area */}
        <main className="flex-1">
          {activeTab === 'generator' ? (
            <GeneratorPage
              restoredItem={restoredItem}
              onClearRestoredItem={() => setRestoredItem(null)}
            />
          ) : (
            <HistoryPage
              onRestorePost={handleRestorePost}
              onNavigateToGenerator={() => setActiveTab('generator')}
            />
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-200 bg-white py-4 text-center text-xs text-slate-500">
          <p>WriteFlow — Write naturally. Post confidently.</p>
        </footer>
      </div>
    </QueryClientProvider>
  );
}
