import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { User, UserMinus } from 'lucide-react';

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
    speed: number;
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
  image_url: string;
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
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

  // Debug logging
  console.log("Available button slugs:", availableButtonSlugs);
  console.log("Player creature skills:", player_creature.collections.skills);

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <User className="w-8 h-8 mb-2 text-green-500" />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={player_creature.image_url}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="transform scale-75 sm:scale-100"
          />
        </div>
        <div className="flex flex-col items-center">
          <UserMinus className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl={opponent_creature.image_url}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            className="transform scale-75 sm:scale-100"
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white border-t-2 border-gray-200 p-4 h-1/3">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug) => {
              const skill = player_creature.collections.skills.find(s => s.uid === slug);
              if (skill) {
                return (
                  <SkillButton
                    key={skill.uid}
                    uid={skill.uid}
                    skillName={skill.display_name}
                    description={skill.description}
                    stats={`Damage: ${skill.stats.base_damage}`}
                    onClick={() => emitButtonClick(slug)}
                  />
                );
              }
              return null;
            })}
          </div>
        ) : (
          <div className="bg-gray-100 p-4 rounded-lg h-full overflow-y-auto flex flex-col justify-between">
            <p className="text-gray-700">
              No actions available at the moment. Waiting for game state update...
            </p>
            <button
              className="bg-blue-500 text-white px-4 py-2 rounded mt-4"
              onClick={() => emitButtonClick("wait")}
            >
              Wait
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
