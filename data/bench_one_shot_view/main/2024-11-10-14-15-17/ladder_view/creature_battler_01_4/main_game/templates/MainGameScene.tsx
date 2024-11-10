import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Shield, Sword } from 'lucide-react';
import { CreatureCard } from "@/components/ui/custom/creature/creature_card";
import { PlayerCard } from "@/components/ui/custom/player/player_card";
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

  const { player, foe, player_creature, foe_creature } = props.data.entities;

  if (!player || !foe || !player_creature || !foe_creature) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading battle...
    </div>;
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  return (
    <div className="h-screen w-screen bg-slate-900 text-white" role="main">
      <div className="grid grid-rows-[auto_1fr_auto] h-full max-w-7xl mx-auto">
        <nav className="flex justify-between items-center p-4 bg-slate-800" role="banner">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.uid}.png`}
          />
          <div className="flex items-center gap-2">
            <Sword className="w-6 h-6" aria-hidden="true" />
            <span className="text-xl font-bold">Battle Arena</span>
            <Shield className="w-6 h-6" aria-hidden="true" />
          </div>
          <PlayerCard
            uid={foe.uid}
            name={foe.display_name}
            imageUrl={`/players/${foe.uid}.png`}
          />
        </nav>

        <div className="flex justify-between items-center p-8 gap-8" role="region" aria-label="battlefield">
          <div className="relative">
            <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-green-400 font-bold">
              Your Creature
            </span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.uid}.png`}
            />
          </div>
          <div className="relative">
            <span className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-red-400 font-bold">
              Opponent's Creature
            </span>
            <CreatureCard
              uid={foe_creature.uid}
              name={foe_creature.display_name}
              hp={foe_creature.stats.hp}
              maxHp={foe_creature.stats.max_hp}
              imageUrl={`/creatures/${foe_creature.uid}.png`}
            />
          </div>
        </div>

        <div className="bg-slate-800 p-4" role="region" aria-label="skills">
          <div className="flex flex-wrap gap-4 justify-center">
            {player_creature.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={`Damage: ${skill.stats.damage}`}
                disabled={!availableButtonSlugs.includes(skill.uid)}
                onClick={() => handleSkillClick(skill.uid)}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
