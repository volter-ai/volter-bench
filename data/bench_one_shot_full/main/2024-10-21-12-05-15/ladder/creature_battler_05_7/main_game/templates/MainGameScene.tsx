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

  const playerCreature = props.data.entities.player?.entities.active_creature;
  const opponentCreature = props.data.entities.opponent?.entities.active_creature;

  return (
    <div className="flex flex-col h-screen w-screen bg-gray-100">
      {/* Battlefield (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent status */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image="/images/opponent.png"
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top-right: Opponent creature */}
        <div className="flex justify-end items-start">
          <img src="/images/opponent-front.png" alt="Opponent Creature" className="w-48 h-48 object-contain" />
        </div>

        {/* Bottom-left: Player creature */}
        <div className="flex justify-start items-end">
          <img src="/images/player-back.png" alt="Player Creature" className="w-48 h-48 object-contain" />
        </div>

        {/* Bottom-right: Player status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image="/images/player.png"
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface (lower 1/3) */}
      <div className="h-1/3 bg-white p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')} className="flex items-center justify-center">
              <Sword className="mr-2" />
              Attack
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')} className="flex items-center justify-center">
              <Repeat className="mr-2" />
              Swap
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')} className="flex items-center justify-center">
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill: Skill) => (
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

      {/* Player information */}
      <div className="absolute top-4 left-4">
        <PlayerCard
          uid={props.data.entities.player.uid}
          playerName={props.data.entities.player.display_name}
          imageUrl="/images/player-avatar.png"
        />
      </div>
    </div>
  );
}
