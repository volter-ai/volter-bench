import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { MessageSquare } from 'lucide-react';

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
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4" style={{ height: '66.67%' }}>
        {/* Opponent Creature Status */}
        <div className="col-start-1 row-start-1 flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature?.uid ?? ''}
            name={opponentCreature?.display_name ?? 'Unknown'}
            image={`/images/creatures/${opponentCreature?.meta.creature_type ?? 'unknown'}_front.png`}
            hp={opponentCreature?.stats.hp ?? 0}
            maxHp={opponentCreature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="col-start-1 row-start-1 flex items-center justify-center">
          <img
            src={`/images/creatures/${opponentCreature?.meta.creature_type ?? 'unknown'}_front.png`}
            alt={opponentCreature?.display_name ?? 'Unknown'}
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="col-start-2 row-start-2 flex items-center justify-center">
          <img
            src={`/images/creatures/${playerCreature?.meta.creature_type ?? 'unknown'}_back.png`}
            alt={playerCreature?.display_name ?? 'Unknown'}
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="col-start-2 row-start-2 flex items-end justify-end">
          <CreatureCard
            uid={playerCreature?.uid ?? ''}
            name={playerCreature?.display_name ?? 'Unknown'}
            image={`/images/creatures/${playerCreature?.meta.creature_type ?? 'unknown'}_back.png`}
            hp={playerCreature?.stats.hp ?? 0}
            maxHp={playerCreature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-100 p-4" style={{ height: '33.33%' }}>
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 h-full">
            {availableButtonSlugs.map((slug) => (
              <SkillButton
                key={slug}
                uid={slug}
                skillName={`Skill ${slug}`}
                description={`Description for skill ${slug}`}
                stats={`Damage: Unknown`}
                onClick={() => emitButtonClick(slug)}
              />
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <MessageSquare className="w-8 h-8 mr-2" />
            <span>Waiting for game message...</span>
          </div>
        )}
      </div>
    </div>
  );
}
