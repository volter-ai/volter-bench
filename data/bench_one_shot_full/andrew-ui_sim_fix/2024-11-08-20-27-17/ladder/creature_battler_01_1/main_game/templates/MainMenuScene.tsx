import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface GameStats {
  [key: string]: number;
}

interface GameMeta {
  prototype_id: string;
  category: string;
}

interface BaseEntity {
  __type: string;
  stats: GameStats;
  meta: GameMeta;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  __type: 'Player';
}

interface MainMenuScene extends BaseEntity {
  __type: 'MainMenuScene';
  entities: {
    player: Player;
  };
}

interface GameUIData {
  entities: {
    player: Player;
  };
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs = [],
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div className="relative w-full max-w-[1920px] mx-auto" style={{ paddingBottom: '56.25%' }}>
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
        
        {/* Title Image Section */}
        <div className="flex-1 flex items-center justify-center w-full max-w-3xl">
          <div 
            className="w-full h-48 bg-center bg-contain bg-no-repeat"
            role="img"
            aria-label="Game Title"
          />
        </div>

        {/* Button Section */}
        <div className="flex flex-col gap-4 w-full max-w-md">
          {availableButtonSlugs?.includes('play') && (
            <button
              onClick={() => emitButtonClick?.('play')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors shadow-lg"
            >
              <Play className="w-6 h-6" />
              <span className="text-xl font-semibold">Play Game</span>
            </button>
          )}

          {availableButtonSlugs?.includes('quit') && (
            <button
              onClick={() => emitButtonClick?.('quit')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors shadow-lg"
            >
              <XCircle className="w-6 h-6" />
              <span className="text-xl font-semibold">Quit</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
