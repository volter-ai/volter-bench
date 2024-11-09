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
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

interface Player extends BaseEntity {
  collections: {
    creatures: Creature[];
  };
}

interface Creature extends BaseEntity {
  stats: GameStats & {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Skill extends BaseEntity {
  stats: GameStats & {
    damage: number;
  };
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

  if (!props?.data) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gradient-to-b from-slate-800 to-slate-900">
        <p className="text-white">Loading game...</p>
      </div>
    );
  }

  return (
    <div 
      className="w-full h-full flex items-center justify-center bg-gradient-to-b from-slate-800 to-slate-900"
      role="main"
      aria-label="Main Menu"
    >
      <div className="w-full max-w-[177.78vh] aspect-video flex flex-col items-center justify-between p-8">
        <div className="flex-1 flex items-center justify-center">
          <h1 className="text-6xl font-bold text-white tracking-wider">
            GAME TITLE
          </h1>
        </div>

        <nav className="flex flex-col gap-4 items-center mb-16" aria-label="Main menu navigation">
          {availableButtonSlugs?.includes('play') && (
            <button
              onClick={() => emitButtonClick('play')}
              className="flex items-center gap-2 px-8 py-4 bg-green-600 hover:bg-green-500 text-white rounded-lg text-xl transition-colors"
              aria-label="Start game"
            >
              <Play className="w-6 h-6" aria-hidden="true" />
              <span>Play Game</span>
            </button>
          )}

          {availableButtonSlugs?.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="flex items-center gap-2 px-8 py-4 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xl transition-colors"
              aria-label="Quit game"
            >
              <XCircle className="w-6 h-6" aria-hidden="true" />
              <span>Quit</span>
            </button>
          )}
        </nav>
      </div>
    </div>
  );
}
