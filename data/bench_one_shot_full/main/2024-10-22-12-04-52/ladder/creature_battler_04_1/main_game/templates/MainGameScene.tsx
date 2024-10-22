import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Zap } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
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
  meta: {
    skill_type: string;
    is_physical: boolean;
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
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature?.uid || ''}
            name={opponentCreature?.display_name || 'Unknown'}
            image={`/images/creatures/${opponentCreature?.meta.creature_type || 'unknown'}_front.png`}
            hp={opponentCreature?.stats.hp || 0}
            maxHp={opponentCreature?.stats.max_hp || 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          <img
            src={`/images/creatures/${opponentCreature?.meta.creature_type || 'unknown'}_front.png`}
            alt={opponentCreature?.display_name || 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          <img
            src={`/images/creatures/${playerCreature?.meta.creature_type || 'unknown'}_back.png`}
            alt={playerCreature?.display_name || 'Unknown'}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={playerCreature?.uid || ''}
            name={playerCreature?.display_name || 'Unknown'}
            image={`/images/creatures/${playerCreature?.meta.creature_type || 'unknown'}_back.png`}
            hp={playerCreature?.stats.hp || 0}
            maxHp={playerCreature?.stats.max_hp || 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug) => {
              const skill = playerCreature?.collections?.skills?.find((s: Skill) => s.uid === slug);
              return skill ? (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                  onClick={() => emitButtonClick(slug)}
                >
                  <div className="flex items-center">
                    {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
                    {skill.display_name}
                  </div>
                </SkillButton>
              ) : null;
            })}
          </div>
        ) : (
          <div className="text-center text-lg">Waiting for action...</div>
        )}
      </div>
    </div>
  );
}
