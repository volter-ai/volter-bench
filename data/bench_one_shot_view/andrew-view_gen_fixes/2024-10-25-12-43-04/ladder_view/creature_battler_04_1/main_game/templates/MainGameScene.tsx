import React from 'react';
import { useCurrentButtons } from "@/lib/useChoices";
import { Shield, Zap } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  collections?: {
    skills?: Skill[];
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

const CreatureStatus: React.FC<{ creature: Creature, isOpponent: boolean }> = ({ creature, isOpponent }) => (
  <div className={`flex flex-col ${isOpponent ? 'items-start' : 'items-end'}`}>
    <h2 className="text-xl font-bold">{creature.display_name}</h2>
    <div className="flex items-center">
      <Shield className="w-4 h-4 mr-1" />
      <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
    </div>
    <div className="flex items-center">
      <Zap className="w-4 h-4 mr-1" />
      <span>{creature.meta.creature_type}</span>
    </div>
  </div>
);

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4" style={{ height: '66.67vh' }}>
        <div className="row-start-2 col-start-1">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/creatures/${playerCreature.uid}_back.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="row-start-2 col-start-2">
          <CreatureStatus creature={playerCreature} isOpponent={false} />
        </div>
        <div className="row-start-1 col-start-2">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/creatures/${opponentCreature.uid}_front.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
        <div className="row-start-1 col-start-1">
          <CreatureStatus creature={opponentCreature} isOpponent={true} />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 p-4">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug, index) => {
              const skill = playerCreature.collections?.skills?.[index];
              return skill ? (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.base_damage}`}
                  onClick={() => emitButtonClick(slug)}
                />
              ) : null;
            })}
          </div>
        ) : (
          <div className="text-center">
            <p className="text-xl">Waiting for action...</p>
          </div>
        )}
      </div>
    </div>
  );
}
