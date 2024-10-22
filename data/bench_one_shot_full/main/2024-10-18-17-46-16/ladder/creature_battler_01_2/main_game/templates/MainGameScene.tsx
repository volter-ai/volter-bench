import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Home, LogOut } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  description: string;
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
      <nav className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <h1 className="text-xl font-bold">Battle Arena</h1>
        <div className="flex space-x-2">
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <Button onClick={() => emitButtonClick('return-to-main-menu')} variant="ghost">
              <Home className="mr-2 h-4 w-4" /> Main Menu
            </Button>
          )}
          {availableButtonSlugs.includes('quit-game') && (
            <Button onClick={() => emitButtonClick('quit-game')} variant="ghost">
              <LogOut className="mr-2 h-4 w-4" /> Quit Game
            </Button>
          )}
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {playerCreature && (
          <div className="text-center">
            <h2 className="text-lg font-bold mb-2">Your Creature</h2>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder-creature.jpg"
              hp={playerCreature.stats.hp}
            />
          </div>
        )}
        {opponentCreature && (
          <div className="text-center">
            <h2 className="text-lg font-bold mb-2">Opponent's Creature</h2>
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl="/placeholder-creature.jpg"
              hp={opponentCreature.stats.hp}
            />
          </div>
        )}
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4">
        <Card className="mb-4 p-2">
          <p className="text-sm">Game description and status updates will appear here.</p>
        </Card>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
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
      </div>
    </div>
  );
}
