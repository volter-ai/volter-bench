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

export function MainMenuSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const handleButtonClick = (slug: string) => {
    emitButtonClick(slug);
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between bg-gradient-to-b from-blue-500 to-purple-600 text-white p-8">
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-center">Creature Battle Game</h1>
      </div>

      <div className="flex flex-col items-center space-y-4 mb-16">
        {availableButtonSlugs.includes('play') && (
          <button
            onClick={() => handleButtonClick('play')}
            className="flex items-center justify-center w-48 h-12 bg-green-500 hover:bg-green-600 rounded-full text-xl font-semibold transition-colors duration-200"
          >
            <Play className="mr-2" size={24} />
            Play
          </button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <button
            onClick={() => handleButtonClick('quit')}
            className="flex items-center justify-center w-48 h-12 bg-red-500 hover:bg-red-600 rounded-full text-xl font-semibold transition-colors duration-200"
          >
            <X className="mr-2" size={24} />
            Quit
          </button>
        )}
      </div>

      <div className="text-sm opacity-70">
        Welcome, {props.data.entities.player?.display_name || 'Player'}!
      </div>
    </div>
  );
}
