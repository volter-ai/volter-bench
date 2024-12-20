import React, { useEffect, useState } from 'react';
import { CHARACTERS, LOCATIONS } from '../logic/gameData';

export default function Story({ gameLogic, onLeaveStory }) {
  const [content, setContent] = useState(null);
  const [location, setLocation] = useState(null);
  const [isTransitioning, setIsTransitioning] = useState(false);

  useEffect(() => {
    const current = gameLogic.getCurrentContent();
    setContent(current.content);
    setLocation(current.location);
  }, []);

  const handleAdvance = () => {
    if (isTransitioning) return;
    
    const result = gameLogic.advance();
    if (result.isGameOver) {
      onLeaveStory();
      return;
    }

    setIsTransitioning(true);
    const current = gameLogic.getCurrentContent();
    setContent(current.content);
    setLocation(current.location);
    
    setTimeout(() => {
      setIsTransitioning(false);
    }, 300);
  };

  const handleChoice = (index) => {
    if (isTransitioning) return;
    
    const currentContent = gameLogic.getCurrentContent().content;
    if (currentContent.type !== 'choice') return;
    
    const result = gameLogic.makeChoice(index);
    if (result.isGameOver) {
      onLeaveStory();
      return;
    }

    setIsTransitioning(true);
    const current = gameLogic.getCurrentContent();
    setContent(current.content);
    setLocation(current.location);
    
    setTimeout(() => {
      setIsTransitioning(false);
    }, 300);
  };

  if (!content) return null;

  return (
    <div className="relative h-screen w-screen overflow-hidden bg-slate-900">
      {/* Background */}
      <div className="absolute inset-0 z-0 pointer-events-none">
        <div className="absolute inset-0 bg-gradient-to-b from-black/30 to-black/70 z-10" />
        <div className="absolute inset-0 bg-gradient-to-r from-black/30 via-transparent to-black/30 z-10" />
        <img
          src={gameLogic.getSpriteUrl(LOCATIONS[location].spriteId)}
          alt="background"
          className="w-full h-full object-cover transition-opacity duration-500"
          style={{ opacity: isTransitioning ? 0.5 : 1 }}
        />
      </div>

      {/* Character */}
      {content.type === 'dialog' && !content.noSpeakerSprite && (
        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 z-20 pointer-events-none">
          <img
            src={gameLogic.getSpriteUrl(CHARACTERS[content.speaker].spriteId, content.variation)}
            alt={CHARACTERS[content.speaker].name}
            className="max-w-none transition-opacity duration-300"
            style={{ 
              width: 'auto', 
              height: 'auto',
              opacity: isTransitioning ? 0 : 1 
            }}
          />
        </div>
      )}

      {/* Dialog/Choice UI */}
      <div className="absolute bottom-0 left-0 right-0 p-4 md:p-6 z-30">
        <div className="backdrop-blur-md bg-slate-900/80 p-6 rounded-xl border border-slate-700/50 shadow-xl"
             style={{ 
               transition: 'all 0.3s ease-in-out',
               opacity: isTransitioning ? 0.5 : 1
             }}>
          {content.type === 'dialog' && (
            <>
              <div className="text-2xl mb-3 font-playfair font-bold text-rose-100">
                {CHARACTERS[content.speaker].name}
              </div>
              <div className="text-lg mb-4 font-lato text-slate-200 leading-relaxed">
                {content.text}
              </div>
              <button
                onClick={handleAdvance}
                className="text-rose-300 text-sm hover:text-rose-200 transition-colors font-crimson italic">
                Continue...
              </button>
            </>
          )}

          {content.type === 'narration' && (
            <>
              <div className="text-lg italic mb-4 font-crimson text-slate-200 leading-relaxed">
                {content.text}
              </div>
              <button
                onClick={handleAdvance}
                className="text-rose-300 text-sm hover:text-rose-200 transition-colors font-crimson italic">
                Continue...
              </button>
            </>
          )}

          {content.type === 'choice' && (
            <>
              <div className="text-lg mb-6 font-lato text-slate-200 leading-relaxed">
                {content.text}
              </div>
              <div className="space-y-3">
                {content.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleChoice(index)}
                    className="w-full p-4 backdrop-blur-sm bg-slate-800/90 hover:bg-slate-700/90 
                             rounded-lg text-left transition-all duration-200 border border-slate-600/50 
                             text-rose-50 font-crimson text-lg hover:scale-[1.02] hover:shadow-lg
                             active:scale-[0.98]">
                    {option.text}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
