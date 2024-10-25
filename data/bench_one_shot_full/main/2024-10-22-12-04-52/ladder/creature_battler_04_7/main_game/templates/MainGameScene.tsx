import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft } from 'lucide-react';
import { SkillButton } from "@/components/ui/custom/skill/skill_button";
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";

interface Skill {
  __type: "Skill";
  stats: { base_damage: number };
  meta: { skill_type: string; is_physical: boolean };
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
    sp_attack: number;
    sp_defense: number;
    speed: number;
  };
  meta: { creature_type: string };
  collections: { skills: Skill[] };
  uid: string;
  display_name: string;
  description: string;
}

interface Player {
  __type: "Player";
  collections: { creatures: Creature[] };
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
  meta: { battle_ended: boolean };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const { player_creature, opponent_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col" style={{ aspectRatio: '16/9' }}>
      {/* Battlefield Display */}
      <div className="flex-grow flex bg-gray-200 relative">
        {/* Opponent Creature */}
        <div className="absolute top-0 right-0 p-4">
          <CreatureCard
            uid={opponent_creature.uid}
            name={opponent_creature.display_name}
            image={`/images/creatures/${opponent_creature.meta.creature_type}.png`}
            hp={opponent_creature.stats.hp}
            maxHp={opponent_creature.stats.max_hp}
          />
        </div>
        {/* Opponent Creature Status */}
        <div className="absolute top-0 left-0 p-4">
          <div className="bg-white p-2 rounded shadow">
            <h3>{opponent_creature.display_name}</h3>
            <div>HP: {opponent_creature.stats.hp}/{opponent_creature.stats.max_hp}</div>
          </div>
        </div>
        {/* Player Creature */}
        <div className="absolute bottom-0 left-0 p-4">
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            image={`/images/creatures/${player_creature.meta.creature_type}_back.png`}
            hp={player_creature.stats.hp}
            maxHp={player_creature.stats.max_hp}
          />
        </div>
        {/* Player Creature Status */}
        <div className="absolute bottom-0 right-0 p-4">
          <div className="bg-white p-2 rounded shadow">
            <h3>{player_creature.display_name}</h3>
            <div>HP: {player_creature.stats.hp}/{player_creature.stats.max_hp}</div>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="h-1/3 bg-gray-100 p-4">
        <div className="grid grid-cols-2 gap-4 h-full">
          {availableButtonSlugs.includes('use-skill') && player_creature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.base_damage}, Type: ${skill.meta.skill_type}`}
              onClick={() => emitButtonClick('use-skill')}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
          {availableButtonSlugs.includes('return-to-main-menu') && (
            <SkillButton
              uid="return-to-main-menu"
              skillName="Return to Main Menu"
              description="Go back to the main menu"
              stats=""
              onClick={() => emitButtonClick('return-to-main-menu')}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Return to Main Menu
            </SkillButton>
          )}
        </div>
      </div>
    </div>
  );
}
