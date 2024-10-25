import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Swords } from 'lucide-react';

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
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  console.log("Available Button Slugs:", availableButtonSlugs);

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-blue-500" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature.stats.hp}
            className="transform scale-75 sm:scale-100"
          />
          <span className="text-blue-500">Player</span>
        </div>
        <Swords className="w-12 h-12 text-red-500" />
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={botCreature.stats.hp}
            className="transform scale-75 sm:scale-100"
          />
          <span className="text-red-500">Opponent</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-200 p-4 h-1/3 overflow-y-auto">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-2">
            {availableButtonSlugs.map((slug) => (
              <SkillButton
                key={slug}
                uid={slug}
                skillName={slug}
                description="Skill description"
                stats="Skill stats"
                onClick={() => emitButtonClick(slug)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-700">
            Waiting for your turn...
          </div>
        )}
      </div>
    </div>
  );
}
