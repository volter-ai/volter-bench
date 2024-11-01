import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { MessageSquare } from 'lucide-react';

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  const availableSkills = player_creature?.collections.skills.filter(skill => 
    availableButtonSlugs.includes(skill.uid)
  ) || [];

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex justify-start items-start">
          <CreatureCard
            uid={opponent_creature?.uid ?? ""}
            name={opponent_creature?.display_name ?? "Unknown"}
            image={`/images/creatures/${opponent_creature?.meta.prototype_id ?? "unknown"}_front.png`}
            hp={opponent_creature?.stats.hp ?? 0}
            maxHp={opponent_creature?.stats.max_hp ?? 1}
            className="w-1/2 h-auto"
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          <img
            src={`/images/creatures/${opponent_creature?.meta.prototype_id ?? "unknown"}_front.png`}
            alt={opponent_creature?.display_name ?? "Unknown Creature"}
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <img
            src={`/images/creatures/${player_creature?.meta.prototype_id ?? "unknown"}_back.png`}
            alt={player_creature?.display_name ?? "Unknown Creature"}
            className="w-32 h-32 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={player_creature?.uid ?? ""}
            name={player_creature?.display_name ?? "Unknown"}
            image={`/images/creatures/${player_creature?.meta.prototype_id ?? "unknown"}_back.png`}
            hp={player_creature?.stats.hp ?? 0}
            maxHp={player_creature?.stats.max_hp ?? 1}
            className="w-1/2 h-auto"
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableSkills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 h-full">
            {availableSkills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(skill.uid)}
                className="h-full"
              />
            ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <MessageSquare className="w-8 h-8 mr-2" />
            <span className="text-lg">Waiting for action...</span>
          </div>
        )}
      </div>
    </div>
  );
}
