import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield } from 'lucide-react';
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
  meta: {
    battle_ended: boolean;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div>{props.data.entities.player.display_name}</div>
        <div className="flex items-center">
          <Shield className="mr-2" />
          {!props.data.meta.battle_ended ? "Battle in progress" : "Battle ended"}
        </div>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <div className="w-1/3">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={playerCreature.stats.hp}
          />
        </div>
        <div className="w-1/3 text-center">VS</div>
        <div className="w-1/3">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            imageUrl="/placeholder-creature.jpg"
            hp={opponentCreature.stats.hp}
          />
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/4 overflow-y-auto">
        <div className="grid grid-cols-2 gap-4">
          {playerCreature.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
              onClick={() => availableButtonSlugs.includes(skill.uid) && emitButtonClick(skill.uid)}
            />
          ))}
        </div>
        {playerCreature.collections.skills.length === 0 && (
          <p className="text-center text-gray-600">
            Waiting for your turn...
          </p>
        )}
      </div>
    </div>
  );
}
