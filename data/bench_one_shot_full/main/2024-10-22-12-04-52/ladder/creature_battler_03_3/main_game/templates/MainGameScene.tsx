import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react';
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

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
    attack: number;
    defense: number;
    speed: number;
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
  meta: {
    battle_ended: boolean;
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

      {/* Main game area */}
      <div className="flex-1 flex flex-col">
        {/* Battlefield */}
        <div className="flex-1 flex items-center justify-between p-4">
          {/* Player Creature */}
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <span className="flex items-center"><Sword size={16} className="mr-1" />{player_creature.stats.attack}</span>
              <span className="flex items-center"><Shield size={16} className="mr-1" />{player_creature.stats.defense}</span>
              <span className="flex items-center"><Zap size={16} className="mr-1" />{player_creature.stats.speed}</span>
            </div>
          </div>

          {/* Opponent Creature */}
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <span className="flex items-center"><Sword size={16} className="mr-1" />{opponent_creature.stats.attack}</span>
              <span className="flex items-center"><Shield size={16} className="mr-1" />{opponent_creature.stats.defense}</span>
              <span className="flex items-center"><Zap size={16} className="mr-1" />{opponent_creature.stats.speed}</span>
            </div>
          </div>
        </div>

        {/* User Interface */}
        <div className="bg-white p-4 border-t border-gray-200">
          <div className="mb-4 h-24 bg-gray-100 p-2 rounded overflow-y-auto">
            {/* Text box for game messages */}
            <p>Battle in progress...</p>
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
    </div>
  );
}
