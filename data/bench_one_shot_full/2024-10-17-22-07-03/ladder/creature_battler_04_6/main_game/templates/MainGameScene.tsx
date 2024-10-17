import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Sword, Zap } from 'lucide-react'
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

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
    is_physical: boolean;
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
    sp_attack: number;
    sp_defense: number;
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      <div className="h-2/3 relative">
        {/* Battlefield Display */}
        <div className="absolute bottom-0 left-0 w-1/3">
          {player_creature && (
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              image="/path/to/player_creature_back_image.png"
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
            />
          )}
        </div>
        <div className="absolute bottom-0 right-0 w-1/3">
          <div className="text-right">
            <h3>{player_creature?.display_name}</h3>
            <p>HP: {player_creature?.stats.hp}/{player_creature?.stats.max_hp}</p>
          </div>
        </div>
        <div className="absolute top-0 right-0 w-1/3">
          {opponent_creature && (
            <CreatureCard
              uid={opponent_creature.uid}
              name={opponent_creature.display_name}
              image="/path/to/opponent_creature_front_image.png"
              hp={opponent_creature.stats.hp}
              maxHp={opponent_creature.stats.max_hp}
            />
          )}
        </div>
        <div className="absolute top-0 left-0 w-1/3">
          <div>
            <h3>{opponent_creature?.display_name}</h3>
            <p>HP: {opponent_creature?.stats.hp}/{opponent_creature?.stats.max_hp}</p>
          </div>
        </div>
      </div>
      <div className="h-1/3 bg-gray-100 p-4">
        {/* User Interface */}
        <div className="grid grid-cols-2 gap-4">
          {player_creature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              disabled={!enabledUIDs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            >
              {skill.meta.is_physical ? <Sword className="mr-2" /> : <Zap className="mr-2" />}
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
      </div>
    </div>
  );
}
