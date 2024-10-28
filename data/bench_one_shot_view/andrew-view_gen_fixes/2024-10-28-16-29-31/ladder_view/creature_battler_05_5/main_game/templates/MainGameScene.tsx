import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="w-full h-full" style={{ aspectRatio: '16/9' }}>
      <div className="flex flex-col h-full">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {/* Top-left: Opponent's creature status */}
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

          {/* Top-right: Opponent's creature */}
          <div className="row-start-1 col-start-2 flex items-end justify-center">
            {opponentCreature && (
              <img
                src={`/creatures/${opponentCreature.uid}.png`}
                alt={opponentCreature.display_name}
                className="w-64 h-64 object-contain"
              />
            )}
          </div>

          {/* Bottom-left: Player's creature */}
          <div className="row-start-2 col-start-1 flex items-start justify-center">
            {playerCreature && (
              <img
                src={`/creatures/${playerCreature.uid}_back.png`}
                alt={playerCreature.display_name}
                className="w-64 h-64 object-contain"
              />
            )}
          </div>

          {/* Bottom-right: Player's creature status */}
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
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-100 p-4 flex flex-col space-y-4">
          <div className="flex justify-center space-x-4">
            {availableButtonSlugs.includes('attack') && (
              <Button className="text-lg px-6 py-3" onClick={() => emitButtonClick('attack')}>
                <Sword className="mr-2 h-6 w-6" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button className="text-lg px-6 py-3" onClick={() => emitButtonClick('swap')}>
                <Repeat className="mr-2 h-6 w-6" /> Swap
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button className="text-lg px-6 py-3" onClick={() => emitButtonClick('back')}>
                <ArrowLeft className="mr-2 h-6 w-6" /> Back
              </Button>
            )}
          </div>
          <div className="flex justify-center space-x-4 overflow-x-auto">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => {
                  if (availableButtonSlugs.includes(skill.uid)) {
                    emitButtonClick(skill.uid);
                  }
                }}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
