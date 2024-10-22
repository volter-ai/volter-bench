import { useCurrentButtons } from "@/lib/useChoices.ts";
import { LogOut } from 'lucide-react';
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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* HUD */}
      <nav className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={playerCreature.stats.hp}
          className="border-blue-500 border-4"
        />
        <CreatureCard
          uid={opponentCreature.uid}
          name={opponentCreature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={opponentCreature.stats.hp}
          className="border-red-500 border-4"
        />
      </div>

      {/* User Interface */}
      <div className="bg-gray-100 p-4">
        <div className="bg-white p-4 mb-4 h-32 overflow-y-auto">
          {/* Game description text would go here */}
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
              disabled={!availableButtonSlugs.includes('use-skill')}
              onClick={() => emitButtonClick('use-skill', { skillId: skill.uid })}
            />
          ))}
          <Button
            onClick={() => emitButtonClick('quit')}
            disabled={!availableButtonSlugs.includes('quit')}
          >
            <LogOut className="mr-2 h-4 w-4" />
            Quit
          </Button>
        </div>
      </div>
    </div>
  );
}
