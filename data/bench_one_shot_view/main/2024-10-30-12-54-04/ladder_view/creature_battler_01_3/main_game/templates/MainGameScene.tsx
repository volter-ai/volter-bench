import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield } from 'lucide-react';

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
  };
  collections: {
    player_skill_queue: Skill[];
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;
  const playerSkills = props.data.collections.player_skill_queue || [];

  const getSkillByUid = (uid: string) => playerSkills.find(skill => skill.uid === uid);

  console.log("Available button slugs:", availableButtonSlugs);
  console.log("Player skills:", playerSkills);

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature.stats.hp}
          />
          <div className="mt-2 flex items-center">
            <Shield className="w-4 h-4 mr-1 text-blue-500" />
            <span className="text-sm font-bold">Player</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={foeCreature.uid}
            name={foeCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={foeCreature.stats.hp}
          />
          <div className="mt-2 flex items-center">
            <Shield className="w-4 h-4 mr-1 text-red-500" />
            <span className="text-sm font-bold">Opponent</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        {availableButtonSlugs.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {availableButtonSlugs.map((slug) => {
              const skill = getSkillByUid(slug);
              if (!skill) {
                console.warn(`Skill not found for UID: ${slug}`);
                return null;
              }
              return (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  onClick={() => emitButtonClick(slug)}
                />
              );
            })}
          </div>
        ) : playerSkills.length > 0 ? (
          <div className="bg-yellow-100 p-4 rounded-md">
            <p className="text-yellow-700">Skills available, but no actions can be taken at this time.</p>
          </div>
        ) : (
          <div className="bg-gray-100 p-4 rounded-md">
            <p className="text-gray-700">Waiting for game action...</p>
          </div>
        )}
      </div>
    </div>
  );
}
