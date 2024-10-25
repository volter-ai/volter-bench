import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Shield, Swords } from 'lucide-react';

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
  } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={`/images/creatures/${player_creature.meta.prototype_id}.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <div className="flex items-center">
              <Swords className="w-4 h-4 mr-1" />
              <span>{player_creature.stats.attack}</span>
            </div>
            <div className="flex items-center">
              <Shield className="w-4 h-4 mr-1" />
              <span>{player_creature.stats.defense}</span>
            </div>
          </div>
        </div>
        <div className="text-2xl font-bold">VS</div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl={`/images/creatures/${opponent_creature.meta.prototype_id}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <div className="flex items-center">
              <Swords className="w-4 h-4 mr-1" />
              <span>{opponent_creature.stats.attack}</span>
            </div>
            <div className="flex items-center">
              <Shield className="w-4 h-4 mr-1" />
              <span>{opponent_creature.stats.defense}</span>
            </div>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4 h-24 bg-gray-100 p-2 rounded overflow-y-auto">
          {/* Game information text would go here */}
          <p>What will {player_creature.display_name} do?</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {player_creature.collections.skills.map((skill) => (
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
