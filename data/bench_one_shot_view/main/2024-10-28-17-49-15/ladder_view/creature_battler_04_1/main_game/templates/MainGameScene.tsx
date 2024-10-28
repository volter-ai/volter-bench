import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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
  description: string;
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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full bg-gradient-to-b from-blue-200 to-green-200 flex flex-col">
      {/* Battlefield Display */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex flex-col items-start justify-start">
          <h3 className="text-lg font-bold">{opponent_creature?.display_name}</h3>
          <div className="flex items-center space-x-2">
            <Heart className="w-4 h-4 text-red-500" />
            <div className="w-32 bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-red-500 h-2.5 rounded-full"
                style={{ width: `${(opponent_creature?.stats.hp / opponent_creature?.stats.max_hp) * 100}%` }}
              ></div>
            </div>
            <span className="text-sm">{opponent_creature?.stats.hp}/{opponent_creature?.stats.max_hp}</span>
          </div>
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-start">
          <CreatureCard
            uid={opponent_creature?.uid || ""}
            name={opponent_creature?.display_name || ""}
            imageUrl={`/images/creatures/${opponent_creature?.meta.creature_type}.png`}
            hp={opponent_creature?.stats.hp || 0}
            maxHp={opponent_creature?.stats.max_hp || 1}
          />
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-end">
          <CreatureCard
            uid={player_creature?.uid || ""}
            name={player_creature?.display_name || ""}
            imageUrl={`/images/creatures/${player_creature?.meta.creature_type}_back.png`}
            hp={player_creature?.stats.hp || 0}
            maxHp={player_creature?.stats.max_hp || 1}
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex flex-col items-end justify-end">
          <h3 className="text-lg font-bold">{player_creature?.display_name}</h3>
          <div className="flex items-center space-x-2">
            <span className="text-sm">{player_creature?.stats.hp}/{player_creature?.stats.max_hp}</span>
            <div className="w-32 bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-green-500 h-2.5 rounded-full"
                style={{ width: `${(player_creature?.stats.hp / player_creature?.stats.max_hp) * 100}%` }}
              ></div>
            </div>
            <Heart className="w-4 h-4 text-green-500" />
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}, ${skill.meta.is_physical ? 'Physical' : 'Special'}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
