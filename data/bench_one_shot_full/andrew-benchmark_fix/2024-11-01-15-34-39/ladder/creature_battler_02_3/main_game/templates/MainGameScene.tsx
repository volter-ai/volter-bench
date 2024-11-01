import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Home, PlayCircle, XCircle } from 'lucide-react';
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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={playerCreature.stats.hp}
          maxHp={playerCreature.stats.max_hp}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={opponentCreature.uid}
          name={opponentCreature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={opponentCreature.stats.hp}
          maxHp={opponentCreature.stats.max_hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="grid grid-cols-2 gap-2 mb-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
            />
          ))}
        </div>
        <div className="flex justify-between">
          {availableButtonSlugs.includes('main-menu') && (
            <Button onClick={() => emitButtonClick('main-menu')}>
              <Home className="mr-2" /> Main Menu
            </Button>
          )}
          {availableButtonSlugs.includes('play-again') && (
            <Button onClick={() => emitButtonClick('play-again')}>
              <PlayCircle className="mr-2" /> Play Again
            </Button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button onClick={() => emitButtonClick('quit')}>
              <XCircle className="mr-2" /> Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
