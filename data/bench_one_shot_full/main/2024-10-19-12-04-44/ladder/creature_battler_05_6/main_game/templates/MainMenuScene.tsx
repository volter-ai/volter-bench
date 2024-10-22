import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface GameUIData {
  entities: {
    player: {
      uid: string;
      display_name: string;
    };
  };
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] flex flex-col items-center justify-between p-8 text-white">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mt-8 sm:mt-16">Creature Battle</h1>
        
        <div className="flex flex-col items-center space-y-4 mb-8 sm:mb-16">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;
            
            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="flex items-center justify-center space-x-2 bg-white text-blue-600 px-6 sm:px-8 py-2 sm:py-3 rounded-full text-lg sm:text-xl font-semibold hover:bg-blue-100 transition-colors duration-200"
              >
                <config.icon size={20} />
                <span>{config.text}</span>
              </button>
            );
          })}
        </div>

        <div className="text-sm">
          Welcome, {data.entities.player?.display_name || 'Player'}!
        </div>
      </div>
    </div>
  );
}
