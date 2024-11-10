import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Heart } from 'lucide-react';

interface BaseEntity {
  __type: string;
  uid: string;
  display_name: string;
  description: string;
  stats: Record<string, number>;
  meta: Record<string, string>;
  entities: Record<string, any>;
  collections: Record<string, any>;
}

interface Skill extends BaseEntity {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: "Skill";
    skill_type: string;
    is_physical: boolean;
  };
}

interface Creature extends BaseEntity {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: "Creature";
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player extends BaseEntity {
  __type: "Player";
  meta: {
    prototype_id: string;
    category: "Player";
  };
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

const HealthBar = ({ current, max, uid }: { current: number; max: number; uid: string }) => (
  <div className="w-full h-2 bg-gray-200 rounded" key={uid}>
    <div
      className="h-full bg-green-500 rounded transition-all duration-300"
      style={{ width: `${Math.max(0, Math.min(100, (current / max) * 100))}%` }}
    />
  </div>
);

const CreatureStats = ({ creature }: { creature: Creature }) => (
  <div className="flex flex-col gap-2 p-4 bg-white/10 rounded" key={creature.uid}>
    <div className="flex justify-between items-center">
      <span className="font-bold">{creature.display_name}</span>
      <span className="text-sm">
        {creature.stats.hp}/{creature.stats.max_hp} HP
      </span>
    </div>
    <HealthBar 
      current={creature.stats.hp} 
      max={creature.stats.max_hp}
      uid={`${creature.uid}-health`}
    />
    <div className="flex gap-2 text-sm">
      <div className="flex items-center gap-1">
        <Sword size={16} />
        {creature.stats.attack}
      </div>
      <div className="flex items-center gap-1">
        <Shield size={16} />
        {creature.stats.defense}
      </div>
      <div className="flex items-center gap-1">
        <Heart size={16} />
        {creature.stats.speed}
      </div>
    </div>
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="w-full h-full flex flex-col bg-gradient-to-b from-blue-900 to-blue-800">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Stats */}
        <div className="col-start-1 row-start-1">
          <CreatureStats creature={opponentCreature} />
        </div>
        
        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-center items-center">
          <div className="relative" key={`${opponentCreature.uid}-display`}>
            <div className="w-32 h-32 bg-gray-400 rounded-full opacity-20 absolute -bottom-4 blur-sm" />
            <div className="w-32 h-32 bg-gradient-to-b from-red-500 to-red-600 rounded-lg shadow-lg" />
          </div>
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex justify-center items-center">
          <div className="relative" key={`${playerCreature.uid}-display`}>
            <div className="w-32 h-32 bg-gray-400 rounded-full opacity-20 absolute -bottom-4 blur-sm" />
            <div className="w-32 h-32 bg-gradient-to-b from-blue-500 to-blue-600 rounded-lg shadow-lg" />
          </div>
        </div>

        {/* Player Stats */}
        <div className="col-start-2 row-start-2">
          <CreatureStats creature={playerCreature} />
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-gray-800/90 p-4 rounded-t-xl shadow-xl z-10">
        <div className="grid grid-cols-2 gap-4 h-full">
          {playerCreature.collections.skills.map((skill) => {
            const buttonId = skill.meta.prototype_id;
            return availableButtonSlugs.includes(buttonId) ? (
              <button
                key={`skill-${skill.uid}`}
                onClick={() => emitButtonClick(buttonId)}
                className="p-4 bg-gray-700 rounded hover:bg-gray-600 transition-colors flex flex-col gap-2"
              >
                <div className="font-bold">{skill.display_name}</div>
                <div className="text-sm text-gray-300">{skill.description}</div>
                <div className="text-xs text-gray-400">
                  Type: {skill.meta.skill_type} | Damage: {skill.stats.base_damage}
                </div>
              </button>
            ) : null;
          })}
        </div>
      </div>
    </div>
  );
}
