import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard, Progress } from "@/components/ui/custom/creature/creature_card";
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

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          <img
            src="/placeholder-opponent-creature.png"
            alt="Opponent Creature"
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Opponent Creature Status */}
        <div className="col-start-2 row-start-1 flex justify-start items-start">
          {opponent.entities.active_creature && (
            <CreatureCard
              uid={opponent.entities.active_creature.uid}
              name={opponent.entities.active_creature.display_name}
              image="/placeholder-opponent.png"
              hp={opponent.entities.active_creature.stats.hp}
              maxHp={opponent.entities.active_creature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          <img
            src="/placeholder-player-creature.png"
            alt="Player Creature"
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="col-start-1 row-start-2 flex justify-end items-end">
          {player.entities.active_creature && (
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              image="/placeholder-player.png"
              hp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && player.entities.active_creature?.collections.skills[0] && (
            <SkillButton
              uid={player.entities.active_creature.collections.skills[0].uid}
              skillName="Attack"
              description="Choose an attack"
              stats={`Base Damage: ${player.entities.active_creature.collections.skills[0].stats.base_damage}`}
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
              stats=""
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
              stats=""
              onClick={() => emitButtonClick('swap')}
            >
              <Repeat className="mr-2" />
              Swap
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  );
}
