import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { SkillButton } from "@/components/ui/custom/skill/skill_button";

interface Skill {
  __type: "Skill";
  uid: string;
  display_name: string;
  description: string;
  stats: {
    damage: number;
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
  };
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
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const foeCreature = props.data.entities.foe_creature;

  return (
    <div className="w-full h-full flex flex-col bg-background">
      {/* HUD Navigation */}
      <div className="h-16 bg-secondary flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-2">
          <Sword className="h-5 w-5" />
          <span className="font-bold">Battle Scene</span>
        </div>
        <div className="flex items-center gap-2">
          <Shield className="h-5 w-5" />
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow grid grid-cols-2 gap-8 p-8">
        {playerCreature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-semibold">Your Creature</span>
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}
        
        {foeCreature && (
          <div className="flex flex-col items-center gap-2">
            <span className="text-sm font-semibold">Opponent's Creature</span>
            <CreatureCard
              uid={foeCreature.uid}
              name={foeCreature.display_name}
              hp={foeCreature.stats.hp}
              maxHp={foeCreature.stats.max_hp}
              imageUrl={`/creatures/${foeCreature.display_name.toLowerCase()}.png`}
            />
          </div>
        )}
      </div>

      {/* Skills UI */}
      <div className="h-48 bg-secondary/50 border-t p-4">
        <div className="flex flex-wrap gap-2">
          {playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={`Damage: ${skill.stats.damage}`}
              disabled={!availableButtonSlugs.includes(skill.uid)}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
