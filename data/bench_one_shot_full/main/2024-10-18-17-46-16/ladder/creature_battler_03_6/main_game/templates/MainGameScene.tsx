import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react';
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
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2">
        <h1 className="text-xl font-bold">Creature Battle</h1>
      </nav>

      {/* Battlefield */}
      <div className="flex-grow flex justify-between items-center p-4">
        <CreatureCard
          uid={playerCreature?.uid ?? ""}
          name={playerCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.png"
          hp={playerCreature?.stats.hp ?? 0}
          maxHp={playerCreature?.stats.max_hp ?? 1}
          className="transform scale-x-[-1]"
        />
        <div className="flex space-x-4">
          <div className="flex flex-col items-center">
            <Sword className="w-6 h-6" />
            <span>{playerCreature?.stats.attack}</span>
          </div>
          <div className="flex flex-col items-center">
            <Shield className="w-6 h-6" />
            <span>{playerCreature?.stats.defense}</span>
          </div>
          <div className="flex flex-col items-center">
            <Zap className="w-6 h-6" />
            <span>{playerCreature?.stats.speed}</span>
          </div>
        </div>
        <CreatureCard
          uid={opponentCreature?.uid ?? ""}
          name={opponentCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.png"
          hp={opponentCreature?.stats.hp ?? 0}
          maxHp={opponentCreature?.stats.max_hp ?? 1}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="mb-4 h-24 bg-gray-100 p-2 rounded overflow-y-auto">
          {/* Text box for game descriptions */}
          <p>What will {playerCreature?.display_name} do?</p>
        </div>
        <div className="grid grid-cols-2 gap-2">
          {playerCreature?.collections.skills.map((skill) => (
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
