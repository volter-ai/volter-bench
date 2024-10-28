import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";

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
  meta: {
    creature_type: string;
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

  const getCreatureImage = (creature: Creature) => {
    return `/images/creatures/${creature.meta.creature_type.toLowerCase()}_${creature.display_name.toLowerCase()}.png`;
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex justify-start items-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl="/images/opponent_avatar.png"
              className="transform scale-75 origin-top-left"
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={getCreatureImage(opponentCreature)}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              className="transform scale-90 origin-top-right"
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={getCreatureImage(playerCreature)}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              className="transform scale-90 origin-bottom-left"
            />
          )}
        </div>

        {/* Player Status */}
        <div className="flex justify-end items-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              playerName={player.display_name}
              imageUrl="/images/player_avatar.png"
              className="transform scale-75 origin-bottom-right"
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4 flex flex-col justify-center items-center">
        <div className="flex space-x-4">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick('attack')}
              disabled={!availableButtonSlugs.includes('attack')}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
          {availableButtonSlugs.includes('swap') && (
            <SkillButton
              uid="swap-button"
              skillName="Swap"
              description="Swap your active creature"
              stats=""
              onClick={() => emitButtonClick('swap')}
            >
              <Repeat className="mr-2 h-4 w-4" />
              Swap
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  );
}
