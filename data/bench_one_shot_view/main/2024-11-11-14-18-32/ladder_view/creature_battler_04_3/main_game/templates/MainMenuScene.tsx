import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Play, XCircle } from 'lucide-react'

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
  uid: string;
  stats: Stats;
  meta: Meta;
  entities: Record<string, any>;
  collections: Record<string, any>;
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
  entities: {
    player: Player;
  };
  uid: string;
  display_name: string;
  description: string;
}

export function MainMenuSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  if (!props.data?.uid) {
    return null;
  }

  return (
    <div 
      key={props.data.uid}
      className="w-full h-full aspect-video bg-gradient-to-b from-slate-900 to-slate-800 flex flex-col items-center justify-between p-8"
    >
      <div className="flex-1 flex items-center justify-center">
        <h1 className="text-6xl font-bold text-white tracking-wider">
          {props.data.display_name || 'CREATURE BATTLE'}
        </h1>
      </div>

      <div className="flex flex-col gap-y-4 items-center mb-12">
        {availableButtonSlugs?.includes('play') && (
          <button
            onClick={() => emitButtonClick('play')}
            className="flex items-center gap-x-2 bg-green-600 hover:bg-green-700 text-white px-8 py-3 rounded-lg text-xl font-semibold transition-colors"
          >
            <Play size={24} />
            Play Game
          </button>
        )}

        {availableButtonSlugs?.includes('quit') && (
          <button
            onClick={() => emitButtonClick('quit')}
            className="flex items-center gap-x-2 bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg text-xl font-semibold transition-colors"
          >
            <XCircle size={24} />
            Quit
          </button>
        )}
      </div>
    </div>
  )
}
