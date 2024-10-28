import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  uid: string;
  display_name: string;
  entities: {
    active_creature?: Creature;
  };
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full bg-gray-100 flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          {opponent.entities.active_creature && (
            <CreatureCard
              uid={opponent.entities.active_creature.uid}
              name={opponent.entities.active_creature.display_name}
              imageUrl={`/creatures/${opponent.entities.active_creature.uid}.png`}
              hp={opponent.entities.active_creature.stats.hp}
              maxHp={opponent.entities.active_creature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex items-start justify-end">
          {opponent.entities.active_creature && (
            <img 
              src={`/creatures/${opponent.entities.active_creature.uid}.png`} 
              alt={opponent.entities.active_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex items-end justify-start">
          {player.entities.active_creature && (
            <img 
              src={`/creatures/${player.entities.active_creature.uid}_back.png`} 
              alt={player.entities.active_creature.display_name}
              className="w-48 h-48 object-contain"
            />
          )}
        </div>

        {/* Player Creature Status */}
        <div className="row-start-2 col-start-2 flex items-end justify-end">
          {player.entities.active_creature && (
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              imageUrl={`/creatures/${player.entities.active_creature.uid}.png`}
              hp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4 flex flex-col justify-between">
        <div className="flex space-x-4 mb-4">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              skillName="Attack"
              description="Perform an attack"
              stats="Basic attack"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" />
              Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back-button"
              skillName="Back"
              description="Go back"
              stats="Navigation"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2" />
              Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap-button"
              skillName="Swap"
              description="Swap creatures"
              stats="Change active creature"
              onClick={() => emitButtonClick('swap')}
            >
              <Repeat className="mr-2" />
              Swap
            </SkillButton>
          )}
        </div>
        <div className="flex flex-wrap">
          {player.entities.active_creature?.collections.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              className="mr-2 mb-2"
            />
          ))}
        </div>
      </div>
    </div>
  );
}
