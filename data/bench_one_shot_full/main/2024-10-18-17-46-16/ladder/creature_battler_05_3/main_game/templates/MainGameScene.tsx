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
  collections: { skills: Skill[] };
  uid: string;
  display_name: string;
  description: string;
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

  const playerCreature = props.data.entities.player.entities.active_creature;
  const opponentCreature = props.data.entities.opponent.entities.active_creature;

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponentCreature?.uid ?? ""}
            name={opponentCreature?.display_name ?? "Unknown"}
            image={`/${opponentCreature?.display_name.toLowerCase()}.png`}
            hp={opponentCreature?.stats.hp ?? 0}
            maxHp={opponentCreature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <img src={`/${opponentCreature?.display_name.toLowerCase()}.png`} alt="Opponent Creature" className="w-40 h-40 object-contain" />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          <img src={`/${playerCreature?.display_name.toLowerCase()}.png`} alt="Player Creature" className="w-40 h-40 object-contain" />
        </div>

        {/* Player Status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            image={`/${playerCreature?.display_name.toLowerCase()}.png`}
            hp={playerCreature?.stats.hp ?? 0}
            maxHp={playerCreature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
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
