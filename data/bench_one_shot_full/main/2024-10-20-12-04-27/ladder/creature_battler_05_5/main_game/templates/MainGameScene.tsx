import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, ArrowLeft, RotateCcw, X, Repeat } from 'lucide-react';

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
  collections: {
    creatures: Creature[];
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player.collections.creatures[0];
  const opponentCreature = props.data.entities.opponent.collections.creatures[0];

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex justify-start items-start">
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
        <div className="flex justify-end items-start">
          <div className="w-48 h-48 bg-gray-200 rounded-full flex items-center justify-center">
            {opponentCreature && (
              <img
                src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
                alt={opponentCreature.display_name}
                className="w-40 h-40 object-contain"
              />
            )}
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <div className="w-48 h-48 bg-gray-200 rounded-full flex items-center justify-center">
            {playerCreature && (
              <img
                src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
                alt={playerCreature.display_name}
                className="w-40 h-40 object-contain"
              />
            )}
          </div>
        </div>

        {/* Player Status */}
        <div className="flex justify-end items-end">
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
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              skillName="Attack"
              description="Perform a basic attack"
              stats="Damage varies"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back-button"
              skillName="Back"
              description="Go back to the previous screen"
              stats="N/A"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2" /> Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes('play-again') && (
            <SkillButton
              uid="play-again-button"
              skillName="Play Again"
              description="Start a new game"
              stats="N/A"
              onClick={() => emitButtonClick('play-again')}
            >
              <RotateCcw className="mr-2" /> Play Again
            </SkillButton>
          )}
          {availableButtonSlugs.includes('quit') && (
            <SkillButton
              uid="quit-button"
              skillName="Quit"
              description="Exit the game"
              stats="N/A"
              onClick={() => emitButtonClick('quit')}
            >
              <X className="mr-2" /> Quit
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap-button"
              skillName="Swap"
              description="Switch to another creature"
              stats="N/A"
              onClick={() => emitButtonClick('swap')}
            >
              <Repeat className="mr-2" /> Swap
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  );
}
