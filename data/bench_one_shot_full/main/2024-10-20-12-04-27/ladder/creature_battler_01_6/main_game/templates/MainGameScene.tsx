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
  const [showButtons, setShowButtons] = useState(true);

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
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.png"
            hp={playerCreature?.stats.hp ?? 0}
          />
          <span className="mt-2 font-bold">Player's Creature</span>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={botCreature?.uid ?? ""}
            name={botCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.png"
            hp={botCreature?.stats.hp ?? 0}
          />
          <span className="mt-2 font-bold">Opponent's Creature</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3">
        <div className="flex justify-between mb-2">
          <h2 className="text-xl font-bold">Actions</h2>
          <button
            onClick={() => setShowButtons(!showButtons)}
            className="flex items-center text-blue-600"
          >
            <Info className="mr-1" /> {showButtons ? "Show Info" : "Show Actions"}
          </button>
        </div>
        {showButtons ? (
          <div className="grid grid-cols-2 gap-2">
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
        ) : (
          <div className="bg-gray-100 p-4 rounded-md h-full overflow-y-auto">
            <p>Game information and status updates will be displayed here.</p>
          </div>
        )}
      </div>
    </div>
  );
}
