import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

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

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  if (!playerCreature || !opponentCreature) {
    return <div>Loading...</div>;
  }

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow flex">
        {/* Opponent Creature */}
        <div className="w-1/2 flex flex-col items-center justify-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="transform scale-x-[-1]"
          />
        </div>
        {/* Player Creature */}
        <div className="w-1/2 flex flex-col items-center justify-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack"
              skillName="Attack"
              description="Perform a basic attack"
              stats="Damage: Base"
            >
              <Sword className="mr-2" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back"
              skillName="Back"
              description="Go back to the previous screen"
              stats=""
            >
              <ArrowLeft className="mr-2" /> Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap"
              skillName="Swap"
              description="Swap your active creature"
              stats=""
            >
              <Repeat className="mr-2" /> Swap
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  );
}
