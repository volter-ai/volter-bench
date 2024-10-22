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
  uid: string;
}

export function MainMenuSceneView({ data }: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerName = data.entities.player?.display_name || "Player";

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="relative w-full h-0 pb-[56.25%]">
      <div className="absolute inset-0 flex flex-col items-center justify-between bg-gray-800 text-white p-4">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-4xl md:text-6xl font-bold text-center">Game Title</h1>
        </div>
        
        <div className="mb-8">
          <p className="text-xl text-center mb-4">Welcome, {playerName}!</p>
          <div className="flex flex-col items-center">
            {availableButtonSlugs.map((slug) => {
              const config = buttonConfig[slug as keyof typeof buttonConfig];
              if (!config) return null;
              
              return (
                <button
                  key={slug}
                  onClick={() => emitButtonClick(slug)}
                  className="flex items-center justify-center bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded my-2 w-48"
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
