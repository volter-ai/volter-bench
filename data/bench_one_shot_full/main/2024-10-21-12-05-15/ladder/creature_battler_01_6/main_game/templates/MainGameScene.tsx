import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Sword, Shield } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.uid}.jpg`}
              hp={playerCreature.stats.hp}
            />
          )}
          <Sword className="mt-2 text-blue-500" />
        </div>
        <div className="flex flex-col items-center">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.uid}.jpg`}
              hp={opponentCreature.stats.hp}
            />
          )}
          <Shield className="mt-2 text-red-500" />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 shadow-lg">
        <Card className="mb-4 p-2">
          <p className="text-gray-700">Game description goes here...</p>
        </Card>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
          {availableButtonSlugs.includes('continue') && (
            <Button onClick={() => emitButtonClick('continue')}>Continue</Button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button onClick={() => emitButtonClick('quit')} variant="destructive">Quit</Button>
          )}
        </div>
      </div>
    </div>
  );
}
