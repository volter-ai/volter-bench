import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
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
  entities: {
    active_creature: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
  message?: string;
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Status */}
          <div className="flex justify-start items-start">
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

          {/* Opponent Creature */}
          <div className="flex justify-end items-start">
            {opponentCreature && (
              <img
                src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>

          {/* Player Creature */}
          <div className="flex justify-start items-end">
            {playerCreature && (
              <img
                src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>

          {/* Player Status */}
          <div className="flex justify-end items-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/images/creatures/${playerCreature.meta.creature_type}.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4 flex flex-col justify-between">
          {props.data.message && (
            <div className="mb-4 text-center font-bold">{props.data.message}</div>
          )}
          <div className="grid grid-cols-2 grid-rows-2 gap-4">
            {availableButtonSlugs.includes('attack') && (
              <SkillButton
                uid="attack-button"
                skillName="Attack"
                description="Choose an attack"
                stats=""
                onClick={() => emitButtonClick('attack')}
              >
                <Sword className="mr-2" /> Attack
              </SkillButton>
            )}
            {availableButtonSlugs.includes('swap') && (
              <SkillButton
                uid="swap-button"
                skillName="Swap"
                description="Swap your active creature"
                stats=""
                onClick={() => emitButtonClick('swap')}
              >
                <Repeat className="mr-2" /> Swap
              </SkillButton>
            )}
            {availableButtonSlugs.includes('back') && (
              <SkillButton
                uid="back-button"
                skillName="Back"
                description="Go back"
                stats=""
                onClick={() => emitButtonClick('back')}
              >
                <ArrowLeft className="mr-2" /> Back
              </SkillButton>
            )}
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
