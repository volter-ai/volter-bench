import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react'
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
  } = useCurrentButtons()

  const player = props.data.entities.player;
  const opponent = props.data.entities.opponent;

  return (
    <div className="w-full h-full bg-gray-100 flex flex-col">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent Creature */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponent?.entities.active_creature?.uid || ''}
            name={opponent?.entities.active_creature?.display_name || 'Unknown'}
            image={`/images/creatures/${opponent?.entities.active_creature?.meta.creature_type}_front.png`}
            hp={opponent?.entities.active_creature?.stats.hp || 0}
            maxHp={opponent?.entities.active_creature?.stats.max_hp || 1}
          />
        </div>

        {/* Top-right: Opponent Status */}
        <div className="flex justify-end items-start">
          <PlayerCard
            uid={opponent?.uid || ''}
            playerName={opponent?.display_name || 'Unknown'}
            imageUrl={`/images/players/${opponent?.uid}.png`}
          />
        </div>

        {/* Bottom-left: Player Creature */}
        <div className="flex justify-start items-end">
          <CreatureCard
            uid={player?.entities.active_creature?.uid || ''}
            name={player?.entities.active_creature?.display_name || 'Unknown'}
            image={`/images/creatures/${player?.entities.active_creature?.meta.creature_type}_back.png`}
            hp={player?.entities.active_creature?.stats.hp || 0}
            maxHp={player?.entities.active_creature?.stats.max_hp || 1}
          />
        </div>

        {/* Bottom-right: Player Status */}
        <div className="flex justify-end items-end">
          <PlayerCard
            uid={player?.uid || ''}
            playerName={player?.display_name || 'Unknown'}
            imageUrl={`/images/players/${player?.uid}.png`}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.includes('attack') && (
            <Button onClick={() => emitButtonClick('attack')}>
              <Sword className="mr-2" />
              Attack
            </Button>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button onClick={() => emitButtonClick('swap')}>
              <Repeat className="mr-2" />
              Swap
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2" />
              Back
            </Button>
          )}
          {player?.entities.active_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
            >
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  )
}
