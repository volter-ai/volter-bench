import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { Button } from "@/components/ui/button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
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
  } = useCurrentButtons()

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          playerName={player.display_name}
          imageUrl="/placeholder-player.png"
        />
        <PlayerCard
          uid={opponent.uid}
          playerName={opponent.display_name}
          imageUrl="/placeholder-opponent.png"
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl="/placeholder-creature.png"
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Sword size={24} />
            <span>{player_creature.stats.attack}</span>
            <Shield size={24} />
            <span>{player_creature.stats.defense}</span>
            <Zap size={24} />
            <span>{player_creature.stats.speed}</span>
          </div>
        </div>
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl="/placeholder-creature.png"
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
          <div className="mt-2 flex space-x-2">
            <Sword size={24} />
            <span>{opponent_creature.stats.attack}</span>
            <Shield size={24} />
            <span>{opponent_creature.stats.defense}</span>
            <Zap size={24} />
            <span>{opponent_creature.stats.speed}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="grid grid-cols-2 gap-2">
          {player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
          {availableButtonSlugs.includes('continue') && (
            <Button
              className="col-span-2"
              onClick={() => emitButtonClick('continue')}
            >
              Continue
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}
