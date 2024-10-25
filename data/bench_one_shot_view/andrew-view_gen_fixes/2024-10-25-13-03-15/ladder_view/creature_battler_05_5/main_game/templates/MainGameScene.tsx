import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react'
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
  } = useCurrentButtons()

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponent.entities.active_creature?.uid ?? ''}
            name={opponent.entities.active_creature?.display_name ?? 'Unknown'}
            image="/placeholder.png"
            hp={opponent.entities.active_creature?.stats.hp ?? 0}
            maxHp={opponent.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <div className="w-48 h-48 bg-blue-200 rounded-full flex items-center justify-center">
            Opponent Creature
          </div>
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          <div className="w-48 h-48 bg-green-200 rounded-full flex items-center justify-center">
            Player Creature
          </div>
        </div>

        {/* Player Status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          <CreatureCard
            uid={player.entities.active_creature?.uid ?? ''}
            name={player.entities.active_creature?.display_name ?? 'Unknown'}
            image="/placeholder.png"
            hp={player.entities.active_creature?.stats.hp ?? 0}
            maxHp={player.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              description="Attack the opponent"
              stats="Damage varies"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2 h-4 w-4" />
              Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <Repeat className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}
          {player.entities.active_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  )
}
