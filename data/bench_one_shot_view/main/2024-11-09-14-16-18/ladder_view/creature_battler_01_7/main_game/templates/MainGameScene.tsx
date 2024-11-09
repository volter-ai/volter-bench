import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Swords } from 'lucide-react';
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

  if (!playerCreature || !foeCreature) {
    return <div className="w-screen h-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="w-screen h-screen flex flex-col bg-background">
      {/* HUD */}
      <nav className="h-[10%] bg-secondary flex items-center justify-between px-6 border-b">
        <div className="flex items-center gap-2">
          <Shield className="w-6 h-6" />
          <span>Battle Scene</span>
        </div>
        <Swords className="w-6 h-6" />
      </nav>

      {/* Battlefield */}
      <div className="h-[60%] flex items-center justify-between px-12">
        <div className="flex flex-col items-center gap-4">
          <span className="text-sm font-bold">Your Creature</span>
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            hp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
            imageUrl="/placeholder.png"
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-sm font-bold">Opponent's Creature</span>
          <CreatureCard
            uid={foeCreature.uid}
            name={foeCreature.display_name}
            hp={foeCreature.stats.hp}
            maxHp={foeCreature.stats.max_hp}
            imageUrl="/placeholder.png"
          />
        </div>
      </div>

      {/* UI Controls */}
      <div className="h-[30%] bg-secondary/20 p-6">
        <div className="grid grid-cols-4 gap-4">
          {playerCreature.collections.skills.map((skill) => (
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
