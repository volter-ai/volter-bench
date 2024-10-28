import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react'
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
  } = useCurrentButtons()

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = player?.entities.active_creature;
  const opponentCreature = opponent?.entities.active_creature;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl={`/images/players/${opponent.uid}.png`}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.uid}_front.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex justify-start items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.uid}_back.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Status */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              playerName={player.display_name}
              imageUrl={`/images/players/${player.uid}.png`}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.map((slug) => {
            if (slug === 'attack') {
              return (
                <Button key={slug} onClick={() => emitButtonClick(slug)} className="w-full h-full">
                  <Sword className="mr-2 h-4 w-4" /> Attack
                </Button>
              );
            } else if (slug === 'back') {
              return (
                <Button key={slug} onClick={() => emitButtonClick(slug)} className="w-full h-full">
                  <ArrowLeft className="mr-2 h-4 w-4" /> Back
                </Button>
              );
            } else if (slug === 'swap') {
              return (
                <Button key={slug} onClick={() => emitButtonClick(slug)} className="w-full h-full">
                  <Repeat className="mr-2 h-4 w-4" /> Swap
                </Button>
              );
            } else {
              const skill = playerCreature?.collections.skills.find(s => s.uid === slug);
              return skill ? (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  description={skill.description}
                  stats={`Base Damage: ${skill.stats.base_damage}`}
                  onClick={() => emitButtonClick(slug)}
                  className="w-full h-full"
                >
                  {skill.display_name}
                </SkillButton>
              ) : null;
            }
          })}
        </div>
      </div>
    </div>
  )
}
