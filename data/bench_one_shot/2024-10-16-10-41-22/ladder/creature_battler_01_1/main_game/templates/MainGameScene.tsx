import { useCurrentButtons, useThingInteraction } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Creature {
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
  };
}

interface Skill {
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
  };
}

interface GameUIData {
  entities: {
    player_creature: Creature;
    foe_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons();
  const { enabledUIDs } = useThingInteraction();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-gray-100">
      {/* HUD */}
      <nav className="bg-blue-600 text-white p-2 flex justify-between items-center">
        <div className="flex items-center">
          <Shield className="mr-2" />
          <span>Player</span>
        </div>
        <div className="flex items-center">
          <span>Opponent</span>
          <Swords className="ml-2" />
        </div>
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
        <CreatureCard
          uid={foeCreature?.uid ?? ""}
          name={foeCreature?.display_name ?? "Unknown"}
          imageUrl="/placeholder-creature.png"
          hp={foeCreature?.stats.hp ?? 0}
          maxHp={foeCreature?.stats.max_hp ?? 1}
        />
      </div>

      {/* User Interface */}
      <div className="bg-white p-4 h-1/3 overflow-y-auto">
        {availableButtonSlugs.length > 0 ? (
          <div className="grid grid-cols-2 gap-4">
            {availableButtonSlugs.map((slug) => {
              const skill = playerCreature?.collections?.skills?.find(
                (s: Skill) => s.uid === slug
              );
              return skill ? (
                <SkillButton
                  key={skill.uid}
                  uid={skill.uid}
                  skillName={skill.display_name}
                  description={skill.description}
                  stats={`Damage: ${skill.stats.damage}`}
                  disabled={!enabledUIDs.includes(skill.uid)}
                  onClick={() => emitButtonClick(skill.uid)}
                />
              ) : null;
            })}
          </div>
        ) : (
          <p className="text-center text-gray-600">
            Waiting for available actions...
          </p>
        )}
      </div>
    </div>
  );
}
