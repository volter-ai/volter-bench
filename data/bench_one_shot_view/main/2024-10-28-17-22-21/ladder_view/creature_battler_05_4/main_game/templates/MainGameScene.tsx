import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
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
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: { prototype_id: string; category: string; creature_type: string };
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
  description: string;
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
    <div className="w-full h-0 pb-[56.25%] relative">
      <div className="absolute inset-0 flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {/* Top-left: Opponent Status */}
          <div className="flex justify-start items-start">
            <CreatureCard
              uid={opponentCreature?.uid ?? ""}
              name={opponentCreature?.display_name ?? "Unknown"}
              image={`/images/creatures/${opponentCreature?.meta.prototype_id ?? "unknown"}_front.png`}
              hp={opponentCreature?.stats.hp ?? 0}
              maxHp={opponentCreature?.stats.max_hp ?? 1}
            />
          </div>

          {/* Top-right: Opponent Creature */}
          <div className="flex justify-end items-start">
            <img
              src={`/images/creatures/${opponentCreature?.meta.prototype_id ?? "unknown"}_front.png`}
              alt={opponentCreature?.display_name ?? "Unknown"}
              className="w-48 h-48 object-contain"
            />
          </div>

          {/* Bottom-left: Player Creature */}
          <div className="flex justify-start items-end">
            <img
              src={`/images/creatures/${playerCreature?.meta.prototype_id ?? "unknown"}_back.png`}
              alt={playerCreature?.display_name ?? "Unknown"}
              className="w-48 h-48 object-contain"
            />
          </div>

          {/* Bottom-right: Player Status */}
          <div className="flex justify-end items-end">
            <CreatureCard
              uid={playerCreature?.uid ?? ""}
              name={playerCreature?.display_name ?? "Unknown"}
              image={`/images/creatures/${playerCreature?.meta.prototype_id ?? "unknown"}_back.png`}
              hp={playerCreature?.stats.hp ?? 0}
              maxHp={playerCreature?.stats.max_hp ?? 1}
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-100 p-4 flex flex-col">
          <div className="flex flex-wrap gap-2 mb-4">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                disabled={!availableButtonSlugs.includes(skill.display_name.toLowerCase())}
              />
            ))}
          </div>
          <div className="flex flex-wrap gap-2">
            <Button
              onClick={() => emitButtonClick("attack")}
              disabled={!availableButtonSlugs.includes("attack")}
            >
              <Sword className="mr-2 h-4 w-4" /> Attack
            </Button>
            <Button
              onClick={() => emitButtonClick("back")}
              disabled={!availableButtonSlugs.includes("back")}
            >
              <ArrowLeft className="mr-2 h-4 w-4" /> Back
            </Button>
            <Button
              onClick={() => emitButtonClick("swap")}
              disabled={!availableButtonSlugs.includes("swap")}
            >
              <Repeat className="mr-2 h-4 w-4" /> Swap
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
