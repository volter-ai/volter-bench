import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";
import { Sword, Shield, RefreshCw, X } from 'lucide-react';

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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <nav className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4 bg-gray-100">
        {playerCreature && (
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.uid}.jpg`}
            hp={playerCreature.stats.hp}
            className="transform scale-x-[-1]"
          />
        )}
        <div className="flex flex-col items-center">
          <Sword className="text-red-500 mb-2" />
          <Shield className="text-blue-500" />
        </div>
        {opponentCreature && (
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.uid}.jpg`}
            hp={opponentCreature.stats.hp}
          />
        )}
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4">
        <div className="mb-4 h-24 bg-white p-2 rounded overflow-y-auto">
          {/* Game description text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
            />
          ))}
          {availableButtonSlugs.includes('play-again') && (
            <Button onClick={() => emitButtonClick('play-again')}>
              <RefreshCw className="mr-2 h-4 w-4" /> Play Again
            </Button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button onClick={() => emitButtonClick('quit')} variant="destructive">
              <X className="mr-2 h-4 w-4" /> Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
