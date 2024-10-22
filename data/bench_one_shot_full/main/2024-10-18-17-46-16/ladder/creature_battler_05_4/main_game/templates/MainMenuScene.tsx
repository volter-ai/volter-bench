import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const buttonConfig = {
    play: { text: 'Play', icon: Play },
    quit: { text: 'Quit', icon: X },
  };

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] aspect-video bg-black bg-opacity-50 flex flex-col items-center justify-between p-8">
        <div className="text-6xl font-bold text-white mt-16 animate-pulse">
          Awesome Game Title
        </div>
        
        <div className="flex flex-col items-center space-y-4 mb-16">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;
            
            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="flex items-center justify-center space-x-2 bg-white text-black px-8 py-3 rounded-full text-xl font-semibold transition-all duration-200 hover:bg-opacity-80 hover:scale-105"
              >
                <config.icon className="w-6 h-6" />
                <span>{config.text}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
