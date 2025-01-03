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
    <div className={`relative ${isOpponent ? 'scale-x-[-1]' : ''} w-64 h-64 flex items-center justify-center`}>
      <div className="absolute bottom-0 w-full h-1/4 bg-gradient-to-t from-gray-800 to-transparent opacity-50 rounded-full"></div>
      <img
        src={`/images/creatures/${creature.meta.creature_type}/${creature.uid}.png`}
        alt={creature.display_name}
        className="w-full h-full object-contain"
      />
    </div>
  );

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-start space-y-1 text-sm bg-white bg-opacity-50 p-2 rounded">
      <div className="flex items-center space-x-2">
        <Sword size={12} /> <span>{creature.stats.attack}</span>
        <Shield size={12} /> <span>{creature.stats.defense}</span>
      </div>
      <div className="flex items-center space-x-2">
        <Zap size={12} /> <span>{creature.stats.speed}</span>
        <Heart size={12} /> <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex flex-col items-start justify-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl={`/images/creatures/${opponent_creature.meta.creature_type}/${opponent_creature.uid}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
          {renderCreatureStats(opponent_creature)}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          {renderCreatureImage(opponent_creature, true)}
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          {renderCreatureImage(player_creature, false)}
        </div>

        {/* Player Creature Status */}
        <div className="flex flex-col items-end justify-end">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={`/images/creatures/${player_creature.meta.creature_type}/${player_creature.uid}.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
          {renderCreatureStats(player_creature)}
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
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
        {availableButtonSlugs.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <p className="text-xl font-semibold">Waiting for opponent's move...</p>
          </div>
        )}
      </div>
    </div>
  );
}
