import { useCurrentButtons } from "@/lib/useChoices";
import { Shield, Sword, Heart, Zap } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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
  };
  collections: {
    skills: Skill[];
  };
  meta: {
    creature_type: string;
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  if (!player_creature || !opponent_creature || !player || !opponent) {
    return <div className="h-screen w-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="h-screen w-full flex flex-col">
      {/* Battlefield Area */}
      <div className="flex-grow-2 grid grid-cols-2 gap-4 p-4">
        {/* Opponent Info */}
        <div className="flex justify-start items-start">
          <PlayerCard
            uid={`${opponent.uid}-card`}
            name={opponent.display_name}
            imageUrl=""
          />
        </div>
        
        {/* Opponent Creature Status */}
        <div className="flex justify-end items-start">
          <CreatureCard
            uid={`${opponent_creature.uid}-status`}
            name={opponent_creature.display_name}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            imageUrl=""
          />
        </div>

        {/* Player Info */}
        <div className="flex justify-start items-end">
          <PlayerCard
            uid={`${player.uid}-card`}
            name={player.display_name}
            imageUrl=""
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex justify-end items-end">
          <CreatureCard
            uid={`${player_creature.uid}-status`}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            imageUrl=""
          />
        </div>
      </div>

      {/* UI Area */}
      <div className="flex-grow-1 grid grid-cols-2 gap-4 p-4">
        {player_creature.collections.skills?.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            skillName={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
            type={skill.meta.skill_type}
          />
        ))}
      </div>
    </div>
  );
}
