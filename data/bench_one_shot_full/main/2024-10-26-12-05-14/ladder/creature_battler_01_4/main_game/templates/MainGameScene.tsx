import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { User, UserMinus } from 'lucide-react';

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  description: string;
  skills: Skill[];
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
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <User className="mb-2" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder.jpg"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <UserMinus className="mb-2" />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder.jpg"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded-lg shadow-inner">
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap justify-center">
          <SkillButton
            uid="tackle"
            skillName="Tackle"
            description="A basic attack"
            stats="Damage: 2"
            onClick={() => emitButtonClick("use-skill-tackle")}
            className="m-1"
            disabled={!availableButtonSlugs.includes("use-skill-tackle")}
          />
          {playerCreature.skills.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              onClick={() => emitButtonClick(`use-skill-${skill.uid}`)}
              className="m-1"
              disabled={!availableButtonSlugs.includes(`use-skill-${skill.uid}`)}
            />
          ))}
          <SkillButton
            uid="quit"
            skillName="Quit"
            description="Exit the battle"
            stats=""
            onClick={() => emitButtonClick("quit")}
            className="m-1"
            disabled={!availableButtonSlugs.includes("quit")}
          />
        </div>
      </div>
    </div>
  );
}
