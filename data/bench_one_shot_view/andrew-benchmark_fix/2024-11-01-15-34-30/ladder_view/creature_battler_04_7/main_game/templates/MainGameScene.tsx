import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-6xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Battlefield Display */}
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Creature Status */}
          <div className="col-start-1 row-start-1 flex items-start justify-start">
            <CreatureCard
              uid={opponentCreature?.uid ?? ""}
              name={opponentCreature?.display_name ?? "Unknown"}
              image={`/images/creatures/${opponentCreature?.meta.creature_type}.png`}
              hp={opponentCreature?.stats.hp ?? 0}
              maxHp={opponentCreature?.stats.max_hp ?? 1}
            />
          </div>

          {/* Opponent Creature */}
          <div className="col-start-2 row-start-1 flex items-center justify-center">
            <img
              src={`/images/creatures/${opponentCreature?.meta.creature_type}_front.png`}
              alt={opponentCreature?.display_name}
              className="max-h-full max-w-full object-contain"
            />
          </div>

          {/* Player Creature */}
          <div className="col-start-1 row-start-2 flex items-center justify-center">
            <img
              src={`/images/creatures/${playerCreature?.meta.creature_type}_back.png`}
              alt={playerCreature?.display_name}
              className="max-h-full max-w-full object-contain"
            />
          </div>

          {/* Player Creature Status */}
          <div className="col-start-2 row-start-2 flex items-end justify-end">
            <CreatureCard
              uid={playerCreature?.uid ?? ""}
              name={playerCreature?.display_name ?? "Unknown"}
              image={`/images/creatures/${playerCreature?.meta.creature_type}.png`}
              hp={playerCreature?.stats.hp ?? 0}
              maxHp={playerCreature?.stats.max_hp ?? 1}
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
            {playerCreature?.collections.skills.map((skill: Skill, index: number) => (
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
        </div>
      </div>
    </div>
  );
}
