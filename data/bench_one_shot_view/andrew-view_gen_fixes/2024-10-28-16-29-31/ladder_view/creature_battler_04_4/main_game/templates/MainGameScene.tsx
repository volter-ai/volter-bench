import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield, Zap, Heart } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
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
  collections?: {
    skills: Skill[];
  };
}

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

interface GameUIData {
  entities: {
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
      image={`/images/creatures/${creature.meta.creature_type}/${isOpponent ? 'front' : 'back'}.png`}
      hp={creature.stats.hp}
      maxHp={creature.stats.max_hp}
      className={`w-full h-full ${isOpponent ? 'transform scale-x-[-1]' : ''}`}
    />
  );

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-start p-4 bg-gray-100 rounded-lg">
      <h3 className="text-lg font-bold mb-2">{creature.display_name}</h3>
      <div className="flex items-center mb-1">
        <Heart className="w-4 h-4 mr-2" />
        <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
      </div>
      <div className="flex items-center mb-1">
        <Sword className="w-4 h-4 mr-2" />
        <span>{creature.stats.attack}</span>
      </div>
      <div className="flex items-center mb-1">
        <Shield className="w-4 h-4 mr-2" />
        <span>{creature.stats.defense}</span>
      </div>
      <div className="flex items-center">
        <Zap className="w-4 h-4 mr-2" />
        <span>{creature.stats.speed}</span>
      </div>
    </div>
  );

  const renderSkillButtons = () => {
    const skills = player_creature.collections?.skills || [];
    return skills
      .filter(skill => availableButtonSlugs.includes(skill.uid))
      .map((skill: Skill) => (
        <SkillButton
          key={skill.uid}
          uid={skill.uid}
          skillName={skill.display_name}
          description={skill.description}
          stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
          onClick={() => emitButtonClick(skill.uid)}
        />
      ));
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-1 col-start-1">
          {renderCreatureStats(opponent_creature)}
        </div>
        <div className="row-start-1 col-start-2">
          {renderCreatureCard(opponent_creature, true)}
        </div>
        <div className="row-start-2 col-start-1">
          {renderCreatureCard(player_creature, false)}
        </div>
        <div className="row-start-2 col-start-2">
          {renderCreatureStats(player_creature)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {renderSkillButtons()}
          </div>
        ) : (
          <div className="text-center">Waiting for action...</div>
        )}
      </div>
    </div>
  );
}
