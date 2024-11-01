import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

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
  image_url: string;
}

interface Player {
  __type: "Player";
  entities: { active_creature: Creature };
  collections: { creatures: Creature[] };
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-200 to-green-200 flex flex-col">
      {/* Battlefield */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponent.entities.active_creature.uid}
            name={opponent.entities.active_creature.display_name}
            image={opponent.entities.active_creature.image_url}
            hp={opponent.entities.active_creature.stats.hp}
            maxHp={opponent.entities.active_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          <img
            src={opponent.entities.active_creature.image_url}
            alt="Opponent Creature"
            className="max-h-full max-w-full object-contain"
          />
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-start">
          <CreatureCard
            uid={player.entities.active_creature.uid}
            name={player.entities.active_creature.display_name}
            image={player.entities.active_creature.image_url}
            hp={player.entities.active_creature.stats.hp}
            maxHp={player.entities.active_creature.stats.max_hp}
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-end">
          <img
            src={player.entities.active_creature.image_url}
            alt="Player Creature"
            className="max-h-full max-w-full object-contain"
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-800 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes("attack") && (
            <SkillButton
              uid="attack"
              skillName="Attack"
              description="Choose an attack"
              stats=""
              onClick={() => emitButtonClick("attack")}
              className="flex items-center justify-center"
            >
              <Sword className="mr-2" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes("back") && (
            <SkillButton
              uid="back"
              skillName="Back"
              description="Go back"
              stats=""
              onClick={() => emitButtonClick("back")}
              className="flex items-center justify-center"
            >
              <ArrowLeft className="mr-2" /> Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes("swap") && (
            <SkillButton
              uid="swap"
              skillName="Swap"
              description="Swap creatures"
              stats=""
              onClick={() => emitButtonClick("swap")}
              className="flex items-center justify-center"
            >
              <Repeat className="mr-2" /> Swap
            </SkillButton>
          )}
          <div></div> {/* Empty div to maintain 2x2 grid */}
        </div>
      </div>
    </div>
  );
}
