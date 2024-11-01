import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Sword, RefreshCw } from 'lucide-react';

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
  skills: Skill[];
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
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="col-start-1 row-start-1 flex justify-start items-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl="/placeholder-opponent.png"
            />
          )}
        </div>
        
        {/* Opponent Creature */}
        <div className="col-start-2 row-start-1 flex justify-end items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/creatures/${opponentCreature.uid}.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>
        
        {/* Player Creature */}
        <div className="col-start-1 row-start-2 flex justify-start items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/creatures/${playerCreature.uid}.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
        
        {/* Player Status */}
        <div className="col-start-2 row-start-2 flex justify-end items-end">
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
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.map((slug, index) => {
            if (slug === 'attack') {
              return (
                <SkillButton
                  key={slug}
                  uid="attack-button"
                  skillName="Attack"
                  description="Perform a basic attack"
                  stats="Damage: 5"
                  onClick={() => emitButtonClick('attack')}
                >
                  <Sword className="mr-2" />
                  Attack
                </SkillButton>
              );
            } else if (slug === 'swap') {
              return (
                <SkillButton
                  key={slug}
                  uid="swap-button"
                  skillName="Swap"
                  description="Swap your active creature"
                  stats="Cost: 1 turn"
                  onClick={() => emitButtonClick('swap')}
                >
                  <RefreshCw className="mr-2" />
                  Swap
                </SkillButton>
              );
            } else {
              const skill = playerCreature?.skills.find(s => s.uid === slug);
              if (skill) {
                return (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    skillName={skill.display_name}
                    description={skill.description}
                    stats={`Damage: ${skill.stats.base_damage}`}
                    onClick={() => emitButtonClick(slug)}
                  />
                );
              }
            }
            return null;
          })}
        </div>
      </div>
    </div>
  );
}
