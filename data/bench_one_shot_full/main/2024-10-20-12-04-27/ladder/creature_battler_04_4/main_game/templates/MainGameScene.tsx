import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap, Heart } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="row-start-1 col-start-1 flex items-start justify-start">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            image={`/images/creatures/${opponentCreature.meta.creature_type}.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="transform scale-75 origin-top-left"
          />
        </div>

        {/* Opponent Creature */}
        <div className="row-start-1 col-start-2 flex items-center justify-center">
          <img
            src={`/images/creatures/${opponentCreature.meta.creature_type}_front.png`}
            alt={opponentCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature */}
        <div className="row-start-2 col-start-1 flex items-center justify-center">
          <img
            src={`/images/creatures/${playerCreature.meta.creature_type}_back.png`}
            alt={playerCreature.display_name}
            className="w-48 h-48 object-contain"
          />
        </div>

        {/* Player Creature Status */}
        <div className="row-start-2 col-start-2 flex items-end justify-end">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            image={`/images/creatures/${playerCreature.meta.creature_type}.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="transform scale-75 origin-bottom-right"
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4 flex items-center justify-center">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              className="w-40 h-16"
            >
              {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
