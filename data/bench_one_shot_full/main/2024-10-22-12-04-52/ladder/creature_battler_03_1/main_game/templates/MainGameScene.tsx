import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword, Zap } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

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

  const { player, opponent, player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <div className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <PlayerCard
          uid={player.uid}
          playerName={player.display_name}
          imageUrl="/placeholder-player.jpg"
        />
        <div className="flex space-x-4">
          <div className="flex items-center">
            <Shield className="mr-1" /> {player_creature?.stats.defense ?? 0}
          </div>
          <div className="flex items-center">
            <Sword className="mr-1" /> {player_creature?.stats.attack ?? 0}
          </div>
          <div className="flex items-center">
            <Zap className="mr-1" /> {player_creature?.stats.speed ?? 0}
          </div>
        </div>
        <PlayerCard
          uid={opponent.uid}
          playerName={opponent.display_name}
          imageUrl="/placeholder-opponent.jpg"
        />
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        {player_creature && (
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            imageUrl={`/creatures/${player_creature.meta.prototype_id}.jpg`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
            className="transform scale-x-[-1]"
          />
        )}
        {opponent_creature && (
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            imageUrl={`/creatures/${opponent_creature.meta.prototype_id}.jpg`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        )}
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3">
        <div className="mb-4 h-24 overflow-y-auto bg-gray-100 p-2 rounded">
          {/* Text box content goes here */}
          Game progress and descriptions will be displayed here.
        </div>
        <div className="grid grid-cols-2 gap-2">
          {player_creature?.collections.skills.map((skill) => (
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
