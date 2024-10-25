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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerName = props.data.entities.player?.display_name || 'Player';

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-500 to-purple-600 flex flex-col items-center justify-between p-8">
      <div className="text-6xl font-bold text-white mt-16">
        Creature Battle Game
      </div>
      
      <div className="text-2xl text-white mb-8">
        Welcome, {playerName}!
      </div>

      <div className="flex flex-col space-y-4 mb-16">
        {availableButtonSlugs.includes('play') && (
          <button
            onClick={() => emitButtonClick('play')}
            className="bg-green-500 hover:bg-green-600 text-white font-bold py-3 px-6 rounded-full flex items-center justify-center text-xl"
          >
            <Play className="mr-2" /> Play Game
          </button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <button
            onClick={() => emitButtonClick('quit')}
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-3 px-6 rounded-full flex items-center justify-center text-xl"
          >
            <X className="mr-2" /> Quit Game
          </button>
        )}
      </div>
    </div>
  );
}
