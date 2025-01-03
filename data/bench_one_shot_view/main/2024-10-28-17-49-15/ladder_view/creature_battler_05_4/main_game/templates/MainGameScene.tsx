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
  stats: {
    hp: number;
    max_hp: number;
  };
  collections?: {
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
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4 bg-gray-100">
        {/* Opponent Status */}
        <div className="col-start-1 row-start-1 flex items-center justify-center">
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

        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex items-center justify-center">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl="/placeholder-opponent.png"
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex items-center justify-center">
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

        {/* Player Status */}
        <div className="col-start-2 row-start-2 flex items-center justify-center">
          {player && (
            <PlayerCard
              uid={player.uid}
              playerName={player.display_name}
              imageUrl="/placeholder-player.png"
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4 flex flex-col items-center justify-center">
        <div className="flex space-x-4 mb-4">
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
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.display_name.toLowerCase())}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
