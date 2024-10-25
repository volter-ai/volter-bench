import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
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
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-7xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Battlefield (upper 2/3) */}
        <div className="h-2/3 flex flex-col">
          {/* Top row */}
          <div className="h-1/2 flex">
            {/* Opponent status */}
            <div className="w-1/2 p-4 flex items-center justify-center">
              <CreatureCard
                uid={opponent_creature.uid}
                name={opponent_creature.display_name}
                image={`/images/creatures/${opponent_creature.meta.prototype_id}_front.png`}
                hp={opponent_creature.stats.hp}
                maxHp={opponent_creature.stats.max_hp}
              />
            </div>
            {/* Opponent creature */}
            <div className="w-1/2 p-4 flex items-center justify-center">
              <img
                src={`/images/creatures/${opponent_creature.meta.prototype_id}_front.png`}
                alt={opponent_creature.display_name}
                className="max-h-full max-w-full object-contain"
              />
            </div>
          </div>
          {/* Bottom row */}
          <div className="h-1/2 flex">
            {/* Player creature */}
            <div className="w-1/2 p-4 flex items-center justify-center">
              <img
                src={`/images/creatures/${player_creature.meta.prototype_id}_back.png`}
                alt={player_creature.display_name}
                className="max-h-full max-w-full object-contain"
              />
            </div>
            {/* Player status */}
            <div className="w-1/2 p-4 flex items-center justify-center">
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                image={`/images/creatures/${player_creature.meta.prototype_id}_front.png`}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
              />
            </div>
          </div>
        </div>

        {/* User Interface (lower 1/3) */}
        <div className="h-1/3 p-4 bg-gray-200">
          <div className="grid grid-cols-2 gap-4 h-full">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
                className="w-full h-full text-lg"
              >
                {skill.meta.skill_type === "normal" && <Sword className="mr-2" />}
                {skill.meta.skill_type === "water" && <Shield className="mr-2" />}
                {skill.meta.skill_type === "fire" && <Zap className="mr-2" />}
                {skill.display_name}
              </SkillButton>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
