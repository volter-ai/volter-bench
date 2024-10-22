import { useCurrentButtons } from "@/lib/useChoices.ts";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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
          {player && (
            <PlayerCard 
              uid={player.uid}
              playerName={player.display_name}
              imageUrl={`/images/players/${player.meta.prototype_id}.jpg`}
            />
          )}
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              imageUrl={`/images/creatures/${player_creature.meta.prototype_id}.jpg`}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
          )}
        </div>
        <div className="flex flex-col items-center">
          {opponent && (
            <PlayerCard 
              uid={opponent.uid}
              playerName={opponent.display_name}
              imageUrl={`/images/players/${opponent.meta.prototype_id}.jpg`}
            />
          )}
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              imageUrl={`/images/creatures/${opponent_creature.meta.prototype_id}.jpg`}
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t border-gray-300">
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
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
