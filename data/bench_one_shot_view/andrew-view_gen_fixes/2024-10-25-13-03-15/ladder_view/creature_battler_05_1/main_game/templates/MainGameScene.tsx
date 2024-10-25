import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Button } from "@/components/ui/button";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string; is_physical: boolean };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  entities: {
    active_creature: Creature;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;
  const playerCreature = player?.entities.active_creature;
  const opponentCreature = opponent?.entities.active_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4" style={{ height: '66.67%' }}>
        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex items-start justify-end">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.prototype_id}_front.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Status */}
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl={`/images/players/${opponent.uid}.png`}
            />
          )}
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex items-end justify-start">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.prototype_id}_back.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Player Status */}
        <div className="row-start-2 col-start-2 flex items-end justify-end">
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
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && (
            <SkillButton
              uid="attack-button"
              description="Attack the opponent"
              stats="Damage varies"
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" />
              Attack
            </SkillButton>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <Repeat className="mr-2" />
              Swap
            </Button>
          )}
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick(skill.uid)}
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
