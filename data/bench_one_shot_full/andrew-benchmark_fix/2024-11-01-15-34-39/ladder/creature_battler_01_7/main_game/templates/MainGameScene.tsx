import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Button } from "@/components/ui/button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Sword, Shield } from 'lucide-react';

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
    opponent: Player;
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
          <Sword className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/creatures/${playerCreature.uid}.jpg`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/creatures/${opponentCreature.uid}.jpg`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          <p>Battle in progress...</p>
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
              onClick={() => emitButtonClick('use-skill')}
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
