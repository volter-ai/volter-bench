import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Heart } from 'lucide-react';

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  const renderCreatureStatus = (creature: Creature, isOpponent: boolean) => (
    <div className={`flex flex-col ${isOpponent ? 'items-start' : 'items-end'}`}>
      <h3 className="text-lg font-bold">{creature.display_name}</h3>
      <div className="flex items-center">
        <Heart className="w-4 h-4 mr-2" />
        <span>{creature.stats.hp}/{creature.stats.max_hp} HP</span>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex items-start justify-start">
          {renderCreatureStatus(opponent_creature, true)}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-end">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            className="w-1/2 h-auto"
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="w-1/2 h-auto"
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex items-end justify-end">
          {renderCreatureStatus(player_creature, false)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {availableButtonSlugs.map((slug) => {
            const skill = player_creature.collections.skills.find(s => s.uid === slug);
            if (!skill) return null;
            return (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                onClick={() => emitButtonClick(slug)}
              />
            );
          })}
        </div>
        {availableButtonSlugs.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <p className="text-lg">Waiting for action...</p>
          </div>
        )}
      </div>
    </div>
  );
}
