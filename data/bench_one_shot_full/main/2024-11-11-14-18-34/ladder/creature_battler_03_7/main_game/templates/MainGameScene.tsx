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
    base_damage: number;
  };
}

interface Creature {
  __type: "Creature";
  uid: string;
  display_name: string;
  stats: {
    hp: number;
    max_hp: number;
    attack: number;
    defense: number;
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
    opponent: Player;
    player_creature: Creature;
    opponent_creature: Creature;
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const playerCreature = props.data.entities.player_creature;
  const opponentCreature = props.data.entities.opponent_creature;

  if (!playerCreature || !opponentCreature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading battle...
    </div>;
  }

  return (
    <div className="w-full h-full grid grid-rows-[auto_1fr_auto] gap-4 p-4">
      {/* HUD */}
      <div className="flex justify-between items-center p-2 bg-slate-800 rounded-lg">
        <div className="flex items-center gap-2">
          <Shield className="w-5 h-5" />
          <span>Defense: {playerCreature.stats.defense}</span>
        </div>
        <div className="flex items-center gap-2">
          <Swords className="w-5 h-5" />
          <span>Attack: {playerCreature.stats.attack}</span>
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex justify-between items-center px-12">
        <div className="transform scale-x-1">
          <CreatureCard
            uid={playerCreature.uid}
            name={playerCreature.display_name}
            currentHp={playerCreature.stats.hp}
            maxHp={playerCreature.stats.max_hp}
          />
        </div>
        <div className="transform scale-x-[-1]">
          <CreatureCard
            uid={opponentCreature.uid}
            name={opponentCreature.display_name}
            currentHp={opponentCreature.stats.hp}
            maxHp={opponentCreature.stats.max_hp}
          />
        </div>
      </div>

      {/* Skills UI */}
      <div className="grid grid-cols-2 gap-2 p-4 bg-slate-800 rounded-lg">
        {playerCreature.collections.skills?.filter(skill => 
          !availableButtonSlugs || availableButtonSlugs.includes(skill.uid)
        ).map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            name={skill.display_name}
            description={skill.description}
            damage={skill.stats.base_damage}
          />
        ))}
      </div>
    </div>
  );
}
