import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <img 
            src={`/creatures/${opponent.entities.active_creature?.uid ?? 'unknown'}_front.png`}
            alt={opponent.entities.active_creature?.display_name ?? 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponent.entities.active_creature?.uid ?? ''}
            name={opponent.entities.active_creature?.display_name ?? 'Unknown'}
            image={`/creatures/${opponent.entities.active_creature?.uid ?? 'unknown'}.png`}
            hp={opponent.entities.active_creature?.stats.hp ?? 0}
            maxHp={opponent.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Player Creature Status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          <CreatureCard
            uid={player.entities.active_creature?.uid ?? ''}
            name={player.entities.active_creature?.display_name ?? 'Unknown'}
            image={`/creatures/${player.entities.active_creature?.uid ?? 'unknown'}.png`}
            hp={player.entities.active_creature?.stats.hp ?? 0}
            maxHp={player.entities.active_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          <img 
            src={`/creatures/${player.entities.active_creature?.uid ?? 'unknown'}_back.png`}
            alt={player.entities.active_creature?.display_name ?? 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-3 gap-4 h-full">
          <PlayerCard
            uid={player.uid}
            playerName={player.display_name}
            imageUrl={`/players/${player.uid}.png`}
          />
          <div className="col-span-2 grid grid-cols-2 grid-rows-2 gap-2">
            {availableButtonSlugs.includes('attack') && (
              <Button onClick={() => emitButtonClick('attack')}>
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
            {player.entities.active_creature?.collections.skills?.map((skill) => (
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
    </div>
  );
}
