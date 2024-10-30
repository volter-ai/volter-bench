import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Swords } from 'lucide-react';
import { useState, useEffect } from 'react';

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
  collections?: {
    skills?: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, foe_creature } = props.data.entities;
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay
    const timer = setTimeout(() => setIsLoading(false), 1000);
    return () => clearTimeout(timer);
  }, []);

  const renderSkillButtons = () => {
    const skills = player_creature.collections?.skills || [];
    return skills.map((skill: Skill) => (
      <SkillButton
        key={skill.uid}
        uid={skill.uid}
        skillName={skill.display_name}
        description={skill.description}
        stats={`Damage: ${skill.stats.damage}`}
        onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
        disabled={!availableButtonSlugs.includes(skill.uid)}
      />
    ));
  };

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-green-500" />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={player_creature.stats.hp}
          />
          <p className="mt-2 font-bold">Player</p>
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={foe_creature.stats.hp}
          />
          <p className="mt-2 font-bold">Opponent</p>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        {isLoading ? (
          <p className="text-center text-gray-600">Loading...</p>
        ) : (
          <div className="flex flex-wrap gap-2">
            {renderSkillButtons()}
          </div>
        )}
        {!isLoading && availableButtonSlugs.length === 0 && (
          <p className="text-center text-gray-600 mt-2">
            Waiting for your turn...
          </p>
        )}
      </div>
    </div>
  );
}
