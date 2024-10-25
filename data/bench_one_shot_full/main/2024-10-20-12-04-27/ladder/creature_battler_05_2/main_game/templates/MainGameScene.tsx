import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react'
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
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-0 pb-[56.25%] relative">
      <div className="absolute inset-0 flex flex-col">
        <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
          <div className="flex justify-start items-start">
            {opponent.entities.active_creature && (
              <CreatureCard
                uid={opponent.entities.active_creature.uid}
                name={opponent.entities.active_creature.display_name}
                image={`/images/creatures/${opponent.entities.active_creature.meta.creature_type}_front.png`}
                hp={opponent.entities.active_creature.stats.hp}
                maxHp={opponent.entities.active_creature.stats.max_hp}
              />
            )}
          </div>
          <div className="flex justify-end items-start">
            {/* Placeholder for potential future use */}
          </div>
          <div className="flex justify-start items-end">
            {/* Placeholder for potential future use */}
          </div>
          <div className="flex justify-end items-end">
            {player.entities.active_creature && (
              <CreatureCard
                uid={player.entities.active_creature.uid}
                name={player.entities.active_creature.display_name}
                image={`/images/creatures/${player.entities.active_creature.meta.creature_type}_back.png`}
                hp={player.entities.active_creature.stats.hp}
                maxHp={player.entities.active_creature.stats.max_hp}
              />
            )}
          </div>
        </div>
        <div className="h-1/3 bg-gray-100 p-4">
          <div className="grid grid-cols-2 grid-rows-2 gap-4">
            {availableButtonSlugs.includes('attack') && (
              <Button onClick={() => emitButtonClick('attack')} className="flex items-center justify-center">
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button onClick={() => emitButtonClick('swap')} className="flex items-center justify-center">
                <RefreshCw className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
            {player.entities.active_creature?.collections.skills.map((skill, index) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(availableButtonSlugs[index + 2])}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
