import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeftRight, ArrowLeft } from 'lucide-react';
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
  meta: {
    skill_type: string;
    is_physical: boolean;
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
    <div className="w-full h-full bg-gray-100 flex flex-col">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent Status */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image="/placeholder-opponent.png"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top-right: Opponent Creature */}
        <div className="flex justify-end items-start">
          <div className="w-48 h-48 bg-blue-200 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold">Opponent</span>
          </div>
        </div>

        {/* Bottom-left: Player Creature */}
        <div className="flex justify-start items-end">
          <div className="w-48 h-48 bg-green-200 rounded-full flex items-center justify-center">
            <span className="text-2xl font-bold">Player</span>
          </div>
        </div>

        {/* Bottom-right: Player Status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image="/placeholder-player.png"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4 flex flex-col">
        <div className="flex justify-between mb-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              <Sword className="mr-2" />
              Attack
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <ArrowLeftRight className="mr-2" />
              Swap
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
        </div>
        <div className="flex-grow overflow-y-auto">
          <h3 className="text-lg font-semibold mb-2">Skills</h3>
          <div className="grid grid-cols-2 gap-2">
            {playerCreature?.collections.skills.map((skill: Skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}, Physical: ${skill.meta.is_physical}`}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
