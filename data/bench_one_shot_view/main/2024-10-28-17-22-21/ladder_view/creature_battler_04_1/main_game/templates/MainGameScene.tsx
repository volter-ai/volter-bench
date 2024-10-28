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

  const renderCreatureCard = (creature: Creature, isOpponent: boolean) => (
    <CreatureCard
      uid={creature.uid}
      name={creature.display_name}
      imageUrl={`/images/creatures/${creature.meta.creature_type}/${isOpponent ? 'front' : 'back'}.png`}
      hp={creature.stats.hp}
      maxHp={creature.stats.max_hp}
      className={`w-full h-full ${isOpponent ? 'transform scale-x-[-1]' : ''}`}
    />
  );

  const renderCreatureStatus = (creature: Creature) => (
    <div className="flex flex-col items-center justify-center h-full">
      <h2 className="text-xl font-bold mb-2">{creature.display_name}</h2>
      <div className="flex space-x-2 mb-2">
        <Sword size={16} /> <span>{creature.stats.attack}</span>
        <Shield size={16} /> <span>{creature.stats.defense}</span>
        <Zap size={16} /> <span>{creature.stats.speed}</span>
        <Heart size={16} /> <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
        <div className="bg-blue-600 h-2.5 rounded-full" style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}></div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-1 col-start-2">
          {renderCreatureStatus(opponent_creature)}
        </div>
        <div className="row-start-1 col-start-1">
          {renderCreatureCard(opponent_creature, true)}
        </div>
        <div className="row-start-2 col-start-1">
          {renderCreatureCard(player_creature, false)}
        </div>
        <div className="row-start-2 col-start-2">
          {renderCreatureStatus(player_creature)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4 h-full">
            {player_creature.collections.skills
              .filter(skill => availableButtonSlugs.includes(skill.uid))
              .map((skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}, Physical: ${skill.meta.is_physical}`}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              ))}
          </div>
        ) : (
          <div className="flex items-center justify-center h-full">
            <p className="text-xl">Waiting for opponent...</p>
          </div>
        )}
      </div>
    </div>
  );
}
