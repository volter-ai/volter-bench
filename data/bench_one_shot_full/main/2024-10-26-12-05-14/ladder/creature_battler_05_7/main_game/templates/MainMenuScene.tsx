import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerName = props.data.entities.player?.display_name || "Player";

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full h-0 pb-[56.25%] relative">
        <div className="absolute inset-0 flex flex-col items-center justify-between p-8 text-white">
          <div className="flex-1 flex items-center justify-center">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-center">Awesome Game Title</h1>
          </div>
          
          <div className="mb-8">
            <p className="text-xl sm:text-2xl mb-4 text-center">Welcome, {playerName}!</p>
            <div className="flex flex-col space-y-4">
              {availableButtonSlugs.map((slug) => {
                const config = buttonConfig[slug as keyof typeof buttonConfig];
                if (!config) return null;
                
                return (
                  <button
                    key={slug}
                    onClick={() => emitButtonClick(slug)}
                    className="flex items-center justify-center space-x-2 bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold text-lg hover:bg-blue-100 transition-colors"
                  >
                    <config.icon size={24} />
                    <span>{config.text}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
