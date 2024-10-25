import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
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
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {playerCreature && (
          <div className="flex flex-col items-center">
            <Sword className="w-8 h-8 mb-2" />
            <span>Player</span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl="/placeholder-creature.jpg"
              hp={playerCreature.stats.hp}
            />
          </div>
        )}
        {foeCreature && (
          <div className="flex flex-col items-center">
            <Shield className="w-8 h-8 mb-2" />
            <span>Opponent</span>
            <CreatureCard
              uid={foeCreature.uid}
              name={foeCreature.display_name}
              imageUrl="/placeholder-creature.jpg"
              hp={foeCreature.stats.hp}
            />
          </div>
        )}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {availableButtonSlugs.includes('use-skill') && (
            <SkillButton
              uid="skill-1"
              skillName="Tackle"
              description="A basic attack"
              stats="Damage: 10"
              onClick={() => emitButtonClick('use-skill')}
            />
          )}
          {availableButtonSlugs.includes('quit') && (
            <Button onClick={() => emitButtonClick('quit')}>
              Quit
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
