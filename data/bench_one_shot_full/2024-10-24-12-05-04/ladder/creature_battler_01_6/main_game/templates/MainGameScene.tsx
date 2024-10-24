import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    damage: number;
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
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      <div className="flex-grow flex items-center justify-between p-4">
        <CreatureCard
          uid={playerCreature.uid}
          name={playerCreature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={playerCreature.stats.hp}
          className="transform scale-x-[-1]"
        />
        <Sword className="text-red-500 w-12 h-12" />
        <CreatureCard
          uid={foeCreature.uid}
          name={foeCreature.display_name}
          imageUrl="/placeholder-creature.jpg"
          hp={foeCreature.stats.hp}
        />
      </div>

      <div className="bg-white p-4 rounded-t-lg shadow-lg">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          <p>Battle description will appear here...</p>
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
            Quit
          </Button>
        </div>
      </div>
    </div>
  );
}
