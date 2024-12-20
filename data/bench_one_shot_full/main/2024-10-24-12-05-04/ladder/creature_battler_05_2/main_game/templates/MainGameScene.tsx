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
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponent.entities.active_creature.uid}
            name={opponent.entities.active_creature.display_name}
            image="/placeholder-opponent.png"
            hp={opponent.entities.active_creature.stats.hp}
            maxHp={opponent.entities.active_creature.stats.max_hp}
          />
        </div>

        <div className="flex items-center justify-center">
          <img
            src="/placeholder-opponent-creature.png"
            alt="Opponent Creature"
            className="max-w-full max-h-full object-contain"
          />
        </div>

        <div className="flex items-center justify-center">
          <img
            src="/placeholder-player-creature.png"
            alt="Player Creature"
            className="max-w-full max-h-full object-contain"
          />
        </div>

        <div className="flex items-end justify-end">
          <CreatureCard
            uid={player.entities.active_creature.uid}
            name={player.entities.active_creature.display_name}
            image="/placeholder-player.png"
            hp={player.entities.active_creature.stats.hp}
            maxHp={player.entities.active_creature.stats.max_hp}
          />
        </div>
      </div>

      <div className="h-1/3 bg-gray-800 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes("attack") && (
            <button
              onClick={() => emitButtonClick("attack")}
              className="bg-red-500 text-white p-4 rounded flex items-center justify-center"
            >
              <Sword className="mr-2" /> Attack
            </button>
          )}
          {availableButtonSlugs.includes("back") && (
            <button
              onClick={() => emitButtonClick("back")}
              className="bg-gray-500 text-white p-4 rounded flex items-center justify-center"
            >
              <ArrowLeft className="mr-2" /> Back
            </button>
          )}
          {availableButtonSlugs.includes("swap") && (
            <button
              onClick={() => emitButtonClick("swap")}
              className="bg-blue-500 text-white p-4 rounded flex items-center justify-center"
            >
              <Repeat className="mr-2" /> Swap
            </button>
          )}
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
      </div>
    </div>
  );
}
