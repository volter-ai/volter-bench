import React from 'react';

export default function Home({ onStartGame }) {
  return (
    <div className="relative h-screen w-screen overflow-hidden">
      {/* Base gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-slate-100 to-rose-100 opacity-90 pointer-events-none" />
      
      {/* Animated gradient overlay */}
      <div 
        className="absolute inset-0 animate-gradient-slow bg-gradient-to-br from-slate-200/50 via-rose-100/50 to-slate-100/50 pointer-events-none"
        style={{
          backgroundSize: '400% 400%',
          animation: 'gradient 15s ease infinite'
        }}
      />

      {/* Main content */}
      <div className="relative z-20 h-full w-full flex flex-col items-center justify-center p-4">
        <h1 
          className="text-5xl md:text-6xl font-playfair font-bold mb-12 text-slate-800 text-center leading-tight animate-float"
          style={{
            textShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}
        >
          eternity_1
        </h1>

        <button
          onClick={onStartGame}
          className="px-12 py-4 bg-slate-800 text-rose-50 rounded-lg font-cormorant text-xl tracking-wider
                     hover:bg-slate-700 hover:scale-105 transform transition-all duration-300
                     shadow-lg hover:shadow-xl active:scale-95"
        >
          Begin Journey
        </button>
      </div>
    </div>
  );
}
