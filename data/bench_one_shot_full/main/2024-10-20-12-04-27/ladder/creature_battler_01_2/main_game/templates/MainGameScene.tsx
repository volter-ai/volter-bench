import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { useState } from "react";
import { Info } from 'lucide-react';

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
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const [showText, setShowText] = useState(true);

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <span>Player: {props.data.entities.player?.display_name}</span>
        <span>Opponent: {props.data.entities.bot?.display_name}</span>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex justify-around items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature?.uid || ""}
            name={playerCreature?.display_name || "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={playerCreature?.stats.hp || 0}
          />
          <span className="mt-2 font-bold">Player's Creature</span>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={botCreature?.uid || ""}
            name={botCreature?.display_name || "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={botCreature?.stats.hp || 0}
          />
          <span className="mt-2 font-bold">Opponent's Creature</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4 flex flex-col">
        <div className="flex justify-between mb-2">
          <h2 className="text-xl font-bold">Actions</h2>
          <button onClick={() => setShowText(!showText)} className="text-blue-600">
            <Info size={24} />
          </button>
        </div>
        {showText ? (
          <div className="flex-1 bg-gray-200 p-4 rounded-md overflow-y-auto">
            <p>Game information and updates will be displayed here.</p>
          </div>
        ) : (
          <div className="flex-1 flex flex-wrap gap-2 overflow-y-auto">
            {playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
