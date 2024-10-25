import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
    is_physical: boolean;
  };
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
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface GameUIData {
  entities: {
    player: Player;
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Battlefield Display */}
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 p-4 gap-4">
          {/* Opponent Status */}
          <div className="flex items-start justify-end">
            {opponentCreature && (
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                image={`/images/creatures/${opponentCreature.meta.prototype_id}_front.png`}
                hp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
                className="transform scale-75 origin-top-right"
              />
            )}
          </div>

          {/* Opponent Creature */}
          <div className="flex items-center justify-center">
            {opponentCreature && (
              <img
                src={`/images/creatures/${opponentCreature.meta.prototype_id}_front.png`}
                alt={opponentCreature.display_name}
                className="max-h-full max-w-full object-contain"
              />
            )}
          </div>

          {/* Player Creature */}
          <div className="flex items-center justify-center">
            {playerCreature && (
              <img
                src={`/images/creatures/${playerCreature.meta.prototype_id}_back.png`}
                alt={playerCreature.display_name}
                className="max-h-full max-w-full object-contain"
              />
            )}
          </div>

          {/* Player Status */}
          <div className="flex items-end justify-start">
            {playerCreature && (
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                image={`/images/creatures/${playerCreature.meta.prototype_id}_front.png`}
                hp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
                className="transform scale-75 origin-bottom-left"
              />
            )}
          </div>
        </div>

        {/* User Interface */}
        <div className="h-1/3 p-4">
          <div className="grid grid-cols-2 gap-4 h-full">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                onClick={() => emitButtonClick(skill.uid)}
                className="h-full text-lg font-semibold"
              >
                <div className="flex flex-col items-center justify-center">
                  {skill.meta.skill_type === "normal" && <Sword className="mb-2" />}
                  {skill.meta.skill_type === "water" && <Zap className="mb-2" />}
                  {skill.meta.skill_type === "fire" && <Shield className="mb-2" />}
                  {skill.display_name}
                </div>
              </SkillButton>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
