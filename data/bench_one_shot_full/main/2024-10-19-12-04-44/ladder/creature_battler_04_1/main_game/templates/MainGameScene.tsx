import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
    is_physical: boolean;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  description: string;
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
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
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
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex flex-col items-start justify-start">
          <h3 className="text-lg font-bold">{opponent_creature.display_name}</h3>
          <div className="flex items-center space-x-2">
            <div className="w-32 bg-gray-200 rounded-full h-2.5">
              <div 
                className="bg-green-600 h-2.5 rounded-full" 
                style={{width: `${(opponent_creature.stats.hp / opponent_creature.stats.max_hp) * 100}%`}}
              ></div>
            </div>
            <span className="text-sm">
              {opponent_creature.stats.hp}/{opponent_creature.stats.max_hp} HP
            </span>
          </div>
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex flex-col items-end justify-end">
          <h3 className="text-lg font-bold">{player_creature.display_name}</h3>
          <div className="flex items-center space-x-2">
            <span className="text-sm">
              {player_creature.stats.hp}/{player_creature.stats.max_hp} HP
            </span>
            <div className="w-32 bg-gray-200 rounded-full h-2.5">
              <div 
                className="bg-green-600 h-2.5 rounded-full" 
                style={{width: `${(player_creature.stats.hp / player_creature.stats.max_hp) * 100}%`}}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {props.data.meta.battle_ended ? (
          <div className="text-center text-2xl font-bold">Battle Ended!</div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              >
                {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
                {skill.display_name}
              </SkillButton>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
