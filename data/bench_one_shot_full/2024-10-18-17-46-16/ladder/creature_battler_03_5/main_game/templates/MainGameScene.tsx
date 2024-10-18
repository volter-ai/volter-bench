import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    base_damage: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    skill_type: string;
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
    attack: number;
    defense: number;
    speed: number;
  };
  meta: {
    prototype_id: string;
    category: string;
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    creatures: Creature[];
  };
  uid: string;
  display_name: string;
  description: string;
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

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        <div className="flex flex-col items-center">
          <Shield className="w-8 h-8 mb-2 text-blue-500" />
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl={`/images/creatures/${playerCreature.meta.prototype_id}.png`}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="flex flex-col items-center">
          <Swords className="w-8 h-8 mb-2 text-red-500" />
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl={`/images/creatures/${opponentCreature.meta.prototype_id}.png`}
            hp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
