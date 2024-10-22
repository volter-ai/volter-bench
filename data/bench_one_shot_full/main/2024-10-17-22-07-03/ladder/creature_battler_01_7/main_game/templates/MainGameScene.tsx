import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: { [key: string]: number };
  uid: string;
  display_name: string;
  description: string;
}

interface Creature {
  __type: "Creature";
  stats: { hp: number; max_hp: number };
  uid: string;
  display_name: string;
  description: string;
  collections: { skills: Skill[] };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: { creatures: Creature[] };
}

interface GameUIData {
  entities: {
    player: Player;
    bot: Player;
    player_creature: Creature;
    bot_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const botCreature = props.data.entities.bot_creature;

  return (
    <div className="w-full h-full flex flex-col">
      {/* HUD */}
      <nav className="bg-gray-800 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature.stats.hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={botCreature.uid}
            name={botCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={botCreature.stats.hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-gray-100 p-4">
        <div className="mb-4 h-24 overflow-y-auto bg-white p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap justify-center">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={Object.entries(skill.stats)
                .map(([key, value]) => `${key}: ${value}`)
                .join(", ")}
              className="m-1"
              disabled={!enabledUIDs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
