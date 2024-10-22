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

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerName = data.entities.player?.display_name || "Player";

  const buttonConfig = {
    play: { text: "Play", icon: Play },
    quit: { text: "Quit", icon: X },
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-900">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] bg-gradient-to-b from-blue-500 to-blue-700 flex flex-col items-center justify-between p-8">
        <div className="text-4xl sm:text-6xl font-bold text-white mt-8 sm:mt-16">
          Creature Battle Game
        </div>

        <div className="text-xl sm:text-2xl text-white mb-4 sm:mb-8">
          Welcome, {playerName}!
        </div>

        <div className="flex flex-col space-y-4 mb-8 sm:mb-16">
          {availableButtonSlugs.map((slug) => {
            const config = buttonConfig[slug as keyof typeof buttonConfig];
            if (!config) return null;

            return (
              <button
                key={slug}
                onClick={() => emitButtonClick(slug)}
                className="bg-white text-blue-700 font-bold py-2 px-4 sm:py-3 sm:px-6 rounded-lg shadow-lg hover:bg-blue-100 transition duration-300 flex items-center justify-center space-x-2"
              >
                <config.icon className="w-4 h-4 sm:w-6 sm:h-6" />
                <span>{config.text}</span>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
