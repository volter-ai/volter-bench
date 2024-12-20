import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap } from 'lucide-react';

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
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden flex flex-col">
        {/* Battlefield Display */}
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4 bg-gradient-to-b from-blue-100 to-green-100">
          {/* Opponent Status */}
          <div className="row-start-1 col-start-1 flex items-start justify-start">
            <CreatureCard
              uid={opponentCreature?.uid ?? ""}
              name={opponentCreature?.display_name ?? "Unknown"}
              image="/placeholder-opponent.png"
              hp={opponentCreature?.stats.hp ?? 0}
              maxHp={opponentCreature?.stats.max_hp ?? 1}
              className="transform scale-75 origin-top-left"
            />
          </div>
          
          {/* Opponent Creature */}
          <div className="row-start-1 col-start-2 flex items-center justify-center">
            <img
              src="/placeholder-opponent-front.png"
              alt={opponentCreature?.display_name ?? "Opponent Creature"}
              className="max-h-full max-w-full object-contain"
            />
          </div>
          
          {/* Player Creature */}
          <div className="row-start-2 col-start-1 flex items-center justify-center">
            <img
              src="/placeholder-player-back.png"
              alt={playerCreature?.display_name ?? "Player Creature"}
              className="max-h-full max-w-full object-contain"
            />
          </div>
          
          {/* Player Status */}
          <div className="row-start-2 col-start-2 flex items-end justify-end">
            <CreatureCard
              uid={playerCreature?.uid ?? ""}
              name={playerCreature?.display_name ?? "Unknown"}
              image="/placeholder-player.png"
              hp={playerCreature?.stats.hp ?? 0}
              maxHp={playerCreature?.stats.max_hp ?? 1}
              className="transform scale-75 origin-bottom-right"
            />
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 p-4 bg-gray-200">
          {availableButtonSlugs.length > 0 ? (
            <div className="grid grid-cols-2 gap-4 h-full">
              {playerCreature?.collections.skills.map((skill: Skill, index: number) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                  onClick={() => emitButtonClick(skill.uid)}
                  className="h-full text-lg font-semibold"
                >
                  <div className="flex items-center justify-center">
                    {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
                    {skill.display_name}
                  </div>
                </SkillButton>
              ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-2xl font-bold text-gray-600">Waiting for action...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
