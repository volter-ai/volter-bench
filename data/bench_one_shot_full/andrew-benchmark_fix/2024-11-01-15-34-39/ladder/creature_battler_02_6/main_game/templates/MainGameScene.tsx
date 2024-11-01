import { useCurrentButtons } from "@/lib/useChoices.ts";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { Sword, Shield } from 'lucide-react';

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
  description: string;
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
  description: string;
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

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
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="mb-2"
          />
          <div className="flex items-center">
            <Sword className="w-5 h-5 mr-1" />
            <span>{player_creature.stats.attack}</span>
            <Shield className="w-5 h-5 ml-2 mr-1" />
            <span>{player_creature.stats.defense}</span>
          </div>
          <span className="mt-2 text-green-600 font-bold">Player's Creature</span>
        </div>

        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl="/placeholder-opponent.jpg"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
            className="mb-2"
          />
          <div className="flex items-center">
            <Sword className="w-5 h-5 mr-1" />
            <span>{opponent_creature.stats.attack}</span>
            <Shield className="w-5 h-5 ml-2 mr-1" />
            <span>{opponent_creature.stats.defense}</span>
          </div>
          <span className="mt-2 text-red-600 font-bold">Opponent's Creature</span>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white border-t-2 border-gray-300 p-4">
        {player_creature.collections.skills.length > 0 ? (
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
        ) : (
          <div className="bg-gray-100 p-4 rounded-md">
            <p className="text-center">Waiting for action...</p>
          </div>
        )}
      </div>
    </div>
  );
}
