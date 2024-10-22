import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
  meta: {
    skill_type: string;
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
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <span>{player?.display_name}</span>
        <span>VS</span>
        <span>{opponent?.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={player_creature?.uid || ""}
            name={player_creature?.display_name || "Unknown"}
            imageUrl="/placeholder-creature.png"
            hp={player_creature?.stats.hp || 0}
            maxHp={player_creature?.stats.max_hp || 1}
          />
          <div className="mt-2 flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{player_creature?.stats.defense}</span>
            <Swords className="text-red-500" />
            <span>{player_creature?.stats.attack}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponent_creature?.uid || ""}
            name={opponent_creature?.display_name || "Unknown"}
            imageUrl="/placeholder-creature.png"
            hp={opponent_creature?.stats.hp || 0}
            maxHp={opponent_creature?.stats.max_hp || 1}
          />
          <div className="mt-2 flex space-x-2">
            <Shield className="text-blue-500" />
            <span>{opponent_creature?.stats.defense}</span>
            <Swords className="text-red-500" />
            <span>{opponent_creature?.stats.attack}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 rounded-t-lg shadow-lg">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick(skill.uid)}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
