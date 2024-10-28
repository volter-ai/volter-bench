import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
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
}

interface GameUIData {
  entities: {
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

  const renderCreatureCard = (creature?: Creature, isOpponent: boolean = false) => {
    if (!creature) return null;
    return (
      <CreatureCard
        uid={creature.uid}
        name={creature.display_name}
        imageUrl={`/images/creatures/${creature.meta.creature_type || 'default'}.png`}
        hp={creature.stats.hp}
        maxHp={creature.stats.max_hp}
        className="w-full h-full"
      />
    );
  };

  const renderSkillButtons = (skills?: Skill[]) => {
    if (!skills || skills.length === 0) return null;
    return (
      <div className="grid grid-cols-2 gap-4">
        {skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            stats={`Damage: ${skill.stats.base_damage}`}
            className="w-full"
            onClick={() => {
              const buttonSlug = availableButtonSlugs.find(slug => slug === skill.uid);
              if (buttonSlug) {
                emitButtonClick(buttonSlug);
              } else {
                console.error(`Button slug not found for skill: ${skill.uid}`);
              }
            }}
          />
        ))}
      </div>
    );
  };

  const renderCreatureStatus = (creature?: Creature, isOpponent: boolean = false) => {
    if (!creature) return null;
    return (
      <div className={`text-${isOpponent ? 'left' : 'right'}`}>
        <h2 className="text-xl font-bold">{creature.display_name}</h2>
        <div className={`flex items-center ${isOpponent ? 'justify-start' : 'justify-end'} space-x-2`}>
          <Shield className="w-4 h-4" />
          <span>{creature.stats.hp}/{creature.stats.max_hp}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          {renderCreatureStatus(opponent_creature, true)}
        </div>
        <div className="row-start-1 col-start-2 flex items-center justify-center">
          {renderCreatureCard(opponent_creature, true)}
        </div>
        <div className="row-start-2 col-start-1 flex items-center justify-center">
          {renderCreatureCard(player_creature)}
        </div>
        <div className="row-start-2 col-start-2 flex items-end justify-end">
          {renderCreatureStatus(player_creature)}
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {availableButtonSlugs.length > 0 ? (
          renderSkillButtons(player_creature?.collections?.skills)
        ) : (
          <div className="text-center">
            <p className="text-lg">Waiting for opponent's move...</p>
          </div>
        )}
      </div>
    </div>
  );
}
