import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Zap, X } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

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
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Creature Status */}
        <div className="flex flex-col items-start justify-start">
          <h3 className="text-lg font-bold">{opponent_creature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div 
              className="bg-red-600 h-2.5 rounded-full" 
              style={{ width: `${((opponent_creature?.stats.hp ?? 0) / (opponent_creature?.stats.max_hp ?? 1)) * 100}%` }}
            ></div>
          </div>
          <p>{opponent_creature?.stats.hp} / {opponent_creature?.stats.max_hp} HP</p>
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={opponent_creature?.uid ?? ""}
            name={opponent_creature?.display_name ?? "Unknown"}
            image={`/images/creatures/${opponent_creature?.meta.creature_type}.png`}
            hp={opponent_creature?.stats.hp ?? 0}
            maxHp={opponent_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <CreatureCard
            uid={player_creature?.uid ?? ""}
            name={player_creature?.display_name ?? "Unknown"}
            image={`/images/creatures/${player_creature?.meta.creature_type}.png`}
            hp={player_creature?.stats.hp ?? 0}
            maxHp={player_creature?.stats.max_hp ?? 1}
          />
        </div>

        {/* Player Creature Status */}
        <div className="flex flex-col items-end justify-start">
          <h3 className="text-lg font-bold">{player_creature?.display_name}</h3>
          <div className="w-full bg-gray-200 rounded-full h-2.5 mt-2">
            <div 
              className="bg-green-600 h-2.5 rounded-full" 
              style={{ width: `${((player_creature?.stats.hp ?? 0) / (player_creature?.stats.max_hp ?? 1)) * 100}%` }}
            ></div>
          </div>
          <p>{player_creature?.stats.hp} / {player_creature?.stats.max_hp} HP</p>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
            />
          ))}
          {availableButtonSlugs.includes('quit-game') && (
            <Button onClick={() => emitButtonClick('quit-game')} className="col-span-2">
              <X className="mr-2 h-4 w-4" /> Quit Game
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
