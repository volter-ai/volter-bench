import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield } from 'lucide-react';
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
  meta: {
    prototype_id: string;
    category: string;
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
  meta: {
    prototype_id: string;
    category: string;
  };
  collections: {
    skills: Skill[];
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  description: string;
  meta: {
    prototype_id: string;
    category: string;
  };
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
  collections: {
    player_skill_queue: Skill[];
    foe_skill_queue: Skill[];
  };
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons();

  const { player, foe, player_creature, foe_creature } = props.data.entities;

  const handleSkillClick = (skillUid: string) => {
    if (!availableButtonSlugs.includes(skillUid)) return;
    emitButtonClick(skillUid);
  };

  return (
    <div className="h-screen w-screen bg-slate-900">
      <div className="container mx-auto h-full aspect-video grid grid-rows-[auto_1fr_auto] gap-4 p-4">
        {/* HUD */}
        <nav className="bg-slate-800 rounded-lg p-4 flex justify-between items-center">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/assets/players/${player.meta.prototype_id}.png`}
            />
          )}
          <div className="flex items-center gap-2">
            <Sword className="h-6 w-6 text-blue-400" />
            <span className="text-white font-bold">VS</span>
            <Shield className="h-6 w-6 text-red-400" />
          </div>
          {foe && (
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl={`/assets/players/${foe.meta.prototype_id}.png`}
            />
          )}
        </nav>

        {/* Battlefield */}
        <div className="flex justify-between items-center px-8">
          {player_creature && (
            <div className="relative">
              <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-white font-bold">
                Your Creature
              </div>
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl={`/assets/creatures/${player_creature.meta.prototype_id}.png`}
              />
            </div>
          )}

          {foe_creature && (
            <div className="relative">
              <div className="absolute -top-8 left-1/2 -translate-x-1/2 text-white font-bold">
                Opponent's Creature
              </div>
              <CreatureCard
                uid={foe_creature.uid}
                name={foe_creature.display_name}
                hp={foe_creature.stats.hp}
                maxHp={foe_creature.stats.max_hp}
                imageUrl={`/assets/creatures/${foe_creature.meta.prototype_id}.png`}
              />
            </div>
          )}
        </div>

        {/* Skills UI */}
        <div className="bg-slate-800 rounded-lg p-4">
          <div className="grid grid-cols-4 gap-4">
            {player_creature?.collections?.skills?.map((skill) => (
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
