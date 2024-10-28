import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
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
  __type: "Player";
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
    <div className="w-full h-full bg-gray-200" style={{ aspectRatio: '16/9' }}>
      <div className="flex flex-col h-full">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {/* Top-left: Opponent Creature */}
          <div className="flex justify-start items-start">
            {opponentCreature && (
              <img
                src={`/creatures/${opponentCreature.display_name.toLowerCase()}.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>

          {/* Top-right: Opponent Status */}
          <div className="flex justify-end items-start">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/creatures/${opponentCreature.display_name.toLowerCase()}.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>

          {/* Bottom-left: Player Status */}
          <div className="flex justify-start items-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>

          {/* Bottom-right: Player Creature */}
          <div className="flex justify-end items-end">
            {playerCreature && (
              <img
                src={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-100 p-4">
          <div className="flex space-x-4 mb-4">
            {availableButtonSlugs.includes('attack') && (
              <Button onClick={() => emitButtonClick('attack')} className="w-24 h-12">
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button onClick={() => emitButtonClick('swap')} className="w-24 h-12">
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button onClick={() => emitButtonClick('back')} className="w-24 h-12">
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
          </div>

          {/* Skills */}
          <div className="flex flex-wrap gap-2">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
                className="w-32 h-16 text-sm"
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
