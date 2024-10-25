import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

interface Creature {
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
  uid: string;
  display_name: string;
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

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          <img
            src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
            alt={opponentCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          <img
            src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
            alt={playerCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex justify-end items-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {playerCreature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!enabledUIDs.includes(skill.uid)}
              >
                <div className="flex items-center">
                  {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
                  {skill.display_name}
                </div>
              </SkillButton>
            ))}
          </div>
        ) : (
          <div className="text-center text-lg">Waiting for opponent...</div>
        )}
      </div>
    </div>
  );
}
