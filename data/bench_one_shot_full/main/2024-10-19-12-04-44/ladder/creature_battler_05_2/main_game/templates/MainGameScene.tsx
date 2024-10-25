import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  message?: string;
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent's creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          <img src="/images/opponent-creature.png" alt="Opponent's creature" className="w-40 h-40 object-contain" />
        </div>

        {/* Opponent's creature status */}
        <div className="col-start-1 row-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponent.entities.active_creature?.uid ?? ''}
            name={opponent.entities.active_creature?.display_name ?? 'Unknown'}
            image="/images/opponent-creature.png"
            hp={opponent.entities.active_creature?.stats.hp ?? 0}
            maxHp={opponent.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Player's creature */}
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          <img src="/images/player-creature.png" alt="Player's creature" className="w-40 h-40 object-contain" />
        </div>

        {/* Player's creature status */}
        <div className="col-start-2 row-start-2 flex justify-end items-end">
          <CreatureCard
            uid={player.entities.active_creature?.uid ?? ''}
            name={player.entities.active_creature?.display_name ?? 'Unknown'}
            image="/images/player-creature.png"
            hp={player.entities.active_creature?.stats.hp ?? 0}
            maxHp={player.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {props.data.message && (
          <div className="mb-4 text-center font-bold">{props.data.message}</div>
        )}
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && player.entities.active_creature?.collections.skills.slice(0, 4).map((skill, index) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" />
              {skill.display_name}
            </SkillButton>
          ))}
          {availableButtonSlugs.includes('back') && (
            <SkillButton
              uid="back-button"
              skillName="Back"
              description="Go back"
              stats="N/A"
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
              stats="N/A"
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
