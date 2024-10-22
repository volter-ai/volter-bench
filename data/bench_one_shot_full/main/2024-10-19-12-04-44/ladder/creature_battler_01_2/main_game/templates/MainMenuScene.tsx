import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerName = data.entities.player?.display_name || "Player";

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-800">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] bg-gray-900 flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-4xl md:text-6xl font-bold text-center text-white">Game Title</h1>
        </div>
        
        <div className="mb-8">
          <p className="text-xl text-center mb-4 text-white">Welcome, {playerName}!</p>
          <div className="flex flex-col items-center">
            {availableButtonSlugs.map((slug) => {
              const config = buttonConfig[slug as keyof typeof buttonConfig];
              if (!config) return null;
              
              return (
                <button
                  key={slug}
                  onClick={() => emitButtonClick(slug)}
                  className="flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded my-2 w-48 transition-colors duration-200"
                >
                  <config.icon className="mr-2" size={20} />
                  {config.text}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
