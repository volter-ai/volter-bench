import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { ArrowLeft, X } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const {
    enabledUIDs
  } = useThingInteraction()

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={player_creature.uid}
          name={player_creature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={player_creature.stats.hp}
          maxHp={player_creature.stats.max_hp}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={opponent_creature.uid}
          name={opponent_creature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={opponent_creature.stats.hp}
          maxHp={opponent_creature.stats.max_hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4 h-24 bg-gray-100 p-2 rounded overflow-y-auto">
          {/* Text box content goes here */}
          <p>Battle information will be displayed here.</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
            />
          ))}
          {availableButtonSlugs.includes('quit-game') && (
            <Button
              onClick={() => emitButtonClick('quit-game')}
              className="bg-red-500 hover:bg-red-600 text-white"
            >
              <X className="mr-2 h-4 w-4" /> Quit Game
            </Button>
          )}
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <Button
              onClick={() => emitButtonClick('return-to-main-menu')}
              className="bg-gray-500 hover:bg-gray-600 text-white"
            >
              <ArrowLeft className="mr-2 h-4 w-4" /> Main Menu
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
