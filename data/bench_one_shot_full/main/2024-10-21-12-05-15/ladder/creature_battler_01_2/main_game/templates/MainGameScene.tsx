import { useCurrentButtons } from "@/lib/useChoices.ts";
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
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Game HUD</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <span className="mb-2 font-bold">Player</span>
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={playerCreature?.stats.hp ?? 0}
          />
        </div>
        <div className="flex flex-col items-center">
          <span className="mb-2 font-bold">Opponent</span>
          <CreatureCard
            uid={botCreature?.uid ?? ""}
            name={botCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={botCreature?.stats.hp ?? 0}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-200 p-4">
        {showText ? (
          <div className="bg-white p-4 rounded-lg shadow">
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
