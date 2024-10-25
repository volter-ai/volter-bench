import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { X } from 'lucide-react';

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <h1 className="text-xl font-bold">Battle Arena</h1>
        <button
          onClick={() => emitButtonClick('quit')}
          className="p-2 hover:bg-blue-700 rounded"
        >
          <X size={24} />
        </button>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={player_creature?.uid ?? ''}
          name={player_creature?.display_name ?? 'Player Creature'}
          imageUrl="/placeholder-player-creature.jpg"
          hp={player_creature?.stats.hp ?? 0}
          className="transform scale-x-[-1]"
        />
        <CreatureCard
          uid={opponent_creature?.uid ?? ''}
          name={opponent_creature?.display_name ?? 'Opponent Creature'}
          imageUrl="/placeholder-opponent-creature.jpg"
          hp={opponent_creature?.stats.hp ?? 0}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game description text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {player_creature?.collections.skills.map((skill) => (
            availableButtonSlugs.includes('use-skill') && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => emitButtonClick('use-skill', { skillId: skill.uid })}
              />
            )
          ))}
        </div>
      </div>
    </div>
  );
}
