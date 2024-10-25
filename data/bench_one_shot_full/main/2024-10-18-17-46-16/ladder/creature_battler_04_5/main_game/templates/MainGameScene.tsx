import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Zap } from 'lucide-react';

interface Skill {
  __type: "Skill";
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
  __type: "Creature";
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
  __type: "Player";
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

  return (
    <div className="w-full h-full flex flex-col bg-gradient-to-b from-blue-200 to-green-200">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex items-start justify-end">
          <img
            src={`/images/creatures/${opponent_creature.meta.creature_type}_front.png`}
            alt={opponent_creature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}_front.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
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
              disabled={!availableButtonSlugs.includes('use-skill')}
              onClick={() => emitButtonClick('use-skill')}
            >
              <div className="flex items-center">
                {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
                {skill.display_name}
              </div>
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
