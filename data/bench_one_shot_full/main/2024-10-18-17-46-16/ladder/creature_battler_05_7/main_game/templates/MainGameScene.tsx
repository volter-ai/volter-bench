import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string; is_physical: boolean };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number };
  meta: { creature_type: string };
  uid: string;
  display_name: string;
  description: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  entities: { active_creature: Creature };
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
  stats: { turn_counter: number };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player.entities.active_creature;
  const opponentCreature = props.data.entities.opponent.entities.active_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent Creature */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <img
              src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          )}
        </div>

        {/* Top-right: Opponent Status */}
        <div className="flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom-left: Player Status */}
        <div className="flex justify-start items-end">
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

        {/* Bottom-right: Player Creature */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <img
              src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes("attack") && (
            <Button onClick={() => emitButtonClick("attack")}>
              <Sword className="mr-2 h-4 w-4" /> Attack
            </Button>
          )}
          {availableButtonSlugs.includes("swap") && (
            <Button onClick={() => emitButtonClick("swap")}>
              <Repeat className="mr-2 h-4 w-4" /> Swap
            </Button>
          )}
          {availableButtonSlugs.includes("back") && (
            <Button onClick={() => emitButtonClick("back")}>
              <ArrowLeft className="mr-2 h-4 w-4" /> Back
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
