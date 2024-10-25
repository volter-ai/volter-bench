import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
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
  collections: {
    skills: Skill[];
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

interface Player {
  uid: string;
  display_name: string;
  entities: {
    active_creature: Creature;
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

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4">
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          {opponentCreature && (
            <img 
              src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`} 
              alt={opponentCreature.display_name} 
              className="w-64 h-64 object-contain"
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          {playerCreature && (
            <img 
              src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`} 
              alt={playerCreature.display_name} 
              className="w-64 h-64 object-contain"
            />
          )}
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.creature_type}.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              description="Attack the opponent"
              stats="Damage varies"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2 h-4 w-4" />
              Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')} className="h-full">
              <Repeat className="mr-2 h-4 w-4" />
              Swap Creature
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')} className="h-full">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
