import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, number>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView({ data, uid }: { data: GameUIData; uid: string }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const renderButtons = () => {
    return (
      <div className="flex flex-col space-y-4">
        {availableButtonSlugs.includes('play') && (
          <button
            className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
            onClick={() => emitButtonClick('play')}
          >
            <Play className="mr-2" /> Play Game
          </button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <button
            className="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded flex items-center justify-center"
            onClick={() => emitButtonClick('quit')}
          >
            <X className="mr-2" /> Quit Game
          </button>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-900">
      <div className="w-full h-full max-w-screen-lg mx-auto aspect-video bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-white mt-16">
          {data?.display_name ?? "Game Title"}
        </h1>
        <div className="flex-grow" />
        {renderButtons()}
      </div>
    </div>
  );
}
