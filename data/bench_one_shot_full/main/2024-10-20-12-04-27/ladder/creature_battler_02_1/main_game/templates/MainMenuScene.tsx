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
      <div className="flex space-x-4">
        {availableButtonSlugs.includes('play') && (
          <button
            className="px-4 py-2 flex items-center space-x-2 bg-green-500 hover:bg-green-600 text-white rounded"
            onClick={() => emitButtonClick('play')}
          >
            <Play size={20} />
            <span>Play</span>
          </button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <button
            className="px-4 py-2 flex items-center space-x-2 bg-red-500 hover:bg-red-600 text-white rounded"
            onClick={() => emitButtonClick('quit')}
          >
            <X size={20} />
            <span>Quit</span>
          </button>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-4xl font-bold text-white mt-16">
        {data.display_name || 'Game Title'}
      </h1>
      <div className="flex-grow" />
      {renderButtons()}
    </div>
  );
}
