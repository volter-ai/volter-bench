import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, Repeat } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
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
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent status */}
        <div className="flex justify-start items-start">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              image={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
              hp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top-right: Opponent creature */}
        <div className="flex justify-end items-start">
          {opponentCreature && (
            <img
              src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
              alt={opponentCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          )}
        </div>

        {/* Bottom-left: Player creature */}
        <div className="flex justify-start items-end">
          {playerCreature && (
            <img
              src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
              alt={playerCreature.display_name}
              className="w-48 h-48 object-contain"
            />
          )}
        </div>

        {/* Bottom-right: Player status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/images/creatures/${playerCreature.meta.creature_type}.png`}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface (lower 1/3) */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills[0] && (
            <SkillButton
              uid={playerCreature.collections.skills[0].uid}
              skillName={playerCreature.collections.skills[0].display_name}
              description={playerCreature.collections.skills[0].description}
              stats={`Damage: ${playerCreature.collections.skills[0].stats.base_damage}`}
              onClick={() => emitButtonClick('attack')}
            >
              <Sword className="mr-2" /> {playerCreature.collections.skills[0].display_name}
            </SkillButton>
          )}
          {availableButtonSlugs.includes('swap') && (
            <Button uid={`${props.data.entities.player.uid}-swap`} onClick={() => emitButtonClick('swap')}>
              <Repeat className="mr-2" /> Swap Creature
            </Button>
          )}
          {availableButtonSlugs.includes('back') && (
            <Button uid={`${props.data.entities.player.uid}-back`} onClick={() => emitButtonClick('back')}>
              <ArrowLeft className="mr-2" /> Back
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
