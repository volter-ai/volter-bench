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
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        <div className="h-2/3 flex flex-col">
          {/* Battlefield */}
          <div className="flex-1 flex">
            {/* Opponent Status */}
            <div className="w-1/2 p-4 flex items-start justify-start">
              <CreatureCard
                uid={opponent.entities.active_creature?.uid ?? ""}
                name={opponent.entities.active_creature?.display_name ?? "Unknown"}
                image="/placeholder.png"
                hp={opponent.entities.active_creature?.stats.hp ?? 0}
                maxHp={opponent.entities.active_creature?.stats.max_hp ?? 1}
              />
            </div>
            {/* Opponent Creature */}
            <div className="w-1/2 p-4 flex items-end justify-end">
              <div className="w-40 h-40 bg-gray-300 rounded-full"></div>
            </div>
          </div>
          <div className="flex-1 flex">
            {/* Player Creature */}
            <div className="w-1/2 p-4 flex items-start justify-start">
              <div className="w-40 h-40 bg-gray-300 rounded-full"></div>
            </div>
            {/* Player Status */}
            <div className="w-1/2 p-4 flex items-end justify-end">
              <CreatureCard
                uid={player.entities.active_creature?.uid ?? ""}
                name={player.entities.active_creature?.display_name ?? "Unknown"}
                image="/placeholder.png"
                hp={player.entities.active_creature?.stats.hp ?? 0}
                maxHp={player.entities.active_creature?.stats.max_hp ?? 1}
              />
            </div>
          </div>
        </div>
        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4 flex flex-col justify-center">
          <div className="flex justify-center space-x-4">
            {availableButtonSlugs.includes("attack") && (
              <Button onClick={() => emitButtonClick("attack")} uid="attack-button">
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes("swap") && (
              <Button onClick={() => emitButtonClick("swap")} uid="swap-button">
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
            {availableButtonSlugs.includes("back") && (
              <Button onClick={() => emitButtonClick("back")} uid="back-button">
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
          </div>
          {player.entities.active_creature?.collections.skills && (
            <div className="mt-4 flex justify-center space-x-2">
              {player.entities.active_creature.collections.skills.map((skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
