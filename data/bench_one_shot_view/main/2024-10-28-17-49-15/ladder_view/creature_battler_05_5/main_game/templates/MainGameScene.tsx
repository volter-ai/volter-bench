import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

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
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
        {/* Battlefield Display */}
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {/* Opponent Creature */}
          <div className="row-start-1 col-start-2 flex items-center justify-center">
            {opponentCreature && (
              <img src={`/creatures/${opponentCreature.uid}.png`} alt={opponentCreature.display_name} className="w-32 h-32 object-contain" />
            )}
          </div>
          
          {/* Opponent Status */}
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/creatures/${opponentCreature.uid}.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>
          
          {/* Player Status */}
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/creatures/${playerCreature.uid}.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
          
          {/* Player Creature */}
          <div className="row-start-2 col-start-1 flex items-center justify-center">
            {playerCreature && (
              <img src={`/creatures/${playerCreature.uid}.png`} alt={playerCreature.display_name} className="w-32 h-32 object-contain" />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-200 p-4 flex flex-col justify-center">
          <div className="flex justify-center space-x-4">
            {availableButtonSlugs.includes('attack') && (
              <Button onClick={() => emitButtonClick('attack')}>
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button onClick={() => emitButtonClick('swap')}>
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button onClick={() => emitButtonClick('back')}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
          </div>
          {playerCreature && (
            <div className="mt-4 flex justify-center space-x-2">
              {playerCreature.collections.skills.map((skill) => (
                availableButtonSlugs.includes(skill.uid) && (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    skillName={skill.display_name}
                    description={skill.description}
                    stats={`Base Damage: ${skill.stats.base_damage}`}
                    onClick={() => emitButtonClick(skill.uid)}
                  />
                )
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
