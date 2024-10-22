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
    <div className="h-screen w-screen flex flex-col">
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4" style={{ height: '66.67%' }}>
        <div className="flex justify-end items-start">
          {opponentCreature && (
            <div className="text-right">
              <h3 className="text-xl font-bold">{opponentCreature.display_name}</h3>
              <p>HP: {opponentCreature.stats.hp} / {opponentCreature.stats.max_hp}</p>
            </div>
          )}
        </div>
        <div className="flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image="/path/to/opponent-creature-front-image.png"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="flex justify-start items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image="/path/to/player-creature-back-image.png"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
        <div className="flex justify-start items-end">
          {playerCreature && (
            <div className="text-left">
              <h3 className="text-xl font-bold">{playerCreature.display_name}</h3>
              <p>HP: {playerCreature.stats.hp} / {playerCreature.stats.max_hp}</p>
            </div>
          )}
        </div>
      </div>
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack"
              skillName="Attack"
              description="Perform an attack"
              stats=""
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" /> Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back"
              skillName="Back"
              description="Go back"
              stats=""
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2" /> Back
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap"
              skillName="Swap"
              description="Swap creatures"
              stats=""
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
