import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, RefreshCw } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
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
  } = useCurrentButtons()

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-200 to-green-200 flex flex-col">
      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponent.entities.active_creature.uid}
            name={opponent.entities.active_creature.display_name}
            image="/placeholder-opponent.png"
            hp={opponent.entities.active_creature.stats.hp}
            maxHp={opponent.entities.active_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          <img
            src="/placeholder-opponent-creature.png"
            alt="Opponent Creature"
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <img
            src="/placeholder-player-creature.png"
            alt="Player Creature"
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={player.entities.active_creature.uid}
            name={player.entities.active_creature.display_name}
            image="/placeholder-player.png"
            hp={player.entities.active_creature.stats.hp}
            maxHp={player.entities.active_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-800 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')} className="flex items-center justify-center">
              <Sword className="mr-2" />
              Attack
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')} className="flex items-center justify-center">
              <RefreshCw className="mr-2" />
              Swap
            </Button>
          )}
          {player.entities.active_creature.collections.skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
