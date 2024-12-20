import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { useState, useEffect } from "react";
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

  // Toggle showText to false after a delay to show buttons
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowText(false);
    }, 3000); // 3 seconds delay

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <div className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Game HUD</h1>
      </div>

      <div className="flex-grow flex items-center justify-around p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder.jpg"
            hp={playerCreature.stats.hp}
          />
          <div className="mt-2 flex items-center">
            <Sword className="mr-2" /> Player
          </div>
        </div>

        <div className="flex flex-col items-center">
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            imageUrl="/placeholder.jpg"
            hp={botCreature.stats.hp}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-2" /> Opponent
          </div>
        </div>
      </div>

      <div className="h-1/3 bg-gray-200 p-4">
        {showText ? (
          <div className="bg-white p-4 rounded-lg shadow">
            <p>Game text goes here...</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-4">
            {playerCreature.collections.skills.map((skill) => (
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
