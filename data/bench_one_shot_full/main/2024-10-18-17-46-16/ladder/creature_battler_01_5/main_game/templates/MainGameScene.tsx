import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { useState } from "react";
import { Sword, Shield } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    damage: number;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
  };
  uid: string;
  display_name: string;
  description: string;
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const [showText, setShowText] = useState(true);

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={playerCreature?.stats.hp ?? 0}
          />
          <div className="mt-2 flex items-center">
            <Sword className="mr-1" /> Player
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature?.uid ?? ""}
            name={opponentCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={opponentCreature?.stats.hp ?? 0}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-1" /> Opponent
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4 overflow-y-auto">
        {showText ? (
          <div className="text-lg">
            Battle in progress... Choose your next move!
            <button onClick={() => setShowText(false)} className="ml-4 p-2 bg-blue-500 text-white rounded">
              Show Skills
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug) => (
              <SkillButton
                key={slug}
                uid={slug}
                skillName={slug}
                description="Skill description"
                stats="Skill stats"
                onClick={() => emitButtonClick(slug)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
