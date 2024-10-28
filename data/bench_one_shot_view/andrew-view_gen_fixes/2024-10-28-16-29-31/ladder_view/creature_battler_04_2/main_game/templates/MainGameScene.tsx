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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-center">
      <div className="flex space-x-2 mb-2">
        <Sword size={16} /> <span>{creature.stats.attack}</span>
        <Shield size={16} /> <span>{creature.stats.defense}</span>
        <Zap size={16} /> <span>{creature.stats.speed}</span>
      </div>
      <div className="flex items-center">
        <Heart size={16} className="mr-2" />
        <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex flex-col items-start justify-start">
          <h3 className="text-lg font-bold mb-2">{opponent_creature.display_name}</h3>
          {renderCreatureStats(opponent_creature)}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image="/placeholder-creature-front.png"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            className="transform scale-x-[-1]"
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image="/placeholder-creature-back.png"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex flex-col items-end justify-end">
          <h3 className="text-lg font-bold mb-2">{player_creature.display_name}</h3>
          {renderCreatureStats(player_creature)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
