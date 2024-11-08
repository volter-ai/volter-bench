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

  const getImageUrl = (type: string, id: string) => `/assets/${type}/${id}.png`;

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs?.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  const renderSkills = () => {
    const skills = player_creature?.collections?.skills;
    
    if (!Array.isArray(skills) || skills.length === 0) {
      return (
        <div className="col-span-3 text-center text-white">
          No skills available
        </div>
      );
    }

    return (
      <div className="grid grid-cols-3 gap-4 w-full">
        {skills.map((skill) => (
          <SkillButton
            key={skill.uid}
            uid={skill.uid}
            name={skill.display_name}
            description={skill.description}
            stats={`Damage: ${skill.stats.damage}`}
            disabled={!availableButtonSlugs?.includes(skill.uid)}
            onClick={() => handleSkillClick(skill.uid)}
          />
        ))}
      </div>
    );
  };

  return (
    <div className="h-screen w-screen bg-slate-900">
      <div className="container mx-auto h-full aspect-video grid grid-rows-[auto_1fr_auto] gap-4 p-4">
        {/* HUD */}
        <nav className="flex justify-between items-center bg-slate-800 rounded-lg p-4">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={getImageUrl('player', player.meta.prototype_id)}
            />
          )}
          <div className="flex gap-4">
            <Sword className="w-6 h-6 text-white" />
            <Shield className="w-6 h-6 text-white" />
          </div>
          {foe && (
            <PlayerCard
              uid={foe.uid}
              name={foe.display_name}
              imageUrl={getImageUrl('player', foe.meta.prototype_id)}
            />
          )}
        </nav>

        {/* Battlefield */}
        <div className="flex justify-between items-center px-8">
          {player_creature && (
            <div className="relative">
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-white">Player</span>
              <CreatureCard
                uid={player_creature.uid}
                name={player_creature.display_name}
                hp={player_creature.stats.hp}
                maxHp={player_creature.stats.max_hp}
                imageUrl={getImageUrl('creature', player_creature.meta.prototype_id)}
              />
            </div>
          )}

          {foe_creature && (
            <div className="relative">
              <span className="absolute -top-8 left-1/2 -translate-x-1/2 text-white">Opponent</span>
              <CreatureCard
                uid={foe_creature.uid}
                name={foe_creature.display_name}
                hp={foe_creature.stats.hp}
                maxHp={foe_creature.stats.max_hp}
                imageUrl={getImageUrl('creature', foe_creature.meta.prototype_id)}
              />
            </div>
          )}
        </div>

        {/* Skills UI */}
        <div className="bg-slate-800 rounded-lg p-4">
          {renderSkills()}
        </div>
      </div>
    </div>
  );
}
