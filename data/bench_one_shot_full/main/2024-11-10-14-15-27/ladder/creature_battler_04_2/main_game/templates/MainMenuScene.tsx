import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react';

interface Stats {
  hp?: number;
  max_hp?: number;
  attack?: number;
  defense?: number;
  sp_attack?: number;
  sp_defense?: number;
  speed?: number;
  base_damage?: number;
}

interface Meta {
  prototype_id: string;
  category: string;
  creature_type?: string;
  skill_type?: string;
  is_physical?: boolean;
}

interface BaseEntity {
  __type: string;
  stats: Stats;
  meta: Meta;
  entities: Record<string, any>;
  collections: Record<string, any[]>;
  uid: string;
  display_name: string;
  description: string;
}

interface Skill extends BaseEntity {
  __type: 'Skill';
}

interface Creature extends BaseEntity {
  __type: 'Creature';
  collections: {
    skills: Skill[];
  };
}

interface Player extends BaseEntity {
  __type: 'Player';
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  __type: 'MainMenuScene';
  stats: Record<string, any>;
  meta: Record<string, any>;
  entities: {
    player: Player;
  };
  collections: Record<string, any>;
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  if (!props.data) {
    return null;
  }

  return (
    <div className="relative w-full" style={{ paddingBottom: '56.25%' }}>
      <div className="absolute inset-0 flex flex-col items-center justify-between p-8 bg-gradient-to-b from-slate-900 to-slate-800">
        
        {/* Title Section */}
        <div className="flex-1 flex items-center justify-center">
          <div className="w-96 h-32 bg-slate-700 flex items-center justify-center rounded-lg">
            {/* Placeholder for title image */}
            <h1 className="text-4xl font-bold text-white tracking-wider">
              {props.data.display_name || 'GAME TITLE'}
            </h1>
          </div>
        </div>

        {/* Spacer */}
        <div className="flex-1" />

        {/* Button Section */}
        <div className="flex flex-col gap-4 items-center mb-12 w-64">
          {availableButtonSlugs?.includes('play-game') && (
            <button
              onClick={() => emitButtonClick('play-game')}
              className="w-full flex items-center justify-center gap-2 px-8 py-4 text-xl 
                         bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
            >
              <Play size={24} />
              Play Game
            </button>
          )}

          {availableButtonSlugs?.includes('quit') && (
            <button
              onClick={() => emitButtonClick('quit')}
              className="w-full flex items-center justify-center gap-2 px-8 py-4 text-xl 
                         bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
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
