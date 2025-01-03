import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
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

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  description: string;
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
    category: "Creature";
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
    category: "Player";
  };
  collections: {
    creatures: Creature[];
  };
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
  const { player_creature, opponent_creature } = props.data.entities;

  // Safety check for required entities
  if (!player_creature || opponent_creature?.["__type"] !== "Creature") {
    return <div>Missing player creature data</div>;
  }

  if (!opponent_creature || opponent_creature?.["__type"] !== "Creature") {
    return <div>Missing opponent creature data</div>;
  }

  return (
    <div className="h-screen w-screen flex flex-col">
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 bg-gradient-to-b from-sky-400 to-sky-300 p-4 gap-4">
        {/* Opponent Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            currentHp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            image={`/creatures/${opponent_creature.meta.prototype_id}_front.png`}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img
              src={`/creatures/${opponent_creature.meta.prototype_id}_front.png`}
              alt={opponent_creature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm transform -scale-y-50" />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <div className="relative">
            <img
              src={`/creatures/${player_creature.meta.prototype_id}_back.png`}
              alt={player_creature.display_name}
              className="w-48 h-48 object-contain"
            />
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm transform -scale-y-50" />
          </div>
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            currentHp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            image={`/creatures/${player_creature.meta.prototype_id}_back.png`}
          />
        </div>
      </div>

      {/* Skills UI */}
      <div className="h-1/3 bg-white p-4 grid grid-cols-2 gap-4">
        {player_creature.collections.skills?.map((skill) => {
          if (skill.__type !== "Skill") return null;
          
          return (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              damage={skill.stats.base_damage}
              type={skill.meta.skill_type}
            />
          );
        })}
      </div>
    </div>
  );
}
