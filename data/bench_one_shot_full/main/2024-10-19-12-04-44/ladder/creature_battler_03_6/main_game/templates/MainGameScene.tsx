import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { PlayCircle, XCircle, Home } from 'lucide-react';

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
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
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
        <div className="mb-4">
          <h2 className="text-lg font-semibold mb-2">Skills</h2>
          <div className="flex space-x-2">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.base_damage}`}
              />
            ))}
          </div>
        </div>
        <div className="flex justify-between">
          {availableButtonSlugs.includes('play-again') && (
            <Button onClick={() => emitButtonClick('play-again')}>
              <PlayCircle className="mr-2 h-4 w-4" /> Play Again
            </Button>
          )}
          {availableButtonSlugs.includes('quit-game') && (
            <Button onClick={() => emitButtonClick('quit-game')}>
              <XCircle className="mr-2 h-4 w-4" /> Quit Game
            </Button>
          )}
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <Button onClick={() => emitButtonClick('return-to-main-menu')}>
              <Home className="mr-2 h-4 w-4" /> Main Menu
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
