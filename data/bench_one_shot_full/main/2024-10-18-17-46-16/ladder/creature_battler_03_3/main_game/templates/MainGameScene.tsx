import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react';
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
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
  __type: "Creature";
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
  meta: {
    creature_type: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
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
    <div className="flex flex-col h-full w-full bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <span>{player?.display_name}</span>
        <span>VS</span>
        <span>{opponent?.display_name}</span>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={player_creature?.uid || ""}
            name={player_creature?.display_name || "Unknown"}
            imageUrl={`/creatures/${player_creature?.uid}.png`}
            hp={player_creature?.stats.hp || 0}
            maxHp={player_creature?.stats.max_hp || 1}
          />
          <div className="mt-2 flex space-x-2">
            <span className="flex items-center"><Sword size={16} className="mr-1" />{player_creature?.stats.attack}</span>
            <span className="flex items-center"><Shield size={16} className="mr-1" />{player_creature?.stats.defense}</span>
            <span className="flex items-center"><Zap size={16} className="mr-1" />{player_creature?.stats.speed}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponent_creature?.uid || ""}
            name={opponent_creature?.display_name || "Unknown"}
            imageUrl={`/creatures/${opponent_creature?.uid}.png`}
            hp={opponent_creature?.stats.hp || 0}
            maxHp={opponent_creature?.stats.max_hp || 1}
          />
          <div className="mt-2 flex space-x-2">
            <span className="flex items-center"><Sword size={16} className="mr-1" />{opponent_creature?.stats.attack}</span>
            <span className="flex items-center"><Shield size={16} className="mr-1" />{opponent_creature?.stats.defense}</span>
            <span className="flex items-center"><Zap size={16} className="mr-1" />{opponent_creature?.stats.speed}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 min-h-[200px]">
        {player_creature?.collections.skills.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {player_creature.collections.skills.map((skill) => (
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
        ) : (
          <div className="text-center text-lg">
            Waiting for opponent...
          </div>
        )}
      </div>
    </div>
  );
}
