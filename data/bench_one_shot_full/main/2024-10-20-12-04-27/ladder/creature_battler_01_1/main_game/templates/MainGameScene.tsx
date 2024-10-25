import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  stats: {
    damage: number;
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
  };
  uid: string;
  display_name: string;
  description: string;
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
}

interface GameUIData {
  entities: {
    player: Player;
    foe: Player;
    player_creature: Creature;
    foe_creature: Creature;
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

  const { player_creature, foe_creature } = props.data.entities;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-gray-800 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player: {props.data.entities.player.display_name}</span>
        </div>
        <div className="flex items-center">
          <Swords className="mr-2" />
          <span>Opponent: {props.data.entities.foe.display_name}</span>
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={player_creature.uid}
          name={player_creature.display_name}
          imageUrl="/placeholder-player-creature.jpg"
          hp={player_creature.stats.hp}
        />
        <div className="text-2xl font-bold">VS</div>
        <CreatureCard
          uid={foe_creature.uid}
          name={foe_creature.display_name}
          imageUrl="/placeholder-foe-creature.jpg"
          hp={foe_creature.stats.hp}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                onClick={() => emitButtonClick(skill.uid)}
                disabled={!availableButtonSlugs.includes(skill.uid)}
              />
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-600">
            {props.data.meta.battle_ended ? "Battle Ended" : "Waiting for opponent..."}
          </div>
        )}
      </div>
    </div>
  );
}
