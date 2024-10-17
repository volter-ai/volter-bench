import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full bg-gray-100 flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex items-center justify-start">
          <div className="text-left">
            <h2 className="text-xl font-bold">{opponentCreature?.display_name}</h2>
            <div className="flex items-center space-x-2">
              <Sword size={16} />
              <span>{opponentCreature?.stats.attack}</span>
              <Shield size={16} />
              <span>{opponentCreature?.stats.defense}</span>
              <Zap size={16} />
              <span>{opponentCreature?.stats.speed}</span>
            </div>
          </div>
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex items-center justify-end">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex items-end justify-start">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex items-end justify-end">
          <div className="text-right">
            <h2 className="text-xl font-bold">{playerCreature?.display_name}</h2>
            <div className="flex items-center justify-end space-x-2">
              <Sword size={16} />
              <span>{playerCreature?.stats.attack}</span>
              <Shield size={16} />
              <span>{playerCreature?.stats.defense}</span>
              <Zap size={16} />
              <span>{playerCreature?.stats.speed}</span>
            </div>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              disabled={!enabledUIDs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
