import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

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
  collections: {
    skills: Skill[];
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    base_damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

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
        <div className="flex flex-col items-center">
          <CreatureCard
            uid={playerCreature?.uid ?? ""}
            name={playerCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder-creature.png"
            hp={playerCreature?.stats.hp ?? 0}
            maxHp={playerCreature?.stats.max_hp ?? 1}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-1" size={16} />
            <span>{playerCreature?.stats.defense ?? 0}</span>
            <Swords className="ml-2 mr-1" size={16} />
            <span>{playerCreature?.stats.attack ?? 0}</span>
          </div>
        </div>

        <div className="flex flex-col items-center">
          <CreatureCard
            uid={opponentCreature?.uid ?? ""}
            name={opponentCreature?.display_name ?? "Unknown"}
            imageUrl="/placeholder-opponent.png"
            hp={opponentCreature?.stats.hp ?? 0}
            maxHp={opponentCreature?.stats.max_hp ?? 1}
          />
          <div className="mt-2 flex items-center">
            <Shield className="mr-1" size={16} />
            <span>{opponentCreature?.stats.defense ?? 0}</span>
            <Swords className="ml-2 mr-1" size={16} />
            <span>{opponentCreature?.stats.attack ?? 0}</span>
          </div>
        </div>
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 border-t-2 border-gray-200">
        <div className="grid grid-cols-2 gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={`Base Damage: ${skill.stats.base_damage}`}
              disabled={!enabledUIDs.includes(skill.uid)}
              onClick={() => emitButtonClick(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
