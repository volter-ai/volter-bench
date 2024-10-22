import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react';
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
    <div className="flex flex-col w-full h-full bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div>{player?.display_name}</div>
        <div>VS</div>
        <div>{opponent?.display_name}</div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {player_creature && (
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <div className="flex items-center">
                <Sword className="w-4 h-4 mr-1" />
                <span>{player_creature.stats.attack}</span>
              </div>
              <div className="flex items-center">
                <Shield className="w-4 h-4 mr-1" />
                <span>{player_creature.stats.defense}</span>
              </div>
              <div className="flex items-center">
                <Zap className="w-4 h-4 mr-1" />
                <span>{player_creature.stats.speed}</span>
              </div>
            </div>
          </div>
        )}
        {opponent_creature && (
          <div className="flex flex-col items-center">
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              imageUrl="/placeholder-creature.png"
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
            <div className="mt-2 flex space-x-2">
              <div className="flex items-center">
                <Sword className="w-4 h-4 mr-1" />
                <span>{opponent_creature.stats.attack}</span>
              </div>
              <div className="flex items-center">
                <Shield className="w-4 h-4 mr-1" />
                <span>{opponent_creature.stats.defense}</span>
              </div>
              <div className="flex items-center">
                <Zap className="w-4 h-4 mr-1" />
                <span>{opponent_creature.stats.speed}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="grid grid-cols-2 gap-2">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
