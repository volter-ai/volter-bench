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
      <div className="flex-grow flex flex-col">
        <div className="flex justify-between h-2/3">
          {/* Opponent's creature and status */}
          <div className="w-1/2 flex flex-col items-end">
            {opponent.entities.active_creature && (
              <div className="flex flex-col items-center">
                <CreatureCard
                  uid={opponent.entities.active_creature.uid}
                  name={opponent.entities.active_creature.display_name}
                  image="/placeholder-opponent.png"
                  hp={opponent.entities.active_creature.stats.hp}
                  maxHp={opponent.entities.active_creature.stats.max_hp}
                />
              </div>
            )}
          </div>
          {/* Player's creature and status */}
          <div className="w-1/2 flex flex-col items-start">
            {player.entities.active_creature && (
              <div className="flex flex-col items-center">
                <CreatureCard
                  uid={player.entities.active_creature.uid}
                  name={player.entities.active_creature.display_name}
                  image="/placeholder-player.png"
                  hp={player.entities.active_creature.stats.hp}
                  maxHp={player.entities.active_creature.stats.max_hp}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              <Sword className="mr-2" />
              Attack
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <Repeat className="mr-2" />
              Swap
            </Button>
          )}
          {player.entities.active_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes(skill.uid) && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
              />
            )
          ))}
        </div>
      </div>
    </div>
  );
}
