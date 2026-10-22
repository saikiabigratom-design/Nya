"use client";

import React from "react";

interface BrandMarkProps {
  size?: "sm" | "md" | "lg" | "xl";
  className?: string;
  showText?: boolean;
}

export const BrandMark: React.FC<BrandMarkProps> = ({
  size = "md",
  className = "",
  showText = false,
}) => {
  const sizeClasses = {
    sm: "w-8 h-8 text-xl",
    md: "w-12 h-12 text-2xl",
    lg: "w-20 h-20 text-4xl",
    xl: "w-28 h-28 text-6xl",
  };

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      <div
        role="img"
        aria-label="Nya — Vocal for Local brand mark"
        className={`inline-flex items-center justify-center rounded-2xl bg-slate-900 dark:bg-nya-indigo border border-teal-500/40 dark:border-nya-teal/30 shadow-lg select-none transition-transform hover:scale-105 ${sizeClasses[size]}`}
        style={{
          boxShadow: "0 0 20px rgba(92, 225, 208, 0.2)",
        }}
      >
        <span
          className="font-bold text-[#5CE1D0] transform -translate-y-0.5 leading-none"
          style={{ fontFamily: "'Noto Sans Bengali', 'Mukti Narrow', sans-serif" }}
        >
          ঞ
        </span>
      </div>
      {showText && (
        <div className="flex flex-col">
          <span className="font-bold tracking-tight text-slate-900 dark:text-nya-white text-xl sm:text-2xl leading-tight">
            Nya <span className="text-teal-600 dark:text-nya-teal font-normal text-sm sm:text-base opacity-90">(ঞ)</span>
          </span>
          <span className="text-xs text-slate-500 dark:text-nya-slate font-medium">Vocal for Local</span>
        </div>
      )}
    </div>
  );
};
