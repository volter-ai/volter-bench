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
  collections?: {
    skills?: Skill[];
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-screen flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-green-500" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
          <p className="mt-2 font-bold">Player</p>
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
          <p className="mt-2 font-bold">Opponent</p>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded overflow-y-auto">
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2 justify-center">
          {playerCreature.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes('use-skill')}
              onClick={() => emitButtonClick('use-skill')}
            />
          ))}
          <SkillButton
            uid="quit-button"
            skillName="Quit"
            description="Exit the battle"
            stats=""
            disabled={!availableButtonSlugs.includes('quit')}
            onClick={() => emitButtonClick('quit')}
          />
        </div>
      </div>
    </div>
  );
}
