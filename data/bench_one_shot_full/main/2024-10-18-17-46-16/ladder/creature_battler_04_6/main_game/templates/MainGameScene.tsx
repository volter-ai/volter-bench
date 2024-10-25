import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex items-start justify-end">
          <img
            src={`/images/creatures/${opponent_creature.meta.creature_type}_front.png`}
            alt={opponent_creature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex items-end justify-start">
          <img
            src={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            alt={player_creature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="row-start-2 col-start-2 flex items-end justify-end">
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
        <div className="grid grid-cols-2 gap-4">
          {player_creature.collections?.skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!availableButtonSlugs.includes('use-skill')}
              onClick={() => emitButtonClick('use-skill', { skillId: skill.uid })}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
