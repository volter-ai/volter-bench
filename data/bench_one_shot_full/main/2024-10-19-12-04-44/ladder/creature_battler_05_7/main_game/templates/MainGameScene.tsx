import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { Button } from "@/components/ui/button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
  };
}

interface Player {
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
  stats: {
    turn_counter: number;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, opponent } = props.data.entities;

  return (
    <div className="w-full h-full flex items-center justify-center">
      <div className="w-full aspect-video bg-gray-100 flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Top-left: Opponent Status */}
          <div className="flex items-start justify-start">
            <CreatureCard
              uid={opponent.entities.active_creature.uid}
              name={opponent.entities.active_creature.display_name}
              image={`/images/creatures/${opponent.entities.active_creature.meta.creature_type}.png`}
              hp={opponent.entities.active_creature.stats.hp}
              maxHp={opponent.entities.active_creature.stats.max_hp}
            />
          </div>

          {/* Top-right: Opponent Creature */}
          <div className="flex items-end justify-end">
            <img
              src={`/images/creatures/${opponent.entities.active_creature.meta.creature_type}_front.png`}
              alt={opponent.entities.active_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>

          {/* Bottom-left: Player Creature */}
          <div className="flex items-start justify-start">
            <img
              src={`/images/creatures/${player.entities.active_creature.meta.creature_type}_back.png`}
              alt={player.entities.active_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          </div>

          {/* Bottom-right: Player Status */}
          <div className="flex items-end justify-end">
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              image={`/images/creatures/${player.entities.active_creature.meta.creature_type}.png`}
              hp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4">
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.includes('attack') && (
              <Button uid="attack-button" onClick={() => emitButtonClick('attack')}>
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button uid="back-button" onClick={() => emitButtonClick('back')}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button uid="swap-button" onClick={() => emitButtonClick('swap')}>
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
            {player.entities.active_creature.collections?.skills?.map((skill: Skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
