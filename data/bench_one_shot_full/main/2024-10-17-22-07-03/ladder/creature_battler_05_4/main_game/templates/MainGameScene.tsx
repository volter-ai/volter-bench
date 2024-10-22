import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-0 pb-[56.25%] relative">
      <div className="absolute inset-0 flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2">
          {/* Opponent Creature Status */}
          <div className="flex items-start justify-start p-4">
            {opponent.entities.active_creature && (
              <CreatureCard
                uid={opponent.entities.active_creature.uid}
                name={opponent.entities.active_creature.display_name}
                image="/placeholder-opponent.png"
                hp={opponent.entities.active_creature.stats.hp}
                maxHp={opponent.entities.active_creature.stats.max_hp}
              />
            )}
          </div>

          {/* Opponent Creature */}
          <div className="flex items-center justify-center">
            <img src="/placeholder-opponent-creature.png" alt="Opponent Creature" className="max-w-full max-h-full" />
          </div>

          {/* Player Creature */}
          <div className="flex items-center justify-center">
            <img src="/placeholder-player-creature.png" alt="Player Creature" className="max-w-full max-h-full" />
          </div>

          {/* Player Creature Status */}
          <div className="flex items-end justify-end p-4">
            {player.entities.active_creature && (
              <CreatureCard
                uid={player.entities.active_creature.uid}
                name={player.entities.active_creature.display_name}
                image="/placeholder-player.png"
                hp={player.entities.active_creature.stats.hp}
                maxHp={player.entities.active_creature.stats.max_hp}
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
            {player.entities.active_creature?.collections.skills.map((skill) => (
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
    </div>
  );
}
