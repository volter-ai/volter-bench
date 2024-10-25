import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Button } from "@/components/ui/button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
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
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4" style={{ height: '66.67%' }}>
        {/* Opponent Status */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          <CreatureCard
            uid={opponent.entities.active_creature?.uid || ''}
            name={opponent.entities.active_creature?.display_name || 'Unknown'}
            image={`/images/creatures/${opponent.entities.active_creature?.meta.creature_type || 'unknown'}.png`}
            hp={opponent.entities.active_creature?.stats.hp || 0}
            maxHp={opponent.entities.active_creature?.stats.max_hp || 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          <img
            src={`/images/creatures/${opponent.entities.active_creature?.meta.creature_type || 'unknown'}_front.png`}
            alt={opponent.entities.active_creature?.display_name || 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          <img
            src={`/images/creatures/${player.entities.active_creature?.meta.creature_type || 'unknown'}_back.png`}
            alt={player.entities.active_creature?.display_name || 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Status */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          <CreatureCard
            uid={player.entities.active_creature?.uid || ''}
            name={player.entities.active_creature?.display_name || 'Unknown'}
            image={`/images/creatures/${player.entities.active_creature?.meta.creature_type || 'unknown'}.png`}
            hp={player.entities.active_creature?.stats.hp || 0}
            maxHp={player.entities.active_creature?.stats.max_hp || 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 gap-4">
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
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>

      {/* Player Information */}
      <div className="absolute top-4 left-4">
        <PlayerCard
          uid={player.uid}
          playerName={player.display_name}
          imageUrl={`/images/players/${player.uid}.png`}
        />
      </div>

      {/* Opponent Information */}
      <div className="absolute top-4 right-4">
        <PlayerCard
          uid={opponent.uid}
          playerName={opponent.display_name}
          imageUrl={`/images/players/${opponent.uid}.png`}
        />
      </div>
    </div>
  );
}
