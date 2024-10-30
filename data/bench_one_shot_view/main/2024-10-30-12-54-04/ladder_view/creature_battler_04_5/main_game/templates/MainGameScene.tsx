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
  meta: {
    skill_type: string;
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
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
        {/* Battlefield Display */}
        <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Status */}
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
                className="transform scale-75 origin-top-left"
              />
            )}
          </div>
          
          {/* Opponent Creature */}
          <div className="row-start-1 col-start-2 flex items-center justify-center">
            <img
              src={`/images/creatures/${opponentCreature?.meta.creature_type}_front.png`}
              alt={opponentCreature?.display_name}
              className="max-h-full max-w-full object-contain"
            />
          </div>
          
          {/* Player Creature */}
          <div className="row-start-2 col-start-1 flex items-center justify-center">
            <img
              src={`/images/creatures/${playerCreature?.meta.creature_type}_back.png`}
              alt={playerCreature?.display_name}
              className="max-h-full max-w-full object-contain"
            />
          </div>
          
          {/* Player Status */}
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
                className="transform scale-75 origin-bottom-right"
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 p-4 bg-gray-200">
          {availableButtonSlugs.length > 0 ? (
            <div className="grid grid-cols-2 gap-4 h-full">
              {availableButtonSlugs.map((slug) => {
                const skill = playerCreature.collections.skills.find(s => s.uid === slug);
                return skill ? (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    skillName={skill.display_name}
                    description={skill.description}
                    stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                    onClick={() => emitButtonClick(slug)}
                    className="w-full h-full text-lg"
                  />
                ) : null;
              })}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="bg-white p-4 rounded-lg shadow flex items-center space-x-2">
                <MessageSquare className="w-6 h-6 text-blue-500" />
                <span className="text-lg">Waiting for action...</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
