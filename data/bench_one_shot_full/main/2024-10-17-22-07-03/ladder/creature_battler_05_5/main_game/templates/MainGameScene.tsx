import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { CreatureCard, Progress } from "@/components/ui/custom/creature/creature_card";
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
  meta: {
    image_url?: string;
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  const renderCreatureStatus = (creature: Creature, isPlayer: boolean) => (
    <div className={`flex flex-col ${isPlayer ? 'items-end' : 'items-start'}`}>
      <h2 className="text-xl font-bold">{creature.display_name}</h2>
      <Progress
        value={(creature.stats.hp / creature.stats.max_hp) * 100}
        className="w-48"
        uid={`${creature.uid}-progress`}
      />
      <p className="text-sm">
        HP: {creature.stats.hp}/{creature.stats.max_hp}
      </p>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      <div className="flex-grow grid grid-cols-2 grid-rows-2 bg-gradient-to-b from-blue-200 to-green-200">
        {/* Opponent Status */}
        <div className="p-4">
          {opponent.entities.active_creature && renderCreatureStatus(opponent.entities.active_creature, false)}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          {opponent.entities.active_creature && (
            <CreatureCard
              uid={opponent.entities.active_creature.uid}
              name={opponent.entities.active_creature.display_name}
              image={opponent.entities.active_creature.meta.image_url || '/placeholder-opponent.png'}
              hp={opponent.entities.active_creature.stats.hp}
              maxHp={opponent.entities.active_creature.stats.max_hp}
              className="transform scale-x-[-1]"
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          {player.entities.active_creature && (
            <CreatureCard
              uid={player.entities.active_creature.uid}
              name={player.entities.active_creature.display_name}
              image={player.entities.active_creature.meta.image_url || '/placeholder-player.png'}
              hp={player.entities.active_creature.stats.hp}
              maxHp={player.entities.active_creature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Status */}
        <div className="p-4">
          {player.entities.active_creature && renderCreatureStatus(player.entities.active_creature, true)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button 
              onClick={() => emitButtonClick('attack')} 
              className="flex items-center justify-center"
              uid="attack-button"
            >
              <Sword className="mr-2" /> Attack
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button 
              onClick={() => emitButtonClick('back')} 
              className="flex items-center justify-center"
              uid="back-button"
            >
              <ArrowLeft className="mr-2" /> Back
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button 
              onClick={() => emitButtonClick('swap')} 
              className="flex items-center justify-center"
              uid="swap-button"
            >
              <Repeat className="mr-2" /> Swap
            </Button>
          )}
          {player.entities.active_creature?.collections.skills.map((skill) => (
            enabledUIDs.includes(skill.uid) && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
              />
            )
          ))}
        </div>
      </div>
    </div>
  );
}
