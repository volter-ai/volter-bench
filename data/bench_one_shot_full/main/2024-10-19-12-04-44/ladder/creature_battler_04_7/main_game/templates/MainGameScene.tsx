import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Activity, Zap } from 'lucide-react';

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
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
    <div className="aspect-[16/9] w-full max-w-[1280px] mx-auto bg-gray-100 flex flex-col">
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex items-start justify-start">
          <CreatureCard
            uid={opponent_creature?.uid ?? ""}
            name={opponent_creature?.display_name ?? "Unknown"}
            image="/placeholder-opponent.png"
            hp={opponent_creature?.stats.hp ?? 0}
            maxHp={opponent_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Opponent Creature */}
        <div className="flex items-start justify-end">
          <div className="w-48 h-48 bg-gray-300 rounded-full flex items-center justify-center">
            <Activity size={64} />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex items-end justify-start">
          <div className="w-48 h-48 bg-gray-300 rounded-full flex items-center justify-center">
            <Zap size={64} />
          </div>
        </div>

        {/* Player Creature Status */}
        <div className="flex items-end justify-end">
          <CreatureCard
            uid={player_creature?.uid ?? ""}
            name={player_creature?.display_name ?? "Unknown"}
            image="/placeholder-player.png"
            hp={player_creature?.stats.hp ?? 0}
            maxHp={player_creature?.stats.max_hp ?? 1}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
