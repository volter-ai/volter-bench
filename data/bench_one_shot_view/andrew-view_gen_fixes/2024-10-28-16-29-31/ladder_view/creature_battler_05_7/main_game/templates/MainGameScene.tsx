import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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
  } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = player?.entities.active_creature;
  const opponentCreature = opponent?.entities.active_creature;

  return (
    <div className="w-full h-full" style={{ aspectRatio: '16/9' }}>
      <div className="flex flex-col h-full">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
          {/* Top-left: Opponent Status */}
          <div className="flex justify-start items-start">
            {opponentCreature && (
              <CreatureCard
                uid={`opponent-creature-${opponentCreature.uid}`}
                name={opponentCreature.display_name}
                image="/placeholder-opponent-front.png"
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            )}
          </div>

          {/* Top-right: Opponent Creature */}
          <div className="flex justify-end items-start">
            {opponent && (
              <PlayerCard
                uid={`opponent-${opponent.uid}`}
                playerName={opponent.display_name}
                imageUrl="/placeholder-opponent.png"
              />
            )}
          </div>

          {/* Bottom-left: Player Creature */}
          <div className="flex justify-start items-end">
            {player && (
              <PlayerCard
                uid={`player-${player.uid}`}
                playerName={player.display_name}
                imageUrl="/placeholder-player.png"
              />
            )}
          </div>

          {/* Bottom-right: Player Status */}
          <div className="flex justify-end items-end">
            {playerCreature && (
              <CreatureCard
                uid={`player-creature-${playerCreature.uid}`}
                name={playerCreature.display_name}
                image="/placeholder-player-back.png"
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 bg-gray-100 p-4">
          <div className="flex flex-wrap gap-2 mb-4">
            {availableButtonSlugs.includes('attack') && (
              <Button onClick={() => emitButtonClick('attack')}>
                <Sword className="mr-2 h-4 w-4" /> Attack
              </Button>
            )}
            {availableButtonSlugs.includes('back') && (
              <Button onClick={() => emitButtonClick('back')}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Back
              </Button>
            )}
            {availableButtonSlugs.includes('swap') && (
              <Button onClick={() => emitButtonClick('swap')}>
                <Repeat className="mr-2 h-4 w-4" /> Swap
              </Button>
            )}
          </div>
          <div className="flex flex-wrap gap-2">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={`skill-${skill.uid}`}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Base Damage: ${skill.stats.base_damage}`}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
