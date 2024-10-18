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
    <div className="w-full h-full flex items-center justify-center bg-gray-900">
      <div className="w-full max-w-[177.78vh] aspect-video bg-gray-800 flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white text-center">
            Creature Battle Game
          </h1>
        </div>
        <div className="flex space-x-4">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => handleButtonClick('play')}
              className="bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded flex items-center"
            >
              <Play className="mr-2" size={24} />
              Play
            </button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => handleButtonClick('quit')}
              className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded flex items-center"
            >
              <X className="mr-2" size={24} />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
