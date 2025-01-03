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
    player_creature?: Creature;
    opponent_creature?: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  const renderCreatureStats = (creature: Creature | undefined) => {
    if (!creature) return null;
    return (
      <div className="flex flex-col items-start p-2 bg-gray-100 rounded-md">
        <h3 className="text-lg font-bold mb-2">{creature.display_name}</h3>
        <div className="flex items-center mb-1">
          <Heart className="w-4 h-4 mr-1" />
          <span>{creature.stats.hp} / {creature.stats.max_hp}</span>
        </div>
        <div className="flex items-center mb-1">
          <Sword className="w-4 h-4 mr-1" />
          <span>{creature.stats.attack}</span>
        </div>
        <div className="flex items-center mb-1">
          <Shield className="w-4 h-4 mr-1" />
          <span>{creature.stats.defense}</span>
        </div>
        <div className="flex items-center">
          <Zap className="w-4 h-4 mr-1" />
          <span>{creature.stats.speed}</span>
        </div>
      </div>
    );
  };

  const renderCreatureCard = (creature: Creature | undefined, isOpponent: boolean) => {
    if (!creature) return null;
    return (
      <CreatureCard
        uid={creature.uid}
        name={creature.display_name}
        image={`/images/creatures/${creature.meta.creature_type}${isOpponent ? '' : '_back'}.png`}
        hp={creature.stats.hp}
        maxHp={creature.stats.max_hp}
      />
    );
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="flex justify-start items-end">
          {renderCreatureStats(opponent_creature)}
        </div>
        <div className="flex justify-end items-end">
          {renderCreatureCard(opponent_creature, true)}
        </div>
        <div className="flex justify-start items-start">
          {renderCreatureCard(player_creature, false)}
        </div>
        <div className="flex justify-end items-start">
          {renderCreatureStats(player_creature)}
        </div>
      </div>
      <div className="h-1/3 bg-gray-200 p-4">
        {player_creature ? (
          <div className="grid grid-cols-2 gap-4">
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
        ) : (
          <div className="text-center text-gray-600">No creature selected</div>
        )}
      </div>
    </div>
  );
}
