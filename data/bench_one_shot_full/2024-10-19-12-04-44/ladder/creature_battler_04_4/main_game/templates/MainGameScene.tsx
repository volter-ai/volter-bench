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
      image={`/images/creatures/${creature.meta.creature_type}_${isOpponent ? 'front' : 'back'}.png`}
      hp={creature.stats.hp}
      maxHp={creature.stats.max_hp}
      className={`w-full h-full ${isOpponent ? 'transform scale-x-[-1]' : ''}`}
    />
  );

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-center justify-center h-full">
      <h2 className="text-xl font-bold mb-2">{creature.display_name}</h2>
      <div className="grid grid-cols-2 gap-2">
        <div className="flex items-center"><Sword className="mr-1" size={16} /> {creature.stats.attack}</div>
        <div className="flex items-center"><Shield className="mr-1" size={16} /> {creature.stats.defense}</div>
        <div className="flex items-center"><Zap className="mr-1" size={16} /> {creature.stats.speed}</div>
        <div className="flex items-center"><Heart className="mr-1" size={16} /> {creature.stats.hp}/{creature.stats.max_hp}</div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-200 to-green-200 flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-2 col-start-1">
          {renderCreatureCard(player_creature, false)}
        </div>
        <div className="row-start-2 col-start-2">
          {renderCreatureStats(player_creature)}
        </div>
        <div className="row-start-1 col-start-2">
          {renderCreatureCard(opponent_creature, true)}
        </div>
        <div className="row-start-1 col-start-1">
          {renderCreatureStats(opponent_creature)}
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
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
