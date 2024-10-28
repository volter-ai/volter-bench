import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = player?.entities.active_creature;
  const opponentCreature = opponent?.entities.active_creature;

  return (
    <div className="h-screen w-screen flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent Status */}
        <div className="flex justify-start items-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl="/placeholder-opponent.png"
            />
          )}
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image="/placeholder-opponent-creature.png"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top-right: Opponent Creature */}
        <div className="flex justify-end items-start">
          <div className="w-48 h-48 bg-gray-200 rounded-full flex items-center justify-center">
            {/* Placeholder for opponent creature image */}
            <span className="text-4xl">🐉</span>
          </div>
        </div>

        {/* Bottom-left: Player Creature */}
        <div className="flex justify-start items-end">
          <div className="w-48 h-48 bg-gray-200 rounded-full flex items-center justify-center">
            {/* Placeholder for player creature image */}
            <span className="text-4xl">🦁</span>
          </div>
        </div>

        {/* Bottom-right: Player Status */}
        <div className="flex justify-end items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              playerName={player.display_name}
              imageUrl="/placeholder-player.png"
            />
          )}
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image="/placeholder-player-creature.png"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4 flex flex-col justify-center items-center">
        <div className="grid grid-cols-2 gap-4 mb-4">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!availableButtonSlugs.includes('attack')}
              onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
            />
          ))}
        </div>
        <div className="flex space-x-4">
          <Button
            onClick={() => emitButtonClick('attack')}
            disabled={!availableButtonSlugs.includes('attack')}
          >
            <Sword className="mr-2 h-4 w-4" /> Attack
          </Button>
          <Button
            onClick={() => emitButtonClick('swap')}
            disabled={!availableButtonSlugs.includes('swap')}
          >
            <Repeat className="mr-2 h-4 w-4" /> Swap
          </Button>
          <Button
            onClick={() => emitButtonClick('back')}
            disabled={!availableButtonSlugs.includes('back')}
          >
            <ArrowLeft className="mr-2 h-4 w-4" /> Back
          </Button>
        </div>
      </div>
    </div>
  );
}
