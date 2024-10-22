import { useCurrentButtons } from "@/lib/useChoices.ts";
import { ArrowLeft } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
  collections: {
    skills: Skill[];
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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">{player?.display_name} vs {opponent?.display_name}</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-1 flex items-center justify-between p-4">
        {player_creature && (
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl="/placeholder-creature.png"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="transform scale-x-[-1]"
          />
        )}
        {opponent_creature && (
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl="/placeholder-creature.png"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        )}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              className="mr-2 mb-2"
            />
          ))}
        </div>
        {availableButtonSlugs.includes('return-to-main-menu') && (
          <Button
            onClick={() => emitButtonClick('return-to-main-menu')}
            className="flex items-center"
          >
            <ArrowLeft className="mr-2" size={16} />
            Return to Main Menu
          </Button>
        )}
      </div>
    </div>
  );
}
