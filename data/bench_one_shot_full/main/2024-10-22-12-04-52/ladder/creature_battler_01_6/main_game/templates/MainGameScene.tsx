import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Sword, RotateCcw, Home } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  description: string;
  collections?: {
    skills?: Skill[];
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full aspect-video bg-gray-100 flex flex-col">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="text-center">
          <h2 className="text-lg font-semibold mb-2">Player</h2>
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.uid}.png`}
              hp={playerCreature.stats.hp}
            />
          )}
        </div>
        <Sword className="w-12 h-12 text-red-500" />
        <div className="text-center">
          <h2 className="text-lg font-semibold mb-2">Opponent</h2>
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.uid}.png`}
              hp={opponentCreature.stats.hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4">
        <div className="bg-white rounded-lg p-4 mb-4 h-24 overflow-y-auto">
          {/* Game description text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
            />
          ))}
          {availableButtonSlugs.includes("play-again") && (
            <Button onClick={() => emitButtonClick("play-again")}>
              <RotateCcw className="mr-2 h-4 w-4" /> Play Again
            </Button>
          )}
          {availableButtonSlugs.includes("return-to-main-menu") && (
            <Button onClick={() => emitButtonClick("return-to-main-menu")}>
              <Home className="mr-2 h-4 w-4" /> Main Menu
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
