import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

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
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col">
      {/* Battlefield (upper 2/3) */}
      <div className="flex-grow flex flex-col justify-between p-4">
        {/* Top row */}
        <div className="flex justify-between">
          {/* Opponent Status */}
          <div className="w-1/3">
            {opponent_creature && (
              <CreatureCard
                uid={opponent_creature.uid}
                name={opponent_creature.display_name}
                image={`/images/creatures/${opponent_creature.meta.prototype_id}_front.png`}
                hp={opponent_creature.stats.hp}
                maxHp={opponent_creature.stats.max_hp}
              />
            )}
          </div>
          {/* Opponent Creature */}
          <div className="w-1/3 flex justify-center items-end">
            {opponent_creature && (
              <img
                src={`/images/creatures/${opponent_creature.meta.prototype_id}_front.png`}
                alt={opponent_creature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>
        </div>
        {/* Bottom row */}
        <div className="flex justify-between">
          {/* Player Creature */}
          <div className="w-1/3 flex justify-center items-start">
            {player_creature && (
              <img
                src={`/images/creatures/${player_creature.meta.prototype_id}_back.png`}
                alt={player_creature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
          </div>
          {/* Player Status */}
          <div className="w-1/3">
            {player_creature && (
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                image={`/images/creatures/${player_creature.meta.prototype_id}_back.png`}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
              />
            )}
          </div>
        </div>
      </div>

      {/* User Interface (lower 1/3) */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
            >
              {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
