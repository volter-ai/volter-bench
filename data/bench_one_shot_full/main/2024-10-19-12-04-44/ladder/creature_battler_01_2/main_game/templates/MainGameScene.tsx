import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  imageUrl: string; // Ensure this is part of the data
  collections?: {
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
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl={playerCreature?.imageUrl ?? "/placeholder-creature.jpg"}
            hp={playerCreature?.stats.hp ?? 0}
            className="mb-2"
          />
          <span className="text-sm font-bold">Player</span>
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={botCreature?.uid ?? ""}
            name={botCreature?.display_name ?? "Unknown"}
            imageUrl={botCreature?.imageUrl ?? "/placeholder-creature.jpg"}
            hp={botCreature?.stats.hp ?? 0}
            className="mb-2"
          />
          <span className="text-sm font-bold">Opponent</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug) => {
              const skill = playerCreature?.collections?.skills?.find(
                (s: Skill) => s.uid === slug
              );
              return skill ? (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  onClick={() => emitButtonClick(slug)}
                />
              ) : null;
            })}
          </div>
        ) : (
          <div className="text-center text-gray-700">
            Waiting for available actions...
          </div>
        )}
      </div>
    </div>
  );
}
