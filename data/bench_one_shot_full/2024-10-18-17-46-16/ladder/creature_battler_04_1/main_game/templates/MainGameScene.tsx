import React from 'react';
import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: 'Skill';
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: 'Creature';
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
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

  return (
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image="/placeholder-opponent.png"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            className="transform scale-75 origin-top-left"
          />
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          <img
            src="/placeholder-opponent-front.png"
            alt={opponent_creature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          <img
            src="/placeholder-player-back.png"
            alt={player_creature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex justify-end items-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image="/placeholder-player.png"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="transform scale-75 origin-bottom-right"
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
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
                stats={`Base Damage: ${skill.stats.base_damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              >
                <Sword className="mr-2 h-4 w-4" />
                {skill.display_name}
              </SkillButton>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
