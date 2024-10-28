import React from 'react';
import { useCurrentButtons } from "@/lib/useChoices";
import { Shield, Swords, AlertCircle } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: 'Skill';
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  __type: 'Creature';
  uid: string;
  display_name: string;
  description: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: 'Player';
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  if (!playerCreature || !foeCreature) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gray-100">
        <AlertCircle className="mr-2" />
        <span>Error: Creature data is missing</span>
      </div>
    );
  }

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
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/images/creatures/${playerCreature.uid}.png`}
            hp={playerCreature.stats.hp}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-1" size={16} />
            <span>Player</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={foeCreature.uid}
            name={foeCreature.display_name}
            imageUrl={`/images/creatures/${foeCreature.uid}.png`}
            hp={foeCreature.stats.hp}
          />
          <div className="mt-2 flex items-center">
            <Swords className="mr-1" size={16} />
            <span>Opponent</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
