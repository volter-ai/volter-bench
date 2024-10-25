import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { useState } from "react";
import { Sword, Shield } from 'lucide-react';

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
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
    <div className="flex flex-col h-full w-full bg-gray-200">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between">
        <span>Player: {props.data.entities.player?.display_name}</span>
        <span>Opponent: {props.data.entities.bot?.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Sword className="mb-2" />
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={playerCreature?.stats.hp ?? 0}
          />
          <span className="mt-2">Player's Creature</span>
        </div>
        <div className="flex flex-col items-center">
          <Shield className="mb-2" />
          <CreatureCard
            uid={botCreature?.uid ?? ""}
            name={botCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder.jpg"
            hp={botCreature?.stats.hp ?? 0}
          />
          <span className="mt-2">Opponent's Creature</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        {showText ? (
          <div className="bg-white p-4 rounded-md shadow-md h-full overflow-y-auto">
            <p>Game text and descriptions will appear here.</p>
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
