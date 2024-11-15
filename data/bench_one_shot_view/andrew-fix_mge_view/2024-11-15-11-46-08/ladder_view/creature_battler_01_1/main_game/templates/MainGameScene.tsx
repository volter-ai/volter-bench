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

  const { player, foe, player_creature, foe_creature } = props.data?.entities || {};

  if (!player || !foe || !player_creature || !foe_creature) {
    return <div className="w-full h-full flex items-center justify-center">
      Loading game state...
    </div>;
  }

  const handleSkillClick = (skillUid: string) => {
    if (availableButtonSlugs.includes(skillUid)) {
      emitButtonClick(skillUid);
    }
  };

  return (
    <div className="w-full h-full flex flex-col bg-background">
      {/* HUD */}
      <div className="h-16 bg-secondary flex items-center justify-between px-4 border-b">
        <div className="flex items-center gap-4">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl="/players/default_avatar.png"
          />
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <Sword className="w-5 h-5" />
            <span>Battle Phase</span>
          </div>
          <div className="flex items-center gap-2">
            <Shield className="w-5 h-5" />
            <span>Defense Ready</span>
          </div>
        </div>
      </div>

      {/* Battlefield */}
      <div className="flex-grow flex items-center justify-between px-16 bg-secondary/10">
        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Your Creature</span>
          <CreatureCard
            uid={player_creature.uid}
            name={player_creature.display_name}
            hp={player_creature.stats.hp}
            imageUrl="/creatures/default_creature.png"
          />
        </div>

        <div className="flex flex-col items-center gap-4">
          <span className="text-lg font-bold">Opponent's Creature</span>
          <CreatureCard
            uid={foe_creature.uid}
            name={foe_creature.display_name}
            hp={foe_creature.stats.hp}
            imageUrl="/creatures/default_creature.png"
          />
        </div>
      </div>

      {/* UI Section */}
      <div className="h-48 bg-secondary/20 p-4 border-t">
        <div className="flex flex-wrap gap-2">
          {player_creature.collections.skills?.map((skill) => (
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
  );
}
