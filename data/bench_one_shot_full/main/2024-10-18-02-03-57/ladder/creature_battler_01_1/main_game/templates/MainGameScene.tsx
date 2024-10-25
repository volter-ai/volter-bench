import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
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
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player_creature, foe_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Battle Arena</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={`/creatures/${player_creature.uid}.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2" />
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            imageUrl={`/creatures/${foe_creature.uid}.png`}
            hp={foe_creature.stats.hp}
            maxHp={foe_creature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        {availableButtonSlugs.length > 0 ? (
          <div className="flex flex-wrap gap-2">
            {player_creature.collections.skills
              .filter(skill => availableButtonSlugs.includes(skill.uid))
              .map((skill) => (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              ))}
          </div>
        ) : (
          <div className="bg-gray-100 p-4 rounded">
            <p className="text-gray-700">Waiting for your turn...</p>
          </div>
        )}
      </div>
    </div>
  );
}
