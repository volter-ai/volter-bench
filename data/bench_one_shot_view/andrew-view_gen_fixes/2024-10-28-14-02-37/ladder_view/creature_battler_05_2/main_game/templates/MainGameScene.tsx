import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { useState } from 'react';

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
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const [showSkills, setShowSkills] = useState(false);

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  const handleAttackClick = () => {
    emitButtonClick('attack');
    setShowSkills(true);
  };

  const handleSkillClick = (skillUid: string) => {
    emitButtonClick('attack');
    setShowSkills(false);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow flex flex-col" style={{ height: '66.67%' }}>
        <div className="flex-1 grid grid-cols-2 grid-rows-2 gap-4 p-4">
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
              <div className="w-32 h-32 bg-contain bg-center bg-no-repeat" style={{backgroundImage: `url(/images/creatures/${opponentCreature.meta.creature_type}_front.png)`}}></div>
            )}
          </div>

          {/* Player Creature */}
          <div className="col-start-1 row-start-2 flex justify-start items-end">
            {playerCreature && (
              <div className="w-32 h-32 bg-contain bg-center bg-no-repeat" style={{backgroundImage: `url(/images/creatures/${playerCreature.meta.creature_type}_back.png)`}}></div>
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
      </div>

      {/* User Interface */}
      <div className="bg-white p-4" style={{ height: '33.33%' }}>
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {!showSkills && (
            <>
              {availableButtonSlugs.includes('attack') && (
                <Button onClick={handleAttackClick}>
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
            </>
          )}
          {showSkills && playerCreature?.collections.skills.map((skill, index) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              onClick={() => handleSkillClick(skill.uid)}
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
