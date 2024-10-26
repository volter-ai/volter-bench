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

  return (
    <div className="w-full h-screen flex items-center justify-center bg-gradient-to-b from-blue-500 to-purple-600">
      <div className="w-full max-w-[177.78vh] h-full max-h-[56.25vw] bg-gray-800 flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white text-center">
            Awesome Game Title
          </h1>
        </div>
        <div className="mb-16">
          <p className="text-xl text-white mb-4">Welcome, {playerName}!</p>
          <div className="flex flex-col gap-4">
            {availableButtonSlugs.includes('play') && (
              <button
                onClick={() => emitButtonClick('play')}
                className="flex items-center justify-center bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded"
              >
                <Play className="mr-2" /> Play Game
              </button>
            )}
            {availableButtonSlugs.includes('quit') && (
              <button
                onClick={() => emitButtonClick('quit')}
                className="flex items-center justify-center bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded"
              >
                <X className="mr-2" /> Quit Game
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
