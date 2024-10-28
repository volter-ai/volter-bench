import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

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

interface Creature {
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

  const renderCreatureImage = (creature: Creature, isOpponent: boolean) => (
    <div className={`relative ${isOpponent ? 'self-start' : 'self-end'} w-48 h-48`}>
      <img
        src={`/images/creatures/${creature.meta.creature_type}.png`}
        alt={creature.display_name}
        className="w-full h-full object-contain"
      />
      <div className="absolute bottom-0 left-0 right-0 h-4 bg-gradient-to-t from-gray-800 to-transparent"></div>
    </div>
  );

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-start space-y-1">
      <div className="flex items-center space-x-2">
        <Sword size={16} /> <span>{creature.stats.attack}</span>
        <Shield size={16} /> <span>{creature.stats.defense}</span>
      </div>
      <div className="flex items-center space-x-2">
        <Zap size={16} /> <span>{creature.stats.speed}</span>
        <Heart size={16} /> <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          {renderCreatureImage(opponent_creature, true)}
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          {renderCreatureImage(player_creature, false)}
        </div>

        {/* Player Creature Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 ? (
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
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-xl font-semibold">Waiting for opponent...</p>
          </div>
        )}
      </div>
    </div>
  );
}
