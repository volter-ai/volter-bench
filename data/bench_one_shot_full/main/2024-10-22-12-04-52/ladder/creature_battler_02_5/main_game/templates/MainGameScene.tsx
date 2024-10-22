import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={player_creature.uid}
          name={player_creature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={player_creature.stats.hp}
          maxHp={player_creature.stats.max_hp}
          className="transform scale-x-[-1]"
        />
        <div className="flex flex-col items-center">
          <Swords className="w-12 h-12 text-red-500 mb-2" />
          <span className="text-lg font-bold">VS</span>
          <Shield className="w-12 h-12 text-blue-500 mt-2" />
        </div>
        <CreatureCard
          uid={opponent_creature.uid}
          name={opponent_creature.display_name}
          imageUrl="/placeholder-creature.png"
          hp={opponent_creature.stats.hp}
          maxHp={opponent_creature.stats.max_hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-300">
        <div className="mb-4 h-24 bg-gray-200 p-2 rounded overflow-y-auto">
          {/* Game text would go here */}
          <p>What will {player_creature.display_name} do?</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {player_creature.collections?.skills?.map((skill: Skill) => (
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
