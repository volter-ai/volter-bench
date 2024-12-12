import React from 'react';

export default function Loading({ error }) {
  if (error) {
    return (
      <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-rose-100 to-slate-200 opacity-90 pointer-events-none" />
        <div className="absolute inset-0 animate-gradient-slow bg-gradient-to-br from-rose-200/50 via-slate-200/50 to-rose-100/50 pointer-events-none" 
             style={{
               backgroundSize: '400% 400%',
               animation: 'gradient 15s ease infinite'
             }}
        />
        <div className="relative z-10 text-center p-8 max-w-md">
          <h1 className="text-2xl font-playfair text-rose-800 mb-4 font-bold">
            Failed to Load Game
          </h1>
          <p className="text-rose-700 font-lato">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-slate-100 to-rose-100 opacity-90 pointer-events-none" />
      <div className="absolute inset-0 animate-gradient-slow bg-gradient-to-br from-slate-200/50 via-rose-100/50 to-slate-100/50 pointer-events-none"
           style={{
             backgroundSize: '400% 400%',
             animation: 'gradient 15s ease infinite'
           }}
      />
      <div className="relative z-10 text-center p-8">
        <h1 className="text-2xl font-playfair text-slate-800 mb-6 font-bold animate-fade-in">
          Loading Game Assets
        </h1>
        <div className="relative">
          <div className="w-16 h-16 border-4 border-rose-300 border-t-transparent rounded-full animate-spin mx-auto"
               style={{
                 boxShadow: '0 0 15px rgba(244, 63, 94, 0.2)'
               }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-white/50 to-transparent pointer-events-none" />
        </div>
      </div>
    </div>
  );
}
