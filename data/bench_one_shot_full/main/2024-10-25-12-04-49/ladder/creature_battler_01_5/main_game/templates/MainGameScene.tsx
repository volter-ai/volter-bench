import { useCurrentButtons } from "@/lib/useChoices.ts";
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
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Sword className="w-8 h-8 mb-2" />
          <span className="text-sm">Player</span>
          <CreatureCard
            uid={playerCreature?.uid || ""}
            name={playerCreature?.display_name || "Unknown"}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature?.stats.hp || 0}
          />
        </div>
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2" />
          <span className="text-sm">Opponent</span>
          <CreatureCard
            uid={opponentCreature?.uid || ""}
            name={opponentCreature?.display_name || "Unknown"}
            imageUrl="/placeholder-creature.jpg"
            hp={opponentCreature?.stats.hp || 0}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 shadow-lg">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game description text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              onClick={() => emitButtonClick(`use-skill-${skill.uid}`)}
              disabled={!availableButtonSlugs.includes(`use-skill-${skill.uid}`)}
            />
          ))}
          <SkillButton
            uid="quit"
            skillName="Quit"
            description="Exit the battle"
            stats=""
            onClick={() => emitButtonClick("quit")}
            disabled={!availableButtonSlugs.includes("quit")}
          />
        </div>
      </div>
    </div>
  );
}
