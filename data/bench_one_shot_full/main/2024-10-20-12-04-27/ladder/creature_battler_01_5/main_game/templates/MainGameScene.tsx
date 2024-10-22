import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Heart, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { useState } from "react";

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
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <span>Player: {props.data.entities.player?.display_name}</span>
        <span>Opponent: {props.data.entities.opponent?.display_name}</span>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-around items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={playerCreature?.stats.hp ?? 0}
          />
          <span className="mt-2 flex items-center">
            <Heart className="mr-1" /> Player's Creature
          </span>
        </div>
        <Swords className="text-red-500" size={48} />
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature?.uid ?? ""}
            name={opponentCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={opponentCreature?.stats.hp ?? 0}
          />
          <span className="mt-2 flex items-center">
            <Heart className="mr-1" /> Opponent's Creature
          </span>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4 overflow-y-auto">
        {showText ? (
          <div className="text-lg">
            Game text describing what is happening...
          </div>
        ) : (
          <div className="flex flex-wrap gap-2">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => emitButtonClick(skill.uid)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
