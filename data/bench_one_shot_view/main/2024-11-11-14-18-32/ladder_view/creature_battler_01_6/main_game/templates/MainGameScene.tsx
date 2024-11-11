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
  meta: {
    prototype_id: string;
  };
}

interface Player {
  __type: "Player";
  uid: string;
  display_name: string;
  collections: {
    creatures: Creature[];
  };
  meta: {
    prototype_id: string;
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

  const getImageUrl = (entity: { meta: { prototype_id: string }}) => 
    `/assets/sprites/${entity.meta.prototype_id}.png`;

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  return (
    <div className="h-screen w-full grid grid-rows-[auto_1fr_auto]">
      <nav className="bg-slate-800 p-4 flex justify-between items-center">
        <div className="flex items-center gap-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={getImageUrl(player)}
            />
          )}
        </div>
        <div className="flex items-center gap-4">
          {foe && (
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl={getImageUrl(foe)}
            />
          )}
        </div>
      </nav>

      <main className="flex justify-between items-center px-16 bg-slate-900">
        {player_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-green-500">
              Player
            </span>
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              hp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={getImageUrl(player_creature)}
            />
          </div>
        )}

        {foe_creature && (
          <div className="relative">
            <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-red-500">
              Opponent
            </span>
            <CreatureCard
              uid={foe_creature.uid}
              name={foe_creature.display_name}
              hp={foe_creature.stats.hp}
              maxHp={foe_creature.stats.max_hp}
              imageUrl={getImageUrl(foe_creature)}
            />
          </div>
        )}
      </main>

      <footer className="bg-slate-700 p-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
          {player_creature?.collections.skills?.map((skill) => (
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
      </footer>
    </div>
  );
}
