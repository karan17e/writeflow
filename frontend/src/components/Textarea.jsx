import React from 'react';
import clsx from 'clsx';

export const Textarea = ({
  label,
  sublabel,
  error,
  rows = 3,
  className = '',
  id,
  ...props
}) => {
  return (
    <div className="w-full flex flex-col gap-1.5">
      {label && (
        <div className="flex items-center justify-between">
          <label htmlFor={id} className="text-[11px] font-bold uppercase tracking-wider text-slate-600">
            {label}
          </label>
          {sublabel && <span className="text-[11px] text-slate-400 font-normal">{sublabel}</span>}
        </div>
      )}
      <textarea
        id={id}
        rows={rows}
        className={clsx(
          'w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-lg text-slate-900 placeholder-slate-400 text-sm focus:outline-none focus:ring-2 focus:ring-[#0a66c2]/20 focus:border-[#0a66c2] transition-all duration-150 resize-none shadow-2xs',
          error && 'border-rose-500 focus:ring-rose-500/20 focus:border-rose-500',
          className
        )}
        {...props}
      />
      {error && <span className="text-xs text-rose-500 font-medium">{error}</span>}
    </div>
  );
};
