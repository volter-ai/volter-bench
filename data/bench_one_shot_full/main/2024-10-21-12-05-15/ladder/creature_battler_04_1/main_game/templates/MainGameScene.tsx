import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
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
}

interface Skill {
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

interface GameUIData {
  entities: {
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
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-start space-y-1">
      <div className="flex items-center">
        <Sword className="w-4 h-4 mr-1" />
        <span>{creature.stats.attack}</span>
      </div>
      <div className="flex items-center">
        <Shield className="w-4 h-4 mr-1" />
        <span>{creature.stats.defense}</span>
      </div>
      <div className="flex items-center">
        <Zap className="w-4 h-4 mr-1" />
        <span>{creature.stats.speed}</span>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full aspect-video bg-gradient-to-b from-blue-100 to-green-100 flex flex-col">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Opponent Creature Status */}
        <div className="flex justify-start items-start">
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
              className="transform scale-75 origin-top-left"
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          {opponent_creature && renderCreatureStats(opponent_creature)}
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          {player_creature && renderCreatureStats(player_creature)}
        </div>

        {/* Player Creature Status */}
        <div className="flex justify-end items-end">
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              className="transform scale-75 origin-bottom-right"
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {props.data.meta.battle_ended ? (
          <div className="text-center text-2xl font-bold">Battle Ended!</div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {player_creature?.collections?.skills?.map((skill: Skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
