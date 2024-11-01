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
  slug: string;
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
      image={`/images/creatures/${creature.meta.creature_type}_${isOpponent ? 'front' : 'back'}.png`}
      hp={creature.stats.hp}
      maxHp={creature.stats.max_hp}
      className="w-full h-full"
    />
  );

  const renderCreatureStats = (creature: Creature) => (
    <div className="flex flex-col items-center justify-center h-full">
      <h2 className="text-xl font-bold mb-2">{creature.display_name}</h2>
      <div className="flex space-x-2">
        <div className="flex items-center"><Sword size={16} className="mr-1" /> {creature.stats.attack}</div>
        <div className="flex items-center"><Shield size={16} className="mr-1" /> {creature.stats.defense}</div>
        <div className="flex items-center"><Zap size={16} className="mr-1" /> {creature.stats.speed}</div>
        <div className="flex items-center"><Heart size={16} className="mr-1" /> {creature.stats.hp}/{creature.stats.max_hp}</div>
      </div>
    </div>
  );

  return (
    <div className="w-full h-full flex items-center justify-center bg-gray-100">
      <div className="w-full max-w-6xl aspect-video bg-white shadow-lg rounded-lg overflow-hidden">
        {/* Battlefield Display */}
        <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
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
        <div className="h-1/3 p-4">
          {availableButtonSlugs.length > 0 ? (
            <div className="grid grid-cols-2 gap-4 h-full">
              {player_creature.collections?.skills
                .filter(skill => availableButtonSlugs.includes(skill.slug))
                .map((skill: Skill) => (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    skillName={skill.display_name}
                    description={skill.description}
                    stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
                    onClick={() => emitButtonClick(skill.slug)}
                  />
                ))}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full">
              <p className="text-xl">Waiting for action...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
