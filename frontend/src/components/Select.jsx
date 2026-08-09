import React from 'react';
import clsx from 'clsx';

export const Select = ({
  label,
  options = [],
  className = '',
  id,
  ...props
}) => {
  return (
    <div className="w-full flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-[11px] font-bold uppercase tracking-wider text-slate-600">
          {label}
        </label>
      )}
      <select
        id={id}
        className={clsx(
          'w-full px-3.5 py-2.5 bg-white border border-slate-200 rounded-lg text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-[#0a66c2]/20 focus:border-[#0a66c2] transition-all duration-150 cursor-pointer shadow-2xs',
          className
        )}
        {...props}
      >
        {options.map((opt) => (
          <option key={opt.value} value={opt.value} className="bg-white text-slate-900">
            {opt.label}
          </option>
        ))}
      </select>
    </div>
  );
};
