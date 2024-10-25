import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { PlayCircle, XCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col justify-between bg-gray-100">
      {/* HUD */}
      <nav className="w-full bg-blue-500 text-white p-2">
        <h1 className="text-xl font-bold text-center">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={playerCreature.stats.hp}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={opponentCreature.uid}
          name={opponentCreature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={opponentCreature.stats.hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 rounded-t-lg shadow-lg">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!enabledUIDs.includes(skill.uid)}
            />
          ))}
          {availableButtonSlugs.includes('play-again') && (
            <Button
              onClick={() => emitButtonClick('play-again')}
              className="bg-green-500 hover:bg-green-600"
            >
              <PlayCircle className="mr-2 h-4 w-4" />
              Play Again
            </Button>
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button
              onClick={() => emitButtonClick('quit')}
              className="bg-red-500 hover:bg-red-600"
            >
              <XCircle className="mr-2 h-4 w-4" />
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
