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
  collections: {
    creatures: BaseEntity[];
  }
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
  stats: Record<string, number>;
  meta: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  return (
    <div 
      className="relative w-full" 
      style={{ paddingBottom: '56.25%' }}
      role="main"
      aria-label="Main Menu"
    >
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
        
        {/* Title Section */}
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            {props.data?.display_name || 'Main Menu'}
          </h1>
        </div>

        {/* Button Section */}
        <div 
          className="flex flex-col gap-4 w-64"
          role="group"
          aria-label="Menu Options"
        >
          {availableButtonSlugs.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
              aria-label="Play Game"
            >
              <Play size={24} aria-hidden="true" />
              <span className="text-xl">Play Game</span>
            </button>
          )}

          {availableButtonSlugs.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center justify-center gap-2 w-full py-4 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
              aria-label="Quit Game"
            >
              <XCircle size={24} aria-hidden="true" />
              <span className="text-xl">Quit</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
