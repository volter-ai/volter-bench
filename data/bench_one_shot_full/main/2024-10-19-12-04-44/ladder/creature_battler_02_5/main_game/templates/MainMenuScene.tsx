import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, X } from 'lucide-react';

interface Player {
  uid: string;
  stats: Record<string, number>;
  meta: Record<string, any>;
  entities: Record<string, any>;
  collections: Record<string, any>;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
  };
  stats: Record<string, any>;
  meta: Record<string, any>;
  collections: Record<string, any>;
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
            onClick={() => emitButtonClick('play')}
            className="flex items-center justify-center px-6 py-3 text-lg font-semibold text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors"
          >
            <Play className="mr-2" size={24} />
            Play
          </button>
        )}
        {availableButtonSlugs.includes('quit') && (
          <button
            onClick={() => emitButtonClick('quit')}
            className="flex items-center justify-center px-6 py-3 text-lg font-semibold text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors"
          >
            <X className="mr-2" size={24} />
            Quit
          </button>
        )}
      </div>
    );
  };

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-900 to-blue-700 flex flex-col items-center justify-between p-8" style={{ aspectRatio: '16/9' }}>
      <h1 className="text-5xl font-bold text-white mt-16">
        {data.display_name || 'Awesome Game'}
      </h1>
      <div className="mb-16">
        {renderButtons()}
      </div>
    </div>
  );
}
