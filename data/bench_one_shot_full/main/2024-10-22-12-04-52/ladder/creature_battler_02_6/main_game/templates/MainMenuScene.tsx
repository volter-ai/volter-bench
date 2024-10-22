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

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerName = props.data.entities.player?.display_name || 'Player';

  return (
    <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full h-full max-w-[177.78vh] max-h-[56.25vw] flex flex-col justify-between items-center p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-8">
          Creature Battle Game
        </h1>

        <div className="text-xl text-white">
          Welcome, {playerName}!
        </div>

        <div className="flex flex-col space-y-4 mb-8">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-opacity-80 transition-colors"
            >
              <Play className="mr-2" size={24} />
              Play Game
            </button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-opacity-80 transition-colors"
            >
              <X className="mr-2" size={24} />
              Quit Game
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
