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

  const renderCreatureStatus = (creature: Creature, isOpponent: boolean) => (
    <div className={`flex flex-col ${isOpponent ? 'items-end' : 'items-start'}`}>
      <h2 className="text-xl font-bold">{creature.display_name}</h2>
      <div className="flex items-center space-x-2">
        <Heart className="w-4 h-4" />
        <div className="w-32 bg-gray-200 rounded-full h-2.5">
          <div
            className="bg-green-600 h-2.5 rounded-full"
            style={{ width: `${(creature.stats.hp / creature.stats.max_hp) * 100}%` }}
          ></div>
        </div>
        <span className="text-sm">{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
    </div>
  );

  const renderStatIcon = (stat: keyof Creature['stats'], value: number) => {
    const icons = {
      attack: Sword,
      defense: Shield,
      speed: Zap,
    };
    const Icon = icons[stat as keyof typeof icons];
    return Icon ? (
      <div className="flex items-center space-x-1">
        <Icon className="w-4 h-4" />
        <span>{value}</span>
      </div>
    ) : null;
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top-left: Opponent Creature */}
        <div className="row-start-1 col-start-1 flex justify-start items-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Top-right: Opponent Creature Status */}
        <div className="row-start-1 col-start-2">
          {renderCreatureStatus(opponent_creature, true)}
        </div>

        {/* Bottom-left: Player Creature Status */}
        <div className="row-start-2 col-start-1 flex flex-col justify-end items-start">
          {renderCreatureStatus(player_creature, false)}
          <div className="flex space-x-2 mt-2">
            {renderStatIcon('attack', player_creature.stats.attack)}
            {renderStatIcon('defense', player_creature.stats.defense)}
            {renderStatIcon('speed', player_creature.stats.speed)}
          </div>
        </div>

        {/* Bottom-right: Player Creature */}
        <div className="row-start-2 col-start-2 flex justify-end items-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
            />
          ))}
        </div>
        {availableButtonSlugs.length === 0 && (
          <div className="text-center text-xl mt-4">Waiting for action...</div>
        )}
      </div>
    </div>
  );
}
