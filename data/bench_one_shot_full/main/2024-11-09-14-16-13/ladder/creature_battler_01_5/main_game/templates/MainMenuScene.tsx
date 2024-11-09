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

  return (
    <div className="relative w-full h-0 pb-[56.25%] bg-gradient-to-b from-slate-800 to-slate-900">
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8">
        {/* Title Section */}
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            CREATURE GAME
          </h1>
        </div>

        {/* Button Section */}
        <div className="flex flex-col gap-4 mb-16">
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center gap-2 px-8 py-4 
                       bg-green-600 hover:bg-green-500 
                       text-white text-xl font-semibold rounded-lg 
                       transition-colors duration-200"
            >
              <Play size={24} />
              Play Game
            </button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center gap-2 px-8 py-4 
                       bg-red-600 hover:bg-red-500 
                       text-white text-xl font-semibold rounded-lg 
                       transition-colors duration-200"
            >
              <XCircle size={24} />
              Quit
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
