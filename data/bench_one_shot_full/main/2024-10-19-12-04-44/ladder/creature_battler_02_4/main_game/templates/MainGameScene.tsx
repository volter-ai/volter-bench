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
    attack: number;
    defense: number;
    speed: number;
  };
  description: string;
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Player {
  uid: string;
  display_name: string;
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
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.png"
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            className="mb-2"
          />
          <div className="flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{playerCreature.stats.defense}</span>
            <Swords className="text-red-500 ml-2" />
            <span>{playerCreature.stats.attack}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder-creature.png"
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
            className="mb-2"
          />
          <div className="flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{opponentCreature.stats.defense}</span>
            <Swords className="text-red-500 ml-2" />
            <span>{opponentCreature.stats.attack}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white border-t-2 border-gray-200 p-4">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Game text would go here */}
          <p>Battle in progress...</p>
        </div>
        <div className="flex flex-wrap gap-2">
          {playerCreature.collections?.skills?.map((skill: Skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
