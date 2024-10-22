import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
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
        <div className="flex items-center">
          <Sword className="mr-2" />
          <span>Player: {props.data.entities.player?.display_name}</span>
        </div>
        <div className="flex items-center">
          <span>Opponent: {props.data.entities.bot?.display_name}</span>
          <Shield className="ml-2" />
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder.jpg"
              hp={playerCreature.stats.hp}
            />
          )}
          <span className="mt-2 font-bold">Player's Creature</span>
        </div>
        <div className="flex flex-col items-center">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              imageUrl="/placeholder.jpg"
              hp={botCreature.stats.hp}
            />
          )}
          <span className="mt-2 font-bold">Opponent's Creature</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-white p-4 overflow-y-auto">
        {showText ? (
          <div className="bg-gray-200 p-4 rounded-lg">
            <p>Game text goes here...</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
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
        <button
          className="mt-4 bg-blue-500 text-white px-4 py-2 rounded"
          onClick={() => setShowText(!showText)}
        >
          {showText ? "Show Skills" : "Show Text"}
        </button>
      </div>
    </div>
  );
}
